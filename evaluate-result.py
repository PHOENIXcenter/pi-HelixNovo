import argparse
import yaml
from denovo import evaluate

def add_args(parser):
    parser.add_argument("--denovo-result", required=True, help="denovo result of pi-helixnovo", type=str)
    parser.add_argument("--config", required=True, help="the config file", type=str)
    parser.add_argument("--mgf", required=True, help="the corresponding ms2 file for denovo result", type=str)
    parser.add_argument("--thresh", help="thresh", type=float)
    return parser
parser = argparse.ArgumentParser()
parser = add_args(parser)
args = parser.parse_args()

with open(args.config, 'r') as file:
    config_data = yaml.load(file, Loader=yaml.FullLoader)
residues = config_data['residues'] # dict

with open(args.denovo_result,'r') as f:
    lines=f.readlines()
denovo_result=[line.strip().split('\t') for line in lines]


number=0
seq,mz,charge=None,None,None
with open(args.mgf,'r') as f:
    while True:
        line=f.readline()
        if not line:
            break
        if 'SEQ=' in line:
            seq=line.strip().split('=')[-1]
        if 'PEPMASS' in line:
            mz=float(line.strip().split('=')[-1])
        if 'CHARGE' in line:
            charge=int(line.strip().split('=')[-1].split('+')[0])
        if (seq is not None) and (mz is not None) and (charge is not None):
            mass = (mz - 1.007276) * charge
            
            denovo_result[number]=denovo_result[number]+[seq]
            
            number = number + 1
            seq,mz,charge=None,None,None

peptides_pred_raw_f,peptides_pred_raw_r, peptides_pred_raw, real =[],[],[],[]


N = len(denovo_result)
for i in range(N):
    real.append(denovo_result[i][-1])
    peptides_pred_raw.append(denovo_result[i][-3])
    
aa_precision, aa_recall, pep_recall = evaluate.aa_match_metrics(
    *evaluate.aa_match_batch(
        peptides_pred_raw, real, residues
    )
)  

with open(args.denovo_result+'_evaluate.txt','w') as f:
    f.write(f'aa_precision: {aa_precision}, aa_recall: {aa_recall}, pep_recall: {pep_recall}\n')
    for i in range(len(denovo_result)):
        f.write('\t'.join(denovo_result[i])+'\n')
    

