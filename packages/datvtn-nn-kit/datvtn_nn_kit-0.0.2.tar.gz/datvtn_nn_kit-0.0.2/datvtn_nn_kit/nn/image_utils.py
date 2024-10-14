import cv2
import math
import numpy as np
import torch
from torchvision.utils import make_grid
from numpy.typing import NDArray
from typing import List, Tuple, Union, Any


def img_to_tensor(imgs: Union[List[NDArray[Any]], NDArray[Any]], bgr2rgb: bool = True, float32: bool = True) -> Union[List[torch.Tensor], torch.Tensor]:
    """Convert numpy array to torch tensor.

    Args:
        imgs (list[ndarray] | ndarray): Input images.
        bgr2rgb (bool): Whether to convert BGR to RGB format. Default is True.
        float32 (bool): Whether to convert image to float32. Default is True.

    Returns:
        list[tensor] | tensor: Converted tensor images. If a single image is
        passed, a tensor is returned.
    """
    def _to_tensor(img: NDArray[Any], bgr2rgb: bool, float32: bool) -> torch.Tensor:
        if img.shape[2] == 3 and bgr2rgb:
            if img.dtype == 'float64':
                img = img.astype('float32')
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = torch.from_numpy(img.transpose(2, 0, 1))
        if float32:
            img = img.float()
        return img

    if isinstance(imgs, list):
        return [_to_tensor(img, bgr2rgb, float32) for img in imgs]
    else:
        return _to_tensor(imgs, bgr2rgb, float32)


def tensor_to_img(tensor: Union[torch.Tensor, List[torch.Tensor]], rgb2bgr: bool = True, out_type: Any = np.uint8, min_max: Tuple[int, int] = (0, 1)) -> Union[NDArray[Any], List[NDArray[Any]]]:
    """Convert torch tensor(s) to numpy image(s).

    Args:
        tensor (Tensor or list[Tensor]): Input tensor(s) in the shape of
            (B x 3/1 x H x W) or (3/1 x H x W) or (H x W).
        rgb2bgr (bool): Whether to convert RGB to BGR. Default is True.
        out_type (numpy type): Output image type (e.g. np.uint8).
        min_max (tuple[int]): Min and max values for clamping. Default is (0, 1).

    Returns:
        ndarray or list[ndarray]: Output image(s).
    """
    if not (torch.is_tensor(tensor) or (isinstance(tensor, list) and all(torch.is_tensor(t) for t in tensor))):
        raise TypeError(f'Expected tensor or list of tensors, but got {type(tensor)}.')

    if torch.is_tensor(tensor):
        tensor = [tensor]

    result = []
    for _tensor in tensor:
        _tensor = _tensor.squeeze(0).float().detach().cpu().clamp_(*min_max)
        _tensor = (_tensor - min_max[0]) / (min_max[1] - min_max[0])

        n_dim = _tensor.dim()
        if n_dim == 4:
            img_np = make_grid(_tensor, nrow=int(math.sqrt(_tensor.size(0))), normalize=False).numpy()
            img_np = img_np.transpose(1, 2, 0)
            if rgb2bgr:
                img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        elif n_dim == 3:
            img_np = _tensor.numpy().transpose(1, 2, 0)
            if img_np.shape[2] == 1:  # grayscale image
                img_np = np.squeeze(img_np, axis=2)
            elif rgb2bgr:
                img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        elif n_dim == 2:
            img_np = _tensor.numpy()
        else:
            raise TypeError(f'Expected tensor of dimension 2, 3, or 4, but got {n_dim}.')
        
        if out_type == np.uint8:
            img_np = (img_np * 255.0).round().astype(out_type)
        result.append(img_np)

    return result[0] if len(result) == 1 else result


def tensor_to_img_fast(tensor: torch.Tensor, rgb2bgr: bool = True, min_max: Tuple[int, int] = (0, 1)) -> NDArray[Any]:
    """Faster version of tensor_to_img. Supports single tensor input.

    Args:
        tensor (Tensor): Torch tensor with shape (1, c, h, w).
        rgb2bgr (bool): Whether to convert RGB to BGR. Default is True.
        min_max (tuple[int]): Min and max values for clamping.

    Returns:
        ndarray: Converted image.
    """
    output = tensor.squeeze(0).detach().clamp_(*min_max).permute(1, 2, 0)
    output = (output - min_max[0]) / (min_max[1] - min_max[0]) * 255
    output = output.type(torch.uint8).cpu().numpy()

    if rgb2bgr:
        output = cv2.cvtColor(output, cv2.COLOR_RGB2BGR)
    return output


def img_from_bytes(content: bytes, flag: str = 'color', float32: bool = False) -> NDArray[Any]:
    """Read an image from bytes content.

    Args:
        content (bytes): Image bytes.
        flag (str): Color mode for reading image ('color', 'grayscale', 'unchanged').
        float32 (bool): Whether to convert to float32. If True, scales values to [0, 1].

    Returns:
        ndarray: Loaded image as numpy array.
    """
    img_np = np.frombuffer(content, np.uint8)
    imread_flags = {'color': cv2.IMREAD_COLOR, 'grayscale': cv2.IMREAD_GRAYSCALE, 'unchanged': cv2.IMREAD_UNCHANGED}
    img = cv2.imdecode(img_np, imread_flags[flag])
    
    if float32:
        img = img.astype(np.float32) / 255.
    
    return img
