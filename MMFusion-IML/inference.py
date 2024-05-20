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
    # Read the heat map image
    heat_map = cv2.imread(heatmap_path, cv2.IMREAD_GRAYSCALE)

    # Apply thresholding to convert to binary image
    _, binary_image = cv2.threshold(heat_map, 127, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a transparent blank canvas
    canvas = np.zeros((heat_map.shape[0], heat_map.shape[1], 4), dtype=np.uint8)
    canvas[:, :, 3] = 0  # Set alpha channel to 0 (fully transparent)

    # Choose a color for the contour (BGR format)
    contour_color = (0, 0, 255)  # Red color

    # Draw contours on the canvas with the specified color
    cv2.drawContours(canvas, contours, -1, contour_color + (255,), 2)  # Contour color with full opacity


    cv2.imwrite(heatmap_path, canvas)

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

            plt.imsave(target, map, cmap='RdBu_r', vmin=0, vmax=1)
            convertHeatmapToEdge(target)
    os.remove('tmp_inf.txt')
    print(f"Ran on {args.path}")
    print(f"Detection score: {det}")
    print(f"Localization map saved in {target}")

if __name__ == "__main__":
    main()