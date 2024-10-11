from typing_extensions import Annotated, NamedTuple
from transformers.models.table_transformer.modeling_table_transformer import (
  TableTransformerConfig,
  Seq2SeqModelOutput,
  TableTransformerForObjectDetection
)
import torch
from torch import Tensor
import pure_cv as vc
import numpy as np
from .config import config
from moveread import tatr

class Output(NamedTuple):
  bboxes: Annotated[Tensor, 'Q 4']
  logits: Annotated[Tensor, 'Q']

class TableDetector(TableTransformerForObjectDetection):

  def __init__(self, config: TableTransformerConfig = config):
    super().__init__(config)
    self.config = config
    self.eval()

  def bboxes(self, output: Seq2SeqModelOutput) -> Annotated[Tensor, 'Q 4']:
    z: Tensor = self.bbox_predictor(output.last_hidden_state)
    return tatr.ensure_bboxes(z.sigmoid()[0])

  def class_logits(self, output: Seq2SeqModelOutput) -> Annotated[Tensor, 'Q']:
    return self.class_labels_classifier(output.last_hidden_state)[0]

  def predict(self, img: vc.Img) -> Output:
    x = tatr.preprocess(img)
    out = self.model(x[None, ...].to(self.device))
    return Output(bboxes=self.bboxes(out), logits=self.class_logits(out))

  def autocrop(self, img: vc.Img) -> Output:
    h, w = img.shape[:2]
    out = self.predict(img)
    preds = tatr.decode(bboxes=out.bboxes, logits=out.logits)
    
    if (grid := tatr.grid(preds)) is None:
      return out

    (x1, y1), (x2, y2) = (tatr.pad_bbox(grid).clip(0, 1) * [w, h]).astype(int)
    img2 = img[y1:y2, x1:x2]
    out = self.predict(img2)
    
    h2, w2 = img2.shape[:2]
    s = torch.tensor([w2, h2])
    t = torch.tensor([x1, y1])

    bboxes2 = out.bboxes.reshape(-1, 2, 2)
    bboxes2 = (s*bboxes2 + t) / torch.tensor([w, h]) # relative w.r.t. the original image
    bboxes2 = bboxes2.reshape(-1, 4)
    return Output(bboxes=bboxes2, logits=out.logits)
  
  def detect(
    self, img: vc.Img, *, autocrop: bool = True, n_rows: int | None = None,
    min_score: float | None = None, max_cells: int | None = None
  ) -> vc.Contours:
    out = self.autocrop(img) if autocrop else self.predict(img)
    preds = tatr.decode(bboxes=out.bboxes, logits=out.logits)
    cells = tatr.sort_cells(preds, n_rows=n_rows, min_score=min_score, max_cells=max_cells)
    return vc.bbox2contour(cells)
      
  # def detect(
  #   self, img: vc.Img, *, autocrop: bool = True,
  #   max: int | None = None, min_score: float | None = None
  # ) -> vc.Contours:
    
  #   h, w = img.shape[:2]
  #   out = self.predict(img)
  #   preds = tatr.decode(bboxes=out.bboxes, logits=out.logits)
    
  #   if autocrop and (grid := tatr.grid(preds)) is not None:
  #     (x1, y1), (x2, y2) = (tatr.pad_bbox(grid).clip(0, 1) * [w, h]).astype(int)
  #     img2 = img[y1:y2, x1:x2]
  #     cnts = self.detect(img2, autocrop=False)
      
  #     h2, w2 = img2.shape[:2]
  #     s = np.array([w2, h2])
  #     t = np.array([x1, y1])
  #     return (s*cnts + t) / [w, h] # relative w.r.t. the original image
      
  #   else:
  #     bboxes = tatr.bboxes(preds, max=max, min_score=min_score)
  #     return vc.bbox2contour(bboxes)


  def load(self, weights_path: str):
    try:
      self.load_state_dict(torch.load(weights_path, weights_only=True))
    except:
      print('Error loading weights. Trying to load on the CPU...')
      self.load_state_dict(torch.load(weights_path, weights_only=True, map_location='cpu'))