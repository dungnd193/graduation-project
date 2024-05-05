import matplotlib.pyplot as plt
import cv2
from skimage.metrics import structural_similarity
import numpy as np

au_pic_path = r"D:\dungnd\data\CASIA2\Au\Au_arc_00086.jpg"
sp_pic_path = r"D:\dungnd\data\CASIA2\Tp\Tp_D_CNN_S_N_cha10122_nat00059_12169"

au_image = plt.imread(au_pic_path)
sp_image = plt.imread(sp_pic_path)
print(au_image.shape)
print(sp_image.shape)
if sp_image.shape == au_image.shape:
    # convert images to grayscale
    gray_au_image = cv2.cvtColor(au_image, cv2.COLOR_BGR2GRAY)
    gray_sp_image = cv2.cvtColor(sp_image, cv2.COLOR_BGR2GRAY)
    # get the difference of the 2 grayscale images
    (_, diff) = structural_similarity(gray_au_image, gray_sp_image, full=True)
    diff = cv2.medianBlur(diff, 1)
    # make background black and tampered area white
    mask = np.ones_like(diff)
    mask[diff < 0.98] = 1
    mask[diff >= 0.98] = 0
    mask = (mask * 255).astype("uint8")
    cv2.imwrite('mask_ground_truth.png', mask)