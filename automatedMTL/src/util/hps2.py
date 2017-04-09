from os.path import expanduser
import sys
import numpy
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..","model")))
from mcrnn_model_gen2 import model
from train_gen import trainModel as TM
#does hyperparameter search over some set of hyperparams.

LR = [0.01,0.001,0.0001]
LR_MOD = [0.0,1.0] #4
N_EPOCHS = [50] # 30
N_EXPERIMENTS = [10] # 5
KEEP_PROB_VAL = [1.0]
CONTEXT_FC = [512] #1024 on AWS
#3*3*3*30*5/60=67.5 hrs.
#experiment = "context_lr=0.5*lr, task_lr=0.5*lr, no learning rate anealing. Learning rates: "
experiment = "N_epochs = 50. N_exp = 10. lstm: 512 for both. hidden fc: 512 for both. dropout: none."
for lr in LR:
    experiment = experiment + str(lr) + ", "
experiment = experiment + " N epoch: "+str(N_EPOCHS[0]) + " Keep prob: "
for prob in KEEP_PROB_VAL:
    experiment = experiment + str(prob) + ", "
experiment = experiment + " Context_fc: "
for fc in CONTEXT_FC:
    experiment = experiment + str(fc) + ", "

def runExperiment(lr, lr_mod,n_epoch,n_experiments,f1, keep_prob_val, context_fc):
    M= model()

    print M.is_multi_task
    if lr_mod == 0.0:
        M.is_multi_task = False
    else:
        M.is_multi_task = True
    print M.is_multi_task

    print M.lr
    M.lr = lr
    print M.lr

    print M.lr_mod
    M.lr_mod = lr_mod
    print M.lr_mod

    print M.n_epoch
    M.n_epoch = n_epoch
    print M.n_epoch

    print M.context_branch_fc
    M.context_branch_fc = context_fc
    print M.context_branch_fc

    maxAccList = [];
    for i in range(n_experiments):
        accuracyVec = TM(M)#INSERT CODE TO run for n epochs
        maxAcc = numpy.max(accuracyVec)
        maxAccList.append(maxAcc)
    expVal = numpy.mean(maxAccList)
    if lr_mod == 0.0:
        string_result = "lr = " + str(lr) + " lr_mod = "+ "none (lstm)" + " avg_acc = " + str(expVal)+'\n'
    else:
        string_result = "lr = " + str(lr) + " lr_mod = "+ "annealing" + " avg_acc = " + str(expVal)+'\n'

    f1.write("")
    f1.write(string_result)
    f1.flush()
    print string_result



f1 = open(expanduser('~/tweetnet/logs/hps_log_mrnn_bidir.log'),'w+') 
f1.write(experiment)
f1.write("\n")
f1.flush()
for lr in LR:
    for lr_mod in LR_MOD:
        for n_epoch in N_EPOCHS:
            for n_experiments in N_EXPERIMENTS:
		for keep_prob_val in KEEP_PROB_VAL:
		    for context_fc in CONTEXT_FC:
                        runExperiment(lr,lr_mod,n_epoch,n_experiments,f1, keep_prob_val, context_fc)      
f1.close()
