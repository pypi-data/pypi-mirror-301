import torch 

from TorchImager import Window

t = torch.rand(3, 256, 256)

with Window(256, 256, "color") as window:
	window.show(t)