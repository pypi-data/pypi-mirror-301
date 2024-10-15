import numpy as np
import cv2

class ImageProcess:
    '''
    图像处理类
    '''
    def __init__(self, img_path, dst_width, dst_height) -> None:
        self.img_path = img_path
        self.dst_width = dst_width
        self.dst_height = dst_height
    
    def preprocess(self):
        '''
        返回处理后的图像以及仿射变换矩阵M
        '''
        img = cv2.imread(self.img_path)
        scale = min((self.dst_width / img.shape[1]), (self.dst_height / img.shape[0]))
        ox = (-scale * img.shape[1] + self.dst_width)  / 2
        oy = (-scale * img.shape[0] + self.dst_height) / 2
        M  = np.array([
            [scale, 0, ox],
            [0, scale, oy]
        ], dtype=np.float32)
        img_pre = cv2.warpAffine(img, M, dsize=[self.dst_width, self.dst_height], flags=cv2.INTER_LINEAR,
                            borderMode=cv2.BORDER_CONSTANT, borderValue=(114,114,114))
        return img_pre, M
