import argparse
import yaml
from denovo import evaluate
import re
from sklearn.metrics import confusion_matrix
from sklearn.metrics import average_precision_score,precision_recall_curve,roc_auc_score,roc_curve
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("Agg")
import os
from pyteomics import mgf

def plot_eval_predictions(labels, predictions, path="figure"):
    """
    Plot histogram of positive and negative predictions, precision-recall curve, and receiver operating characteristic curve.
    :param y: Labels
    :type y: np.ndarray
    :param phat: Predicted probabilities
    :type phat: np.ndarray
    :param path: File prefix for plots to be saved to [default: figure]
    :type path: str
    """
    pos_phat = predictions[labels == 1]
    neg_phat = predictions[labels == 0]
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle("Distribution of Predictions")
    ax1.hist(pos_phat)
    ax1.set_xlim(0, 1)
    ax1.set_title("Positive")
    ax1.set_xlabel("p-hat")
    ax2.hist(neg_phat)
    ax2.set_xlim(0, 1)
    ax2.set_title("Negative")
    ax2.set_xlabel("p-hat")
    plt.savefig(path + "phat_dist.svg")
    plt.close()
    precision, recall, pr_thresh = precision_recall_curve(labels, predictions)
    plt.step(recall, precision, color="b", alpha=0.2, where="post")
    plt.fill_between(recall, precision, step="post", alpha=0.2, color="b")
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])
    plt.title("Precision-Recall (AUPR: {:.3})".format(aupr))
    plt.savefig(path + "aupr.svg")
    plt.close()
    fpr, tpr, roc_thresh = roc_curve(labels, predictions)
    plt.step(fpr, tpr, color="b", alpha=0.2, where="post")
    plt.fill_between(fpr, tpr, step="post", alpha=0.2, color="b")
    plt.xlabel("FPR")
    plt.ylabel("TPR")
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])
    plt.title("Receiver Operating Characteristic (AUROC: {:.3})".format(auroc))
    plt.savefig(path + "auroc.svg")
    plt.close()

def judge(denovo,seq,residues):
    denovo = re.split(r"(?<=.)(?=[A-Z])", denovo)
    seq = re.split(r"(?<=.)(?=[A-Z])", seq)
    if len(seq) != len(denovo):
        return 0
    else:
        for i in range(len(seq)):
            if "+" in seq[i] or "-" in seq[i]:
                if abs(residues[seq[i]] - residues[denovo[i]]) >= 0.5:
                    return 0
                else:
                    pass
            else:
                if abs(residues[seq[i]] - residues[denovo[i]]) >= 0.1:
                    return 0
                else:
                    pass
    return 1
    

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

mass_diff=[]
mass_thresh=0.1
number=0
spectra = mgf.read(args.mgf)
for spectrum in spectra:
    seq=spectrum["params"].get("seq")   
    
    truth = judge(denovo_result[number][-2],seq,residues)
    if denovo_result[number][-1] == 'nan':
        denovo_result[number][-1]=0
    else:
        denovo_result[number][-1]=float(denovo_result[number][-1])
    denovo_result[number]=denovo_result[number]+[seq,truth]
    
    
    
    pmz_ = spectrum['params']['pepmass'][0]
    charge = int(spectrum['params']['charge'][0])
    pmass = (pmz_ - 1.007276035)*charge
    
    denovo_seq = denovo_result[number][-4]
    denovo_seq = re.split(r"(?<=.)(?=[A-Z])", denovo_seq)
    denovo_mass = 18.0105647
    
    status=0
    for aa in denovo_seq:
        try:
            denovo_mass = denovo_mass + residues[aa]
        except:
            status=1
    if status == 1:
        diff = mass_thresh*2
    else:
        diff = abs(denovo_mass - pmass)
    if diff >= mass_thresh:
        mass_diff.append(0)
    else:
        mass_diff.append(1)

    number=number+1
    

real=[]
denovo=[]
pred=[]
truth=[]
score=[]
N = len(denovo_result)
for i in range(N):
    real.append(denovo_result[i][-2])
    denovo.append(denovo_result[i][-4])
    pred.append(denovo_result[i][-3])
    truth.append(denovo_result[i][-1])

aa_precision, aa_recall, pep_recall = evaluate.aa_match_metrics(
    *evaluate.aa_match_batch(
        denovo, real, residues
    )
)  
#print('AA precision: ',aa_precision,"AA recall ",aa_recall, "Peptide recall ",pep_recall)


labels = np.array(truth)
predicted_labels = np.array(pred)
#aupr = average_precision_score(labels, predicted_labels)
#auroc = roc_auc_score(labels, predicted_labels)

#plot_eval_predictions(labels, predicted_labels,os.path.dirname(args.denovo_result)+'/')
predicted_labels[predicted_labels>=args.thresh]=1
predicted_labels[predicted_labels<args.thresh]=0

for i in range(len(mass_diff)):
    if mass_diff[i]==0 and predicted_labels[i]==1:
        predicted_labels[i]=0

tn, fp, fn, tp = confusion_matrix(labels, predicted_labels).ravel()
accuracy = (tp+tn)/(tp+tn+fp+fn)
sensitivity = tp/(tp+fn) 
specificity = tn/(tn+fp)
ppv = tp/(tp+fp)
npv = tn/(tn+fn)
f1score = 2*tp/(2*tp+fp+fn)
print("accuracy: {:.4f},sensitivity: {:.4f},specificity: {:.4f},ppv: {:.4f},npv: {:.4f},F1 score: {:.4f}".format(accuracy,sensitivity,specificity,ppv,npv,f1score))


# with open(os.path.dirname(args.denovo_result)+'/result.txt','w') as f:
#     for line in denovo_result:
#         line=[str(i) for i in line]
#         line='\t'.join(line)+'\n'
#         f.write(line)
