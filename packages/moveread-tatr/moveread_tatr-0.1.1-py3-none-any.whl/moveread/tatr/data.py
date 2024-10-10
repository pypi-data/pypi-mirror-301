from typing_extensions import Annotated
import torch
import numpy as np
import pure_cv as vc
from torchvision import transforms

normalize = transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])

def img2tensor(img: vc.Img):
  """Convert an image to a normalized tensor. `img` must already be resized."""
  return torch.tensor(img).float().permute(2, 0, 1)

def preprocess(img: vc.Img) -> torch.Tensor:
  img = vc.descale_h(img, 1024)
  return normalize(img2tensor(img) / 255.0)

def pad_bbox(bbox, *, l=0.05, t=0.05, r=0.05, b=0.05):
  (x0, y0), (x1, y1) = bbox
  w, h = x1-x0, y1-y0
  top = y0 - t*h
  left = x0 - l*w
  bottom = y1 + b*h
  right = x1 + r*w
  return np.array([[left, top], [right, bottom]])

def ensure_bboxes(bboxes: Annotated[torch.Tensor, 'Q 4']) -> Annotated[torch.Tensor, 'Q 4']:
  """Ensure boxes are in valid format
  - `bboxes = [(x1, y1, x2, y2), ...]`
  - Output boxes ensure `x1 <= x2` and `y1 <= y2`
  """
  return torch.cat([bboxes[:, :2], torch.max(bboxes[:, 2:], bboxes[:, :2])], dim=1)