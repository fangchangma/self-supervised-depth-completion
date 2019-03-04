# self-supervised-depth-completion

This repo contains the PyTorch implementation of our ICRA'19 paper on ["Self-supervised Sparse-to-Dense:  Self-supervised Depth Completion from LiDAR and Monocular Camera"](https://arxiv.org/pdf/1807.00275.pdf) by [Fangchang Ma](http://www.mit.edu/~fcma/), Guilherme Venturelli Cavalheiro, and [Sertac Karaman](http://karaman.mit.edu/) at MIT. A video demonstration is available on [YouTube](https://youtu.be/bGXfvF261pc).

<p align="center">
	<img src="https://j.gifs.com/rRrOW4.gif" alt="photo not available" height="50%">
</p>

## Contents
0. [Notes](#requirements)
0. [Requirements](#requirements)
0. [Trained Models](#trained-models)
0. [Training and Testing](#training-and-testing)
0. [Questions](#questions)
0. [Citation](#citation)

## Notes
Our network is trained with the KITTI dataset alone, without pretraining on Cityscapes or other similar driving dataset (either synthetic or real). The use of additional data is very likely to further improve the accuracy.

## Requirements
This code was tested with Python 3 and PyTorch 1.0 on Ubuntu 16.04.
- Install [PyTorch](https://pytorch.org/get-started/locally/) on a machine with CUDA GPU.
- The code for self-supervised training requires [OpenCV](http://pytorch.org/) along with the contrib modules. For instance,
```bash
pip3 uninstall opencv-contrib-python
pip3 install opencv-contrib-python==3.4.2.16
```
- Download the [KITTI Depth](http://www.cvlibs.net/datasets/kitti/eval_depth.php?benchmark=depth_completion) Dataset and the corresponding RGB images (script will be released). 
- The code, data and result directory structure is shown as follows
```
.
├── self-supervised-depth-completion
├── data
|   ├── kitti_depth
|   |   ├── train
|   |   ├── val_selection_cropped
|   └── kitti_rgb
|   |   ├── train
|   |   ├── val_selection_cropped
├── results
```

## Trained Models
Download our trained models at http://datasets.lids.mit.edu/self-supervised-depth-completion to a folder of your choice.
- supervised training (i.e., models trained with semi-dense lidar ground truth): http://datasets.lids.mit.edu/self-supervised-depth-completion/supervised/
- self-supervised (i.e., photometric loss + sparse depth loss + smoothness loss): http://datasets.lids.mit.edu/self-supervised-depth-completion/self-supervised/

## Training and testing
A complete list of training options is available with 
```bash
python main.py -h
```
For instance,
```bash
python main.py --train-mode dense -b 1 # train with the KITTI semi-dense annotations and batch size 1
python main.py --train-mode sparse+photo # train with the self-supervised framework, not using ground truth
python main.py --resume [checkpoint-path] # resume previous training
python main.py --evaluate [checkpoint-path] # test the trained model
```

## Questions
Please create a new issue for code-related questions. Pull requests are welcome.

## Citation
If you use our code or method in your work, please cite the following:

	@article{ma2018self,
		title={Self-supervised Sparse-to-Dense: Self-supervised Depth Completion from LiDAR and Monocular Camera},
		author={Ma, Fangchang and Cavalheiro, Guilherme Venturelli and Karaman, Sertac},
		booktitle={ICRA},
		year={2019}
	}
	@article{Ma2017SparseToDense,
		title={Sparse-to-Dense: Depth Prediction from Sparse Depth Samples and a Single Image},
		author={Ma, Fangchang and Karaman, Sertac},
		booktitle={ICRA},
		year={2018}
	}

