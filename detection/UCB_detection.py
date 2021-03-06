"""
After the auto-online brute approach, here we proposed another approach which
can possibly detect the abnormal in the human activities, from their history.

"""

import numpy as np
import detection

d = np.load('data_d_co.npy')

# par_indice = np.unique(d[:,0])
# three example 101(good), 105(normal), 106(bad)
par_indice = np.array([106])

Number_par = 55
results = []
problem_indice = np.array([5,33,41,47,58])
threshold = 0.6

for indice, label in enumerate(par_indice):

    current_seg = d[d[:, 0] == label]
    # np.random.shuffle(current_seg)

    # 2^5 = 32, 3 states with Hostiles, Uncertain, NON Hostiles
    # Here we initialise the frequency table and probability table
    # the probability_table will change if new elements come in the frequency table

    frequence_table = np.ones([32, 3])

    transform = current_seg[:, 3] * (2 ** 4) + current_seg[:, 4] * (2 ** 3) + \
                current_seg[:, 5] * (2 ** 2) \
                + current_seg[:, 6] * 2 + current_seg[:, 7]

    # We set up an alarm table, which includes two columns, for the
    # first columns, we save the alarm state value,
    # i.e: 1 (normal) No alarm, 0 alarm (not normal)
    # second columns, we evaluate the decision of the system is correct or not


    alarm = np.zeros([len(transform),2])

    for index_trans, value_trans in enumerate(transform):

        # alarm[index_trans,0] = detection.testing(transform[index_trans],frequence_table,current_seg[index_trans,1],threshold)

       alarm[index_trans,0] = detection.best_testing(transform[index_trans],frequence_table,current_seg[index_trans,1])

        # alarm[index_trans,0] = detection.reject_testing(transform[index_trans],frequence_table,current_seg[index_trans,1],threshold)

        # alarm[index_trans, 0] = detection.non_para_testing(transform[index_trans], frequence_table, current_seg[index_trans, 1])

       alarm[index_trans,1] = detection.checking(alarm[index_trans,0],current_seg[index_trans,1:3])
        
       frequence_table = detection.updating(transform[index_trans],current_seg[index_trans,1], 
                                                             frequence_table)
       if indice not in problem_indice:
           results.append(alarm[:,1])

detection.drawing(results)
detection.error_visu(results)

