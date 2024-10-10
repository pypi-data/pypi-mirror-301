import torchvision.transforms
import torch
from PIL import Image
from typing import List
import torch.nn.functional as F
import cv2 as cv
import numpy as np

class MultiTransform():
    def __init__(self):
        pass

    def __call__(self, input):
        raise NotImplementedError()
    
    def __get_size__(self, imgs):
        if not hasattr(self, 'size'):
            if isinstance(imgs[0], torch.Tensor):
                self.size = (imgs[0].shape[1], imgs[0].shape[2])
            else:
                self.size = (imgs[0].size[1], imgs[0].size[0])
    
    def __reset__(self):
        raise NotImplementedError()

class Compose():
    def __init__(self, children:List[MultiTransform]):
        self.children = children
        pass

    def __call__(self, input):
        result = input
        for c in self.children:
            result = c(result)
        for c in self.children:
            c.__reset__()
        return result
    
    def __reset__(self):
        pass

class Normalize(MultiTransform):
    def __init__(self, mean, std, inplace = False):
        super().__init__()

        self.normalize = torchvision.transforms.Normalize(mean, std, inplace)
        self.__toTensor__ = ToTensor()
        self.__toPILImage__ = ToPILImage()

    def __call__(self, inputs):
        is_tensor = isinstance(inputs[0], torch.Tensor)
        if not is_tensor:
            inputs = self.__toTensor__(inputs)
        inputs = torch.stack(inputs)

        results = []
        for res in self.normalize(inputs):
            results.append(res)

        if not is_tensor:
            results = self.__toPILImage__(results)
        return results
    
    def __reset__(self):
        pass
    
class ToTensor(MultiTransform):
    def __init__(self):
        super().__init__()

        self.toTensor = torchvision.transforms.ToTensor()

    def __call__(self, images:Image):
        results = []
        for img in images:
            result = self.toTensor(img)
            results.append(result)
        return results
    
    def __reset__(self):
        pass
    
class CenterCrop(MultiTransform):
    def __init__(self, max_scale = 2):
        super().__init__()

        if max_scale < 1:
            raise Exception(f'max_scale expected to be greater than 1. Actual value is {max_scale})')
        self.max_scale = max_scale

        self.__toTensor__ = ToTensor()
        self.__toPILImage__ = ToPILImage()

        self.__reset__()

    def __call__(self, imgs):
        self.__get_size__(imgs)
    
        results = []

        is_tensor = isinstance(imgs[0], torch.Tensor)
        if not is_tensor:
            imgs = self.__toTensor__(imgs)
        
        for img in imgs:
            img_before = img.permute(1, 2, 0).numpy()

            w, h = self.size[1], self.size[0]
            new_w, new_h = int(np.round(w * self.__scale__)), int(np.round(h * self.__scale__))
            img_after = cv.resize(img_before, (new_w, new_h))

            cx, cy = new_w // 2, new_h // 2
            result = img_after[cy - h // 2: cy + h // 2, cx - w // 2: cx + w // 2]
            result = torch.tensor(result, dtype=img.dtype).permute(2, 0, 1)

            results.append(result)

        if not is_tensor:
            results = self.__toPILImage__(results)
            
        return results
    
    def __reset__(self):
        self.__scale__ = 1. + np.random.random() * (self.max_scale - 1.)

class RandomCrop(MultiTransform):
    def __init__(self, max_scale = 2):
        super().__init__()

        if max_scale < 1:
            raise Exception(f'max_scale expected to be greater than 1. Actual value is {max_scale})')
        self.max_scale = max_scale

        self.__toCVImage__ = ToCVImage()
        self.__toTensor__ = ToTensor()
        self.__toPILImage__ = ToPILImage()

        self.__reset__()

    def __call__(self, imgs):
        self.__get_size__(imgs)
    
        results = []

        is_tensor = isinstance(imgs[0], torch.Tensor)
        if not is_tensor:
            imgs = self.__toTensor__(imgs)
        
        #imgs = self.__toCVImage__(imgs)

        for img in imgs:
            img_before = img.permute(1, 2, 0).numpy()

            w, h = self.size[1], self.size[0]
            new_w, new_h = int(np.round(w * self.__scale__)), int(np.round(h * self.__scale__))
            img_after = cv.resize(img_before, (new_w, new_h))

            img_after = torch.tensor(img_after, dtype=img.dtype).permute(2, 0, 1)
            result = img_after[:, self.__sy__:self.__sy__ + h, self.__sx__:self.__sx__ + w]

            results.append(result)

        if not is_tensor:
            results = self.__toPILImage__(results)
            
        return results
    
    def __reset__(self):
        self.__scale__ = 1. + np.random.random() * (self.max_scale - 1.)
        if not hasattr(self, 'size'):
            self.__sx__ = 0
            self.__sy__ = 0
        else:
            w, h = self.size[1], self.size[0]
            new_w, new_h = self.__scale__ * self.size[1], self.__scale__ * self.size[0]
            self.__sx__ = int(np.round(np.random.random() * (new_w - w)))
            self.__sy__ = int(np.round(np.random.random () * (new_h - h)))

class Rotate(MultiTransform):
    def __init__(self, max_angle = 180, auto_scale:bool = True):
        super().__init__()

        self.max_angle = max_angle
        self.auto_scale = auto_scale

        self.__toTensor__ = ToTensor()
        self.__toPILImage__ = ToPILImage()

    def __call__(self, imgs):
        self.__get_size__(imgs)
        self.__reset__()
    
        results = []

        is_tensor = isinstance(imgs[0], torch.Tensor)
        if not is_tensor:
            imgs = self.__toTensor__(imgs)

        for img in imgs:
            img_before = img.permute(1, 2, 0).numpy()

            w, h = self.size[1], self.size[0]
            mat = cv.getRotationMatrix2D((w // 2, h // 2), self.__angle__, self.__scale__)
            img_after = cv.warpAffine(img_before, mat, (w, h))

            result = torch.tensor(img_after, dtype=img.dtype).permute(2, 0, 1)

            results.append(result)

        if not is_tensor:
            results = self.__toPILImage__(results)
            
        return results
    
    def __reset__(self):
        self.__angle__ = -self.max_angle + 2 * np.random.random() * self.max_angle

        w, h = self.size[1], self.size[0]
        t1 = np.sin(self.__angle__)
        new_w = w + np.abs(np.sin(self.__angle__ / 180 * np.pi) * w)
        new_h = h + np.abs(np.sin(self.__angle__ / 180 * np.pi) * h)

        self.__scale__ = 1.03 * np.max([new_w / w, new_h / h]) if self.auto_scale else 1.

class ToNumpy(MultiTransform):
    def __init__(self):
        super().__init__()

    def __call__(self, tensor:torch.Tensor):
        result = tensor.numpy()
        return result
    
    def __reset__(self):
        pass

class ToCVImage(MultiTransform):
    def __init__(self):
        super().__init__()

        self.__toTensor__ = ToTensor()

    def __call__(self, inputs) -> List[np.array]:
        is_tensor = isinstance(inputs[0], torch.Tensor)
        if not is_tensor:
            inputs = self.__toTensor__(inputs)
        results = []
        for img in inputs:
            result = img.permute(1, 2, 0).numpy()
            results.append(result)
        return results
    
    def __reset__(self):
        pass

class ToPILImage(MultiTransform):
    def __init__(self):
        super().__init__()

        self.__toPILImage__ = torchvision.transforms.ToPILImage()

    def __call__(self, tensor:torch.Tensor):
        results = []
        for img in tensor:
            result = self.__toPILImage__(img)
            results.append(result)
        return results
    
    def __reset__(self):
        pass

class BGR2RGB(MultiTransform):
    def __init__(self):
        super().__init__()

        self.__toTensor__ = ToTensor()
        self.__toPILImage__ = ToPILImage()

    def __call__(self, inputs):
        is_tensor = isinstance(inputs[0], torch.Tensor)
        if not is_tensor:
            inputs = self.__toTensor__(inputs)

        results = []
        for input in inputs:
            result = torch.flip(input, (0,))
            results.append(result)

        if not is_tensor:
            results = self.__toPILImage__(results)
        return results
    
    def __reset__(self):
        pass

class RGB2BGR(BGR2RGB):
    pass


if __name__ == '__main__':
    transforms = Compose([
        ToTensor(),
        #RandomCrop(max_scale=1.1),
        Normalize(0, 1),
        Rotate(max_angle=5, auto_scale=True),
        RGB2BGR(),
        ToCVImage(),
    ])

    imgs = [
        Image.open('/Users/schulzr/Library/CloudStorage/OneDrive-Persönlich/Datasets/tuc-actionpredictiondataset1/sequences/realsense/train/A000C000S000SEQ000/C000F00000_color.jpg'),
        Image.open('/Users/schulzr/Library/CloudStorage/OneDrive-Persönlich/Datasets/tuc-actionpredictiondataset1/sequences/realsense/train/A000C000S000SEQ000/C000F00001_color.jpg'),
        Image.open('/Users/schulzr/Library/CloudStorage/OneDrive-Persönlich/Datasets/tuc-actionpredictiondataset1/sequences/realsense/train/A000C000S000SEQ000/C000F00002_color.jpg'),
        Image.open('/Users/schulzr/Library/CloudStorage/OneDrive-Persönlich/Datasets/tuc-actionpredictiondataset1/sequences/realsense/train/A000C000S000SEQ000/C000F00003_color.jpg'),
        Image.open('/Users/schulzr/Library/CloudStorage/OneDrive-Persönlich/Datasets/tuc-actionpredictiondataset1/sequences/realsense/train/A000C000S000SEQ000/C000F00004_color.jpg'),
        Image.open('/Users/schulzr/Library/CloudStorage/OneDrive-Persönlich/Datasets/tuc-actionpredictiondataset1/sequences/realsense/train/A000C000S000SEQ000/C000F00005_color.jpg'),
        Image.open('/Users/schulzr/Library/CloudStorage/OneDrive-Persönlich/Datasets/tuc-actionpredictiondataset1/sequences/realsense/train/A000C000S000SEQ000/C000F00006_color.jpg'),
    ]

    for i in range(10):
        results = transforms(imgs)
        for img, result in zip(imgs, results):
            cv.imshow('img', np.asarray(img))
            cv.imshow('result', result)
            cv.waitKey()
    pass