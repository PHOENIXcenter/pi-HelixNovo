# pi-HelixNovo
pi-HelixNovo is a de novo sequencing model based on the Transformer architecture, using a MS2 spectrum and its complementary spectrum as inputs and generating the corresponding peptides. The model weights we have trained are avaliable at https://zenodo.org/records/10405582. If you use pi-HelixNovo in your work, please cite the following publication: 

Tingpeng Yang, Tianze Ling, Boyan Sun, Zhendong Liang, Fan Xu, Xiansong Huang, Linhai Xie, Yonghong He, Leyuan Li, Fuchu He, Yu Wang, Cheng Chang, Introducing π-HelixNovo for practical large-scale de novo peptide sequencing, Briefings in Bioinformatics, Volume 25, Issue 2, March 2024, bbae021, https://doi.org/10.1093/bib/bbae021
# Hardware requirements
## GPU
- Train a model from scratch: An NVIDIA GPU with enough computing power and memory (e.g., Tesla V100 with 32GB of memory).
- Evaluate a pretrained model or de novo sequencing: CPU (slow) or an NVIDIA GPU (e.g., GeForce RTX 3050 with 4GB of memory, ..., Tesla V100 with 32GB of memory). If the error “CUDA OUT OF MEMORY” occurs, please decrease the “predict_batch_size” in the config.yaml.
## Storage space
- Windows system: C drive with enough storage space.
- Linux system: A hard disk with enough storage space.
# The usage of our code
## Preparation:
### For linux users
Enter the code folder

```
conda env create -f main_env.yaml
conda activate main_env 
```

### For windows users
Refer to [Run pi-HelixNovo in Docker](./run_in_docker/docker-env.md)
## Specify the device

```
--gpu=-1 # run pi-HelixNovo on CPU
--gpu=0 # run pi-HelixNovo on GPU 0
--gpu=0,1 # run pi-HelixNovo on GPU 0,1; Distributed deep learning
```

## Train a model from scratch:

```
python main.py --mode=train --gpu=0 --config=./config.yaml --output=train.log --peak_path=./sample_data/training_set/*.mgf --peak_path_val=./sample_data/validation_set/*.mgf
```

## Evaluate a pretrained model

```
python main.py --mode=eval --gpu=0 --config=./config.yaml --output=evaluate.log --peak_path=./sample_data/validation_set/*.mgf --model=the_path_of_your_model
```

## De novo sequencing

```
python main.py --mode=denovo --config=./config.yaml --gpu=0 --output=denovo.log --peak_path=./sample_data/denovo_sample/*.mgf --model=the_path_of_your_model
```
The results will be shown in the current folder as **denovo**.csv because --output=**denovo**.log
| sequence | score | aa_scores | spectrum_id |  
| :--: | :--: | :--: | :--: |  
| VLEGHAEK | 0.95 | "1.0\|1.0\|0.92\|1.0\|1.0\|1.0\|0.7\|1.0" | sample:0 |  
| LQHEAATATQK | 0.93 | "1.0\|0.99\|1.0\|0.93\|1.0\|1.0\|0.53\|0.98\|0.99\|0.83\|1.0" | sample:1 |  
| KEAAPPPK | 0.96 | "1.0\|0.99\|1.0\|1.0\|0.72\|1.0\|1.0\|1.0" | sample:2 |

- `"sequence"` — predicted peptide sequence
- `"score"` — "confidence" score for a predicted sequence
- `"aa_scores"` — per-amino acid scores
- `"spectrum_id"` — information of each prediction
    `{filename}:{index}` string, where  
    `filename` — name of the .mgf file
    `index` —  index (0-based) of each spectrum in an .mgf file.

# Recommendation
For practical large-scale de novo peptide sequencing, we highly recommend utilizing the model weight "pi-helixnovo_massivekb.ckpt", which was trained on the large-scale MassIVE-KB dataset, while employing the "config.yaml" configuration file.

