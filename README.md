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

### Prepare for the casanovo model: 

```
cd main
python setup.py clean --all
python setup.py install
cd ../depthcharge-casanovo
python setup.py clean --all
python setup.py install;
```

### Prepare for the PandaNovo model: 

```
cd main
python setup.py clean --all
python setup.py install
cd ../depthcharge-encoder3(PandaNovo)
python setup.py clean --all
python setup.py install;
```

### Prepare for the model using Encoder-1 to encode the complementary spectrum: 

```
cd main
python setup.py clean --all
python setup.py install
cd ../depthcharge-encoder1
python setup.py clean --all
python setup.py install
```

### Prepare for the model using Encoder-2 to encode the complementary spectrum: 

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
cd ..
```

## Train a model from scratch:

```
main --mode=train --gpu=0 --config=./config.yaml --output=train.log --peak_path=./code/sample_data/training_set/*.mgf --peak_path_val=./code/sample_data/validation_set/*.mgf
```

## Evaluate a pretrained model

```
main --mode=eval --gpu=0 --config=./config.yaml --output=evaluate.log --peak_path=./code/sample_data/validation_set/*.mgf --model=./Model-weights/PandaNovo/ricebean-epoch-11-step-550000.ckpt 
```

## De novo sequencing (the results will be shown in the current folder as predictions.txt)

```
main --mode=denovo --config=./config.yaml --gpu=0 --output=denovo.log --peak_path=./code/sample_data/denovo_sample/*.mgf --model=./Model-weights/PandaNovo/ricebean-epoch-11-step-550000.ckpt 
```

## the config.yaml used in PandaNovo and Casanovo
If you train models on the nine-species benchmark dataset, please use config.yaml  

If you train models on the merged dataset of PXD008808, PXD011246, PXD012645 and PXD012979, please use merge-config.yaml.

If you train models on the MSV000081142 dataset, please use config.yaml


