import cv2
import numpy as np
import matplotlib.pyplot as plt
import torch

# 讀取圖片並轉換為灰度圖
image = cv2.imread('images.jpeg', 0)  # 替換為你的圖片路徑
image = cv2.resize(image, (256, 256))    # 統一尺寸

def opencv_fft_demo(img):
    # OpenCV FFT處理
    # 1. 傅里葉變換
    dft = cv2.dft(np.float32(img), flags=cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)
    magnitude = cv2.magnitude(dft_shift[:,:,0], dft_shift[:,:,1])
    magnitude_spectrum = 20 * np.log(magnitude + 1e-6)  # 對數轉換
    
    # 2. 逆傅里葉變換
    idft_shift = np.fft.ifftshift(dft_shift)
    img_back = cv2.idft(idft_shift, flags=cv2.DFT_REAL_OUTPUT)
    img_back = cv2.normalize(img_back, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    
    return magnitude_spectrum, img_back

def pytorch_fft_demo(img):
    # PyTorch FFT處理
    # 轉換為Tensor
    img_tensor = torch.from_numpy(img).float()
    
    # 1. 傅里葉變換
    fft = torch.fft.fft2(img_tensor)
    fft_shift = torch.roll(fft, shifts=(img.shape[0]//2, img.shape[1]//2), dims=(0, 1))
    magnitude = torch.abs(fft_shift)
    magnitude_spectrum = 20 * torch.log(magnitude + 1e-6)  # 對數轉換
    
    # 2. 逆傅里葉變換
    ifft_shift = torch.roll(fft_shift, shifts=(-img.shape[0]//2, -img.shape[1]//2), dims=(0, 1))
    img_back = torch.fft.ifft2(ifft_shift).real
    img_back = img_back.numpy()
    img_back = cv2.normalize(img_back, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    
    return magnitude_spectrum.numpy(), img_back

# 執行處理
opencv_spec, opencv_back = opencv_fft_demo(image)
pytorch_spec, pytorch_back = pytorch_fft_demo(image)

# 繪製結果
plt.figure(figsize=(12, 8))

# 原始圖像
plt.subplot(2, 3, 1)
plt.imshow(image, cmap='gray')
plt.title('Original Image')
plt.axis('off')

# OpenCV處理結果
plt.subplot(2, 3, 2)
plt.imshow(opencv_spec, cmap='gray')
plt.title('OpenCV FFT Spectrum')
plt.axis('off')

plt.subplot(2, 3, 3)
plt.imshow(opencv_back, cmap='gray')
plt.title('OpenCV Reconstructed')
plt.axis('off')

# PyTorch處理結果
plt.subplot(2, 3, 5)
plt.imshow(pytorch_spec, cmap='gray')
plt.title('PyTorch FFT Spectrum')
plt.axis('off')

plt.subplot(2, 3, 6)
plt.imshow(pytorch_back, cmap='gray')
plt.title('PyTorch Reconstructed')
plt.axis('off')

plt.tight_layout()
plt.show()