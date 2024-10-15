# This code incorporates a significant amount of code adapted from the following open-source projects:
# alibaba-damo-academy/3D-Speaker (https://github.com/alibaba-damo-academy/3D-Speaker)
# and wenet-e2e/wespeaker (https://github.com/wenet-e2e/wespeaker).
# We have extensively utilized the outstanding work from these repositories to enhance the capabilities of our project.
# For specific copyright and licensing information, please refer to the original project links provided.
# We express our gratitude to the authors and contributors of these projects for their
# invaluable work, which has contributed to the advancement of this project.

# Copyright 3D-Speaker (https://github.com/alibaba-damo-academy/3D-Speaker). All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

import os
import sys
import re
import argparse
import numpy as np
from tqdm import tqdm
from dguard.utils.utils import get_logger
from dguard.utils.score_metrics import (
    compute_pmiss_pfa_rbst,
    compute_eer,
    compute_c_norm,
    compute_tn_fn_tp_fp,
)


def calc_cosine_similarity(emb1, emb2, embedding_sizes=(256,256)):
    if isinstance(emb1, torch.Tensor):
        emb1 = emb1.cpu().detach().numpy().reshape(-1)
    else:
        emb1 = emb1.numpy().reshape(-1)
    if isinstance(emb2, torch.Tensor):
        emb2 = emb2.cpu().detach().numpy().reshape(-1)
    else:
        emb2 = emb2.numpy().reshape(-1)
    start = 0
    scores = []
    for _size in embedding_sizes:
        emb1 = emb1[start:start+_size]
        emb2 = emb2[start:start+_size]
        start += _size
        cosine_score = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        scores.append(cosine_score)
    return np.mean(scores)


def get_metrics(embedding_list, test_list, embedding_sizes=(256,256), p_target=0.01, c_miss=1, c_fa=1, id_fn=None):
    scores = []
    labels = []
    for embedding_data in embedding_list:
        emb_torch = torch.tensor(embedding_data["emb"])
        emb_id = embedding_data["id"]
        if id_fn:
            emb_id = id_fn(emb_id)
        for test_data in test_list:
            test_torch = torch.tensor(test_data["emb"])
            test_id = test_data["id"]
            if id_fn:
                test_id = id_fn(test_id)
            score = calc_cosine_similarity(emb_torch, test_torch, embedding_sizes)
            label = 1 if emb_id == test_id else 0
            scores.append(score)
            labels.append(label)
            
        # compute metrics
        scores = np.array(scores)
        print(f"Socre shape is {scores.shape}")
        labels = np.array(labels)
        print(f"Label shape is {labels.shape}")

        fnr, fpr = compute_pmiss_pfa_rbst(scores, labels)
        eer, thres = compute_eer(fnr, fpr, scores)
        min_dcf = compute_c_norm(
            fnr, fpr, p_target=args.p_target, c_miss=args.c_miss, c_fa=args.c_fa
        )
        th_matrix_result = compute_tn_fn_tp_fp(scores, labels)

        # write the metrics
        logger.info(f"Results of {trial_name} is:")
        logger.info("\t\tEER = {0:.4f}".format(100 * eer))
        logger.info(
            "\t\tminDCF (p_target:{} c_miss:{} c_fa:{}) = {:.4f}".format(
                args.p_target, args.c_miss, args.c_fa, min_dcf
            )
        )
        for _info in th_matrix_result:
            logger.info(
                "\t\tTH:{0:.2f}\tTP:{1:.4f}\tFP:{2:.4f}\tTN:{3:.4f}\tFN:{4:.4f}".format(
                    *_info
                )
            )
        return eer, min_dcf, th_matrix_result

if __name__ == "__main__":
    main()
