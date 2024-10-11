from typing_extensions import TypedDict, Annotated
from collections import defaultdict
import numpy as np
from torch import Tensor
import pure_cv as vc

class Object(TypedDict):
  score: float
  bbox: vc.BBox

class Preds(TypedDict):
  cell: list[Object]
  pair: list[Object]
  block: list[Object]
  grid: list[Object]

id2label = { 0: 'cell', 1: 'pair', 2: 'block', 3: 'grid' }

def decode(
  *, bboxes: Annotated[Tensor, 'Q *'],
  logits: Annotated[Tensor, 'Q'],
) -> Preds:
  
  m = logits.softmax(-1).max(-1)
  pred_labels = m.indices.detach().cpu().numpy().tolist()
  pred_scores = m.values.detach().cpu().numpy().tolist()
  pred_bboxes = bboxes.detach().cpu().numpy()

  outputs = defaultdict(list)
  for label, score, bbox in zip(pred_labels, pred_scores, pred_bboxes):
    if label in id2label:
      lab = id2label[label]
      outputs[lab].append(Object(score=score, bbox=bbox.reshape(2, 2)))

  return outputs # type: ignore


def grid(preds: Preds) -> vc.BBox | None:
  if len(preds.get('grid') or []) > 0:
    return min(preds['grid'], key=lambda x: x['score'])['bbox']

  
def bboxes(preds: Preds, *, max: int | None = None, min_score: float | None = None) -> vc.BBoxes:
  objs = preds.get('cell') or []
  if min_score is not None:
    objs = [x for x in objs if x['score'] >= min_score]
  if max is not None and len(objs) > max:
    objs = sorted(objs, key=lambda x: x['score'], reverse=True)[:max]

  return np.stack([x['bbox'] for x in objs])