from typing import Annotated
from torch import Tensor
import torch
import numpy as np
from scipy.optimize import linear_sum_assignment
from transformers.models.table_transformer.modeling_table_transformer import generalized_box_iou
from moveread import tatr

def nary_match(
  *, elems: Annotated[Tensor, 'N 2 2'],
  groups: Annotated[Tensor, 'M 2 2'],
  n: int
):
  """Match each group to at most `n` elements
  - Returns `I, J`, s.t. `elems[I]` is matched to `groups[J]` (`J` will likely contain duplicates)
  """
  n_groups = torch.repeat_interleave(groups.reshape(-1, 4), n, dim=0) # [g1, ..., g1, ..., gm, ..., gm] (each repeated n times)
  giou_matrix = generalized_box_iou(elems.reshape(-1, 4), n_groups)
  I, J = linear_sum_assignment(-giou_matrix)
  return I, J//n

def xsort(bboxes: Annotated[Tensor, 'N 2 2']):
  return bboxes[torch.argsort(bboxes[:, 0, 0])]

def ysort(bboxes: Annotated[Tensor, 'N 2 2']):
  return bboxes[torch.argsort(bboxes[:, 0, 1])]


def sort_cells(
  preds: tatr.Preds, *, n_rows: int | None = None,
  min_score: float | None = None, max_cells: int | None = None
) -> Annotated[Tensor, 'N 2 2']:

  def filter_objs(objs: list[tatr.Object]):
    if min_score is not None:
      objs = [x for x in objs if x['score'] >= min_score]
    if max_cells is not None and len(objs) > max_cells:
      objs = sorted(objs, key=lambda x: x['score'], reverse=True)[:max_cells]
    return objs
  
  preds = { k: filter_objs(v) for k, v in preds.items() }
  blocks = torch.stack([torch.from_numpy(b['bbox']) for b in preds['block']])
  blocks = xsort(blocks)

  pairs = torch.stack([torch.from_numpy(b['bbox']) for b in preds['pair']])
  cells = torch.stack([torch.from_numpy(b['bbox']) for b in preds['cell']])

  _, J = nary_match(elems=pairs, groups=blocks, n=n_rows or len(pairs))
  blocked_idcs = [
    np.argwhere(J == j)[:, 0]
    for j in range(len(blocks))
  ]
  blocked_pairs = [ysort(pairs[idcs]) for idcs in blocked_idcs]
  all_pairs = torch.cat(blocked_pairs)

  _, J = nary_match(elems=cells, groups=all_pairs, n=2)
  paired_idcs = [
    np.argwhere(J == j)[:, 0]
    for j in range(len(all_pairs))
  ]
  paired_cells = [xsort(cells[idcs]) for idcs in paired_idcs]
  return torch.cat(paired_cells)