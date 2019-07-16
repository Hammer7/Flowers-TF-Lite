# Recognize Flowers using Transfer Learning

Original Code can be found at https://colab.sandbox.google.com/github/tensorflow/examples/blob/master/community/en/flowers_tf_lite.ipynb

## Prerequisite
- Conda or Pip
- Python >= 3.7
- Tensorflow >= 2.0 Beta 1
- VS Code (optional)

## Installation
Highly recommended to create a virtual environment to keep Tensorflow 2.0 Beta separated.
## For Conda
### For CPU Installation
```
conda create -n tf20 python=3.7 pip matplotlib pillow scipy pylint
conda activate tf20
pip install tensorflow==2.0.0-beta1
```
### For GPU Installation

We will need to install tensorflow-gpu 1.x first to let conda install CUDA/CUDNN dependencies. Use this command instead.
```
conda create -n tf20 python=3.7 pip matplotlib pillow scipy pylint tensorflow-gpu
conda activate tf20
conda uninstall tensorflow-gpu
pip install tensorflow-gpu==2.0.0-beta1
```


## For PIP

### For CPU Installation
```
virtualenv -p /path/to/python3.7 ~/.virtualenvs/tf20
source ~/.virtualenvs/tf20/bin/activate tf20
pip install numpy matplotlib pillow scipy pylint tensorflow==2.0.0-beta1
```

### For GPU Installation
```
virtualenv -p /path/to/python3.7 ~/.virtualenvs/tf20
source ~/.virtualenvs/tf20/bin/activate tf20
pip install numpy matplotlib pillow scipy pylint tensorflow-gpu==2.0.0-beta1
```

## Known Issue
save_model_as_tflite doesn't work on Windows because there are some issue with TOCO/TFLite Converter in Windows.
## License
Solutions licensed under Apache License. See LICENSE.txt for further details.

