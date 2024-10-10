import torch
import pickle
import numpy as np
import matplotlib.pyplot as plt
from simba.sandbox.pose_estimation.pose_dataset import PoseDataset
from simba.sandbox.pose_estimation.pose_model import PoseModel
from pytorch_lightning.callbacks import ModelCheckpoint
from pytorch_lightning.callbacks.early_stopping import EarlyStopping
from pytorch_lightning import Trainer
from torchvision import transforms
from typing import Optional, Tuple, Dict, List


class PoseTrain():
    def __init__(self,
                 train_dataset: PoseDataset,
                 test_dataset: PoseDataset,
                 val_dataset: PoseDataset,
                 trainer: Trainer,
                 batch_size: Optional[int] = 24,
                 shuffle: Optional[bool] = True):


        train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, drop_last=True, shuffle=shuffle, num_workers=4)
        val_loader = torch.utils.data.DataLoader(val_dataset, batch_size=batch_size, num_workers=4, shuffle=shuffle)
        test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=batch_size, num_workers=4, shuffle=shuffle)

        model = PoseModel(num_joints=7, pos_weight=10.0, detection_thresh=0.25)

        trainer.fit(model=model, train_dataloader=train_loader, val_dataloaders=val_loader)

        pass



train_img_transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((81.1), (55.1))])
train_joint_transform= transforms.Compose([transforms.RandomVerticalFlip(p=0.5), transforms.RandomHorizontalFlip(p=0.5), transforms.RandomRotation(degrees=10)])
train_target_transform = transforms.Compose([transforms.ToTensor()])

test_img_transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((81.1), (55.1))])
test_target_transform = transforms.Compose([transforms.ToTensor()])

train_dataset = PoseDataset(labelme_dir=r'C:\troubleshooting\coco_data\labels\train_', continuous_target=True, continuous_std=0.5, img_transforms=train_img_transform, joint_transform=train_joint_transform, target_transform=train_target_transform)
test_dataset = PoseDataset(labelme_dir=r'C:\troubleshooting\coco_data\labels\test_', continuous_target=True, continuous_std=0.5, img_transforms=test_img_transform, joint_transform=None, target_transform=test_target_transform)
val_dataset = PoseDataset(labelme_dir=r'C:\troubleshooting\coco_data\labels\val_', continuous_target=True, continuous_std=0.5, img_transforms=test_img_transform, joint_transform=None, target_transform=test_target_transform)

best_callback = ModelCheckpoint( save_top_k=1, monitor='mean-l2-dist', mode='min', filename='{epoch}-{step}-{val_loss:.6f}', verbose=True)
early_stop_callback = EarlyStopping( monitor='val_loss', min_delta=0.0, patience=100, verbose=True, mode='min')
epoch_callback = ModelCheckpoint(save_top_k=1, every_n_epochs=1, filename='{epoch}-{step}')
trainer = Trainer(max_epochs=250, accelerator='gpu', devices=[0], precision=16, log_every_n_steps=5, callbacks=[epoch_callback, best_callback, early_stop_callback])

PoseTrain(train_dataset=train_dataset, test_dataset=test_dataset, val_dataset=val_dataset, trainer=trainer)


