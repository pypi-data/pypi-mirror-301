import torch
from tse_motion import get_dinov2
import nibabel as nib
import numpy as np
from PIL import Image
from transformers import AutoImageProcessor
import torchvision.transforms as transforms
import pdb
import torchio as tio
from tqdm import tqdm
image_processor = AutoImageProcessor.from_pretrained(f"facebook/dpt-dinov2-large-nyu")
class ToPILImage:
    def __call__(self, x):
        return transforms.ToPILImage()(x)

class ToTensor:
    def __call__(self, x):
        return transforms.ToTensor()(x)
    
transform = transforms.Compose([
    ToTensor(),
    transforms.CenterCrop((512, 512)),
    ToPILImage(),
])

def process_nii(nii):
    nii = nii.transpose(-1,0,1)
    processeds = []
    for nii_slice in nii:
        nii_slice = (nii_slice / nii_slice.max()) * 255
        nii_slice = np.repeat(nii_slice[:, :, np.newaxis], 3, axis=2)
        nii_slice = nii_slice.astype(np.uint8)
        nii_slice = Image.fromarray(nii_slice.astype(np.uint8), mode='RGB')
        processeds.append(image_processor(transform(nii_slice), return_tensors="pt")['pixel_values'].squeeze())
    return np.stack(processeds)

model = get_dinov2()
with torch.no_grad():
    orig = nib.load('/Users/jinghangli/Developer/tse-rating/test.nii.gz')
    orig_img = nib.load('/Users/jinghangli/Developer/tse-rating/test.nii.gz').get_fdata()
    pred_negs = []
    pred_poses = []
    for img in tqdm(process_nii(orig_img)):
        pred = model(torch.from_numpy(img).unsqueeze(0))['predicted_depth']
        pred_neg = pred[:,0,:,:]
        pred_pos = pred[:,1,:,:]
        pred_neg = torch.nn.functional.interpolate(pred_neg.unsqueeze(1), size=img.shape[1::], mode="bicubic", align_corners=False,)
        pred_neg = tio.CropOrPad(( (orig_img.shape[0], orig_img.shape[1], 1)))(pred_neg.permute(1,2,3,0).detach().cpu()).squeeze()
        pred_pos = torch.nn.functional.interpolate(pred_pos.unsqueeze(1),size=img.shape[1::],mode="bicubic",align_corners=False,)
        pred_pos = tio.CropOrPad(((orig_img.shape[0], orig_img.shape[1], 1)))(pred_pos.permute(1,2,3,0).detach().cpu()).squeeze()
        pred_negs.append(pred_neg)
        pred_poses.append(pred_pos)

    pdb.set_trace()
    pred_pos = torch.stack(pred_poses).permute(1,2,0).numpy()
    pred_neg = torch.stack(pred_negs).permute(1,2,0).numpy()
    orig_img = np.stack((orig_img / orig_img.max()) * 255)

    pred = pred_pos+pred_neg
    pred = pred.flatten()
    pred = 1 - np.dot(pred, (np.zeros_like(pred) + 1e-3)) / (np.linalg.norm(pred) * np.linalg.norm(np.zeros_like(pred) + 1e-3))
    nib.save(nib.Nifti1Image(pred, orig.affine), 'pred.nii.gz')
