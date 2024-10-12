from typing import Any

import numpy as np

from .heatmapcalc import calc_longterm_heatmap


def heatmapcalc(
    detects: list[tuple[Any, Any, Any, Any]], shape: tuple[int, int]
) -> np.ndarray:
    """Wrapper for calc_longterm_heatmap"""
    if len(detects) == 0:
        return np.zeros(shape[:2], dtype=np.int32)
    boxes: list[tuple[int, int, int, int]]
    if not isinstance(detects[0][0], int):
        assert all(hasattr(detect, "box") for detect in detects)
        boxes = [detect.box for detect in detects]  # pyright: ignore[reportAttributeAccessIssue]
    else:
        boxes = detects  # pyright: ignore[reportAssignmentType]
    res = calc_longterm_heatmap(boxes, shape)
    return np.array(res)
