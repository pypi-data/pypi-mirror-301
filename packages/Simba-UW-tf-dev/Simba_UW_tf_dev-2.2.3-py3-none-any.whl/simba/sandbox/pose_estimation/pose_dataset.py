import os

import pandas as pd
import torch
import pickle
import numpy as np
from typing import Union, Optional, Tuple, Any, Dict
from torchvision import transforms

from simba.utils.checks import check_if_dir_exists
from simba.utils.read_write import find_files_of_filetypes_in_directory
from simba.utils.enums import Formats, Options
from simba.mixins.image_mixin import ImageMixin
from simba.third_party_label_appenders.converters import labelme_to_df, _b64_dict_to_imgs



def get_continuous_target_arr(imgs: np.ndarray,
                              annotation_data: pd.DataFrame,
                              continuous_std: float):

    variance = continuous_std ** 2
    coord_arr = annotation_data.fillna(-1).values.astype(np.int32)  # Y and X change
    coord_arr = coord_arr.reshape(-1, int(coord_arr.shape[-1] / 2), 2)
    n, h, w, _ = imgs.shape
    targets = np.zeros((n, h, w, coord_arr.shape[1]), dtype=np.float32)
    y_arr = np.tile(np.arange(h), (w, 1)).T
    x_arr = np.tile(np.arange(w), (h, 1))
    for img_id in range(coord_arr.shape[0]):
        for bp_id in range(coord_arr[img_id].shape[0]):
            x, y = coord_arr[img_id][bp_id][0], coord_arr[img_id][bp_id][1]
            if x < 0 or x == np.nan:
                continue
            else:
                z = (y_arr - y) ** 2 + (x_arr - x) ** 2
                z = np.exp(- 0.5 * z / variance)
                targets[img_id, :, :, bp_id] = z
    return targets

def get_discrete_target_arr(imgs: np.ndarray,
                            annotation_data: pd.DataFrame):

    coord_arr = annotation_data.values.astype(np.int32)  # Y and X change
    coord_arr = coord_arr.reshape(-1, int(coord_arr.shape[-1] / 2), 2)
    n, h, w, _ = imgs.shape
    targets = np.zeros((n, h, w, coord_arr.shape[1]), dtype=np.float32)
    for img_id in range(coord_arr.shape[0]):
        for bp_id in range(coord_arr[img_id].shape[0]):
            x, y = coord_arr[img_id][bp_id][0], coord_arr[img_id][bp_id][1]
            if x < 0 or x == np.nan:
                continue
            else:
                targets[img_id, y, x, bp_id] = 1
    return targets




def get_img_meta_data(imgs: np.ndarray) -> Dict[str, Any]:

    if imgs.ndim == 4:
        m_r, std_r = np.mean(imgs[:, :, :, 0]), np.std(imgs[:, :, :, 0])
        m_g, std_g = np.mean(imgs[:, :, :, 1]), np.std(imgs[:, :, :, 1])
        m_b, std_b = np.mean(imgs[:, :, :, 2]), np.std(imgs[:, :, :, 2])

    return {'image_cnt': imgs.shape[0],
            'img_height': imgs.shape[1],
            'img_width': imgs.shape[2],
            'mean_red': m_r,
            'mean_green': m_g,
            'mean_blue': m_b,
            'std_red': std_r,
            'std_green': std_g,
            'std_blue': std_b}



class PoseDataset(torch.utils.data.Dataset):

    def __init__(self,
                 labelme_dir: Optional[Union[str, os.PathLike]] = None,
                 continuous_target: Optional[bool] = True,
                 continuous_std: Optional[float] = 0.5,
                 img_transforms: Optional[Union[transforms.Compose, None]] = None,
                 target_transform: Optional[Union[transforms.Compose, None]] = transforms.ToTensor(),
                 joint_transform: Optional[Union[transforms.Compose, None]] = None):

        if labelme_dir is not None:
            annotation_data = labelme_to_df(labelme_dir=labelme_dir)
            self.imgs = _b64_dict_to_imgs(x=annotation_data.set_index('image_name')['image'].to_dict())
            self.imgs = np.stack(self.imgs.values())
            annotation_data = annotation_data.drop(['image_name', 'image'], axis=1)
        else:
            return
        if continuous_target:
            self.targets = get_continuous_target_arr(imgs=self.imgs, annotation_data=annotation_data, continuous_std=continuous_std)
        else:
            self.targets = get_discrete_target_arr(imgs=self.imgs, annotation_data=annotation_data)

        self.img_transforms = img_transforms
        self.target_transform = target_transform
        self.joint_transform = joint_transform
        self.meta_data = get_img_meta_data(imgs=self.imgs)

    def __len__(self):
        return self.imgs.shape[0]

    def __getitem__(self, index):
        img = self.imgs[index]
        target = self.targets[index]
        coords = self.coordinates_arr[index]
        if self.img_transforms is not None:
            img = self.img_transforms(img)
        if self.target_transform is not None:
            target = self.target_transform(target)
        if self.joint_transform is not None:
            concat = torch.cat([img, target], dim=0)
            concat = self.joint_transform(concat)
            img = concat[:3]
            target = concat[3:]
        return {'img': img, 'target': target, 'coordinates': coords}

# img_transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((81.1), (55.1))])
# joint_transform= transforms.Compose([transforms.RandomVerticalFlip(p=0.5), transforms.RandomHorizontalFlip(p=0.5), transforms.RandomRotation(degrees=10)])
# target_transform = transforms.Compose([transforms.ToTensor()])
# PoseDataset(labelme_dir=r'C:\troubleshooting\coco_data\labels\test_2', continuous_target=True, continuous_std=0.5, img_transforms=img_transform, joint_transform=joint_transform, target_transform=target_transform)



