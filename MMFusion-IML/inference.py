import argparse
import os
import numpy as np
import cv2
from torch.utils.data import DataLoader
import torch
import torchvision.transforms.functional as TF
import logging
import matplotlib.pyplot as plt
from data.datasets import ManipulationDataset
from models.cmnext_conf import CMNeXtWithConf
from models.modal_extract import ModalitiesExtractor
from configs.cmnext_init_cfg import _C as config, update_config

parser = argparse.ArgumentParser(description='Infer')
parser.add_argument('-gpu', '--gpu', type=int, default=0, help='device, use -1 for cpu')
parser.add_argument('-log', '--log', type=str, default='INFO', help='logging level')
parser.add_argument('-exp', '--exp', type=str, default='experiments/ec_example_phase2.yaml', help='Yaml experiment file')
parser.add_argument('-ckpt', '--ckpt', type=str, default='ckpt/early_fusion_detection.pth', help='Checkpoint')
parser.add_argument('-path', '--path', type=str, default='example.png', help='Image path')
parser.add_argument('opts', help="other options", default=None, nargs=argparse.REMAINDER)

args = parser.parse_args()

config = update_config(config, args.exp)

loglvl = getattr(logging, args.log.upper())
logging.basicConfig(level=loglvl)

gpu = args.gpu

device = 'cuda:%d' % gpu if gpu >= 0 else 'cpu'
np.set_printoptions(formatter={'float': '{: 7.3f}'.format})

if device != 'cpu':
    # cudnn setting
    import torch.backends.cudnn as cudnn

    cudnn.benchmark = False
    cudnn.deterministic = True
    cudnn.enabled = config.CUDNN.ENABLED

def convertHeatmapToEdge(heatmap_path=""):
    # Step 1: Read the image
    image = cv2.imread(heatmap_path, cv2.IMREAD_UNCHANGED)

    # Step 2: Convert the image to the HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Step 3: Create a mask for the red regions using the updated HSV ranges
    lower_red1 = np.array([0, 70, 50])
    upper_red1 = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv_image, lower_red1, upper_red1)

    lower_red2 = np.array([170, 70, 50])
    upper_red2 = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)

    # Combine both masks
    red_mask = cv2.bitwise_or(mask1, mask2)

    # Step 4: Remove noise and fill holes using morphological operations
    kernel = np.ones((5, 5), np.uint8)
    red_mask_cleaned = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)  # Fill small holes
    red_mask_cleaned = cv2.morphologyEx(red_mask_cleaned, cv2.MORPH_OPEN, kernel)  # Remove small noise
    red_mask_cleaned = cv2.dilate(red_mask_cleaned, kernel, iterations=2)  # Further fill gaps

    # Step 5: Remove small regions (<= 10% of image area)
    # Calculate the total area of the image
    total_area = image.shape[0] * image.shape[1]
    min_area_threshold = 0.005 * total_area

    # Find connected components in the mask
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(red_mask_cleaned, connectivity=8)

    # Create a mask for large components
    large_components_mask = np.zeros_like(red_mask_cleaned)

    for i in range(1, num_labels):  # Start from 1 to skip the background
        if stats[i, cv2.CC_STAT_AREA] > min_area_threshold:
            large_components_mask[labels == i] = 255

    # Step 6: Apply the large components mask to the original image
    result = cv2.bitwise_and(image, image, mask=large_components_mask)

    # Step 7: Set non-red regions to transparent
    # Check the number of channels in the input image
    if image.shape[2] == 3:  # If the image has 3 channels (BGR)
        b, g, r = cv2.split(result)
        alpha = large_components_mask
        # Merge the BGR channels with the alpha channel
        rgba = cv2.merge([b, g, r, alpha])
    elif image.shape[2] == 4:  # If the image has 4 channels (BGRA)
        b, g, r, _ = cv2.split(result)
        alpha = large_components_mask
        # Merge the BGRA channels with the new alpha channel
        rgba = cv2.merge([b, g, r, alpha])

    # Save the result image
    cv2.imwrite("temp.png", rgba)

    image = cv2.imread("temp.png", cv2.IMREAD_UNCHANGED)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Định nghĩa phạm vi màu đỏ trong không gian màu HSV
    lower_red1 = np.array([0, 70, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 70, 50])
    upper_red2 = np.array([180, 255, 255])

    # Tạo mặt nạ cho màu đỏ
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    # Tìm các đường viền
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Tạo một ảnh mới với nền trong suốt
    transparent_background = np.zeros((image.shape[0], image.shape[1], 4), dtype=np.uint8)

    # Vẽ tất cả các đường viền trên ảnh với nền trong suốt
    cv2.drawContours(transparent_background, contours, -1, (0, 0, 255, 255), thickness=2)

    os.remove("temp.png")
    # Lưu ảnh kết quả
    cv2.imwrite(heatmap_path, transparent_background)

def main():
    modal_extractor = ModalitiesExtractor(config.MODEL.MODALS[1:], config.MODEL.NP_WEIGHTS)

    model = CMNeXtWithConf(config.MODEL)

    ckpt = torch.load(args.ckpt)

    model.load_state_dict(ckpt['state_dict'])
    modal_extractor.load_state_dict(ckpt['extractor_state_dict'])

    modal_extractor.to(device)
    model = model.to(device)
    modal_extractor.eval()
    model.eval()

    mask_name = os.path.basename(args.path).split(".")[0]+"_mask.png"
    output_dir = r"..\server\masks"

    target = os.path.join(output_dir, mask_name)
    # target = args.path.split(".")[-2] + "_mask.png"

    with open('tmp_inf.txt', 'w') as f:
        f.write(args.path + ' None 0\n')

    val = ManipulationDataset('tmp_inf.txt',
                            config.DATASET.IMG_SIZE,
                            train=False)
    val_loader = DataLoader(val,
                            batch_size=1,
                            shuffle=False,
                            num_workers=config.WORKERS,
                            pin_memory=True)
    f1 = []
    f1th = []
    for step, (images, _, masks, lab) in enumerate(val_loader):
        with torch.no_grad():
            images = images.to(device, non_blocking=True)
            masks = masks.squeeze(1).to(device, non_blocking=True)

            modals = modal_extractor(images)

            images_norm = TF.normalize(images, mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            inp = [images_norm] + modals

            anomaly, confidence, detection = model(inp)

            gt = masks.squeeze().cpu().numpy()
            map = torch.nn.functional.softmax(anomaly, dim=1)[:, 1, :, :].squeeze().cpu().numpy()
            det = detection.item()
            with open(r'..\.\server\accuracy.txt', 'w') as file:
                file.write(str(det))

            plt.imsave(target, map, cmap='RdBu_r', vmin=0, vmax=1)
            convertHeatmapToEdge(target)
    os.remove('tmp_inf.txt')
    print(f"Ran on {args.path}")
    print(f"Detection score: {det}")
    print(f"Localization map saved in {target}")

if __name__ == "__main__":
    main()