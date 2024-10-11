# scevow

> scevow: Excellent optimization of variant function mapping through weighted random walks at single-cell resolution

> scevow: 通过单细胞分辨率下的加权随机游走对突变功能映射进行优化

## 1. 介绍

## 2. 上传

> upload

> test

```shell
python3 -m build
twine check dist/*
twine upload --repository testpypi dist/*
```

> production

```shell
python3 -m build
twine check dist/*
twine upload dist/*
```

## 3. 使用

```shell
vim ~/.bashrc
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
source ~/.bashrc

```

> test

```shell
pip3 install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
pip3 install scLift -i https://test.pypi.org/simple/
```

> production

```shell
pip3 install scLift

```
