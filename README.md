# PandaNovo
PandaNovo is a de novo sequencing model based on the Transformer architecture, using a MS2 spectrum and its complementary spectrum as inputs and generating the corresponding peptides.
# The usage of our code
## Preparation:  
Enter the code folder

```
conda create --name main_env python=3.8
conda activate main_env
pip install tensorboard;
```

### If you want to prepare for the casanovo model: 

```
cd main
python setup.py clean --all
python setup.py install
cd ../depthcharge-casanovo
python setup.py clean --all
python setup.py install;
```

### If you want to prepare for the PandaNovo model: 

```
cd main
python setup.py clean --all
python setup.py install
cd ../depthcharge-encoder3(PandaNovo)
python setup.py clean --all
python setup.py install;
```

### If you want to prepare for the model using Encoder-1 to encode the complementary spectrum: 

```
cd main
python setup.py clean --all
python setup.py install
cd ../depthcharge-encoder1
python setup.py clean --all
python setup.py install
```

### If you want to prepare for the model using Encoder-2 to encode the complementary spectrum: 

```
cd main
python setup.py clean --all
python setup.py install
cd ../depthcharge-encoder2
python setup.py clean --all
python setup.py install
```

Back to the code folder

```
cd ../..
```

## Train a model from scratch:

```
main --mode=train --gpu=0 --config=./merge-config.yaml --output=train.log --peak_path=./merged-dataset_and_ABRF_DDA_PXD008844_PXD010559/merged-train.mgf --peak_path_val=./merged-dataset_and_ABRF_DDA_PXD008844_PXD010559/merged-valid.mgf
```

## Evaluate a pretrained model

```
main --mode=eval --gpu=0 --config=./merge-config.yaml --output=test.log --peak_path=./merged-dataset_and_ABRF_DDA_PXD008844_PXD010559/ABRF_DDA-test.mgf --model=./Model-weights/PandaNovo/merge-epoch-26-step-500000.ckpt 
```

## De novo sequencing (the results will be shown in the current folder as predictions.txt)

```
main --mode=denovo --config=./merge-config.yaml --gpu=0 --output=test --peak_path=To_be_Identified_MS2.mgf --model=./Model-weights/PandaNovo/merge-epoch-26-step-500000.ckpt 
```

## the config.yaml used in PandaNovo and Casanovo
If you train models on the nine-species benchmark dataset, please use config.yaml  

If you train models on the merged dataset of PXD008808, PXD011246, PXD012645 and PXD012979, please use merge-config.yaml.

If you train models on the MSV000081142 dataset, please use config.yaml


