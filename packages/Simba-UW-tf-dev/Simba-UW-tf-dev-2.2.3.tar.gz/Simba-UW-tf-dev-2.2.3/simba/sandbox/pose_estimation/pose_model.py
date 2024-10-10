import torch
import pytorch_lightning as pl
from torchmetrics.metric import Metric
from torchvision.models.segmentation import lraspp_mobilenet_v3_large
from torchvision.models.mobilenetv3 import MobileNetV3
import torchvision.models as models
from typing import Optional

model = models.mobilenet_v3_large(pretrained=True)


class PoseModel(pl.LightningModule):
    '''
    Pose estimation model. Relies on a pretrained MobileNetV3 backbone.

    Args:
      num_joints: number of joints in the pose estimation model.
      pos_weight: weight for positive examples in binary cross entropy loss.
      detection_thresh: threshold for joint detection.
    '''

    def __init__(self,
                 num_joints: Optional[int] = 7,
                 pos_weight: Optional[float] = 1.0,
                 detection_thresh: Optional[float] = 0.5):

        super().__init__()

        # Set up pretrained model.
        self.model = lraspp_mobilenet_v3_large(num_classes=num_joints,
                                               pretrained=True,
                                               progress=False)

        # Set up performance metrics.
        self.loss = PoseLoss(pos_weight=pos_weight)
        self.pose_accuracy = PoseAccuracy(num_joints, detection_thresh)

    def forward(self, img):
        return self.model(img)['out']

    def training_step(self, batch, batch_idx):
        # Unpack batch.
        img = batch['img']
        target = batch['target']
        # coordinates = batch['coordinates']

        # Calculate loss.
        pred = self.model(img)['out']
        loss = self.loss(pred, target)
        self.log('train_loss', loss)
        return loss

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer,
                                                                T_max=self.trainer.max_epochs,
                                                                eta_min=1e-6,
                                                                verbose=False)
        scheduler_config = {
            'scheduler': scheduler,
            'interval': 'epoch',
        }
        return {
            'optimizer': optimizer,
            'lr_scheduler': scheduler_config
        }

    def validation_step(self, val_batch, batch_idx):
        # Unpack batch.
        img = val_batch['img']
        target = val_batch['target']
        coordinates = val_batch['coordinates']

        # Calculate validation loss.
        pred = self.model(img)['out']
        loss = self.loss(pred, target)
        self.log('val_loss', loss, prog_bar=True)

        # Calculate validation accuracy.
        self.pose_accuracy.update(pred, coordinates)

    def on_validation_epoch_end(self):
        val_accuracy = self.pose_accuracy.compute()
        self.pose_accuracy.reset()

        # Calculate joint detection accuracy.
        for i in range(len(val_accuracy['detection_acc'])):
            self.log(f'joint-{i}-acc', val_accuracy['detection_acc'][i], prog_bar=False)
        self.log('mean-detection-acc', val_accuracy['detection_acc'].mean(), prog_bar=True)

        # Calculate joint distances.
        for i in range(len(val_accuracy['l2_distance'])):
            self.log(f'joint-{i}-dist', val_accuracy['l2_distance'][i], prog_bar=True)
        self.log('mean-l2-dist', val_accuracy['l2_distance'].mean(), prog_bar=True)


class PoseLoss(torch.nn.Module):
    '''
    Loss function for training pose estimation model. We could instead use the
    built-in BCEWithLogitsLoss, but this makes the calculation more readable.

    Args:
      pos_weight: weight for positive examples in binary cross entropy loss.
    '''

    def __init__(self, pos_weight=1):
        super().__init__()
        self.pos_weight = pos_weight

    def forward(self, pred, target):
        prob = torch.nn.functional.logsigmoid(pred)
        non_prob = torch.nn.functional.logsigmoid(1 - pred)
        return (
            - self.pos_weight * (prob * target)
            - (non_prob * (1 - target))
        ).mean()


class PoseAccuracy(Metric):
    '''
    Pose estimation accuracy metric.

    Args:
      num_joints: number of joints in the pose estimation model.
      detection_thresh: threshold for joint detection.
    '''
    is_differentiable = False
    higher_is_better = True

    def __init__(self, num_joints, detection_thresh):
        super().__init__()
        self.detection_thresh = detection_thresh
        # TODO can we initialize these all as scalars?
        self.add_state('present_counts', default=torch.zeros(num_joints), dist_reduce_fx='sum')
        self.add_state('correct_detections', default=torch.zeros(num_joints), dist_reduce_fx='sum')
        self.add_state('l2_dist', default=torch.zeros(num_joints), dist_reduce_fx='sum')
        self.add_state('total_count', default=torch.tensor(0.0), dist_reduce_fx='sum')

    def update(self, pred, coordinates):
        # Prepare predictions and max values.
        pred = pred.sigmoid()
        max_val = pred.max(dim=3, keepdim=True).values.max(dim=2, keepdim=True).values
        self.total_count += len(pred)

        # Calculate detection accuracies (whether present joints are detected).
        present = (coordinates[:, ::2] != -1)
        detected = (max_val[:, :, 0, 0] > self.detection_thresh)
        correct_detections = (present == detected).float().sum(dim=0)
        self.correct_detections += correct_detections
        self.present_counts += present.float().sum(dim=0)

        # Calculate distances between true and predicted joint locations.
        y = torch.zeros(pred.shape[0], pred.shape[1]).type_as(pred)
        x = torch.zeros(pred.shape[0], pred.shape[1]).type_as(pred)
        for i in range(len(pred)):
            for j in range(pred.shape[1]):
                # Find location with maximum value for this image/joint.
                y_pred, x_pred = (pred[i, j] == max_val[i, j, 0, 0]).nonzero()[0]
                y[i, j] = y_pred
                x[i, j] = x_pred
        y_true = coordinates[:, ::2]
        x_true = coordinates[:, 1::2]
        dist = ((y - y_true) ** 2 + (x - x_true) ** 2) ** 0.5
        self.l2_dist += (dist * present.float()).sum(dim=0)

    def compute(self):
        detection_acc = self.correct_detections / self.total_count
        l2_dist = self.l2_dist / self.present_counts
        return {
            'detection_acc': detection_acc,
            'l2_distance': l2_dist
        }

