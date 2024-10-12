from skimage.metrics import structural_similarity as ssim_func
from .ssim import _3d_to_4d_tensors
import torch
import numpy as np

def _tensor2ndarray(X:torch.Tensor):
    r""" PyTorch format to OpenCV format ()
    Args:
        X (torch.Tensor): (B,C,H,W)

    Returns:
        X (torch.Tensor): 
            if C == 1: (B, H, W)
            if C > 1: (B, H, W, C)
    """
    assert len(X.size()) == 4

    X = X.permute(0, 2, 3, 1) # (B, C, H, W) -> (B, H, W, C)
    if X.size(-1) == 1:
        X = X.squeeze(-1)
    
    X = X.numpy().astype(np.float64)
    return X

def ssim(X:torch.Tensor, Y:torch.Tensor, addition_func=None, data_range=1):
    r""" interface of ssim
    Args:
        X (torch.Tensor): a batch of images, (N,C,H,W)
        Y (torch.Tensor): a batch of images, (N,C,H,W)
        data_range (float or int, optional): value range of input images. (usually 1.0 or 255)

    Returns:
        torch.Tensor: ssim results
    """
    assert X.size() == Y.size()
    X = X.cpu()
    Y = Y.cpu()

    X = _3d_to_4d_tensors(X)
    Y = _3d_to_4d_tensors(Y)

    X = _tensor2ndarray(X)
    Y = _tensor2ndarray(Y)

    if addition_func is not None:
        X = addition_func(X)
        Y = addition_func(Y)

    the_ssim = torch.tensor([float(ssim_func(X, Y, data_range=data_range, channel_axis=0))])

    return the_ssim