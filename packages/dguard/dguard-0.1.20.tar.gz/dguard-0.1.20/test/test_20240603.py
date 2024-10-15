# coding = utf-8
# @Time    : 2024-06-03  09:50:55
# @Author  : zhaosheng@nuaa.edu.cn
# @Describe: Read all npy files and compare.
import os
import re
from tqdm import tqdm
import numpy as np

def get_npy_files(path):
    _files = os.listdir(path)
    npy_files = [os.path.join(path, _file) for _file in _files if re.match(r'.*\.npy', _file)
                 and _file != "1.npy"]
    return npy_files

def analyze_data(all_data, n, m):
    count = 0
    for phone in all_data.keys():
        audio_num = len(all_data[phone].keys())
        if audio_num > n:
            for diarize_path in all_data[phone].keys():
                if len(all_data[phone][diarize_path]["split_files"]) > m:
                    count += 1
    print(f"n = {n}, m = {m}, count = {count}")
    return count

def calc_score(emb1, emb2):
    emb1 = emb1.reshape(-1)
    emb2 = emb2.reshape(-1)
    emb1_a = emb1[:256]
    emb1_b = emb1[256:]
    emb2_a = emb2[:256]
    emb2_b = emb2[256:]
    a_score = np.dot(emb1_a, emb2_a) / (np.linalg.norm(emb1_a) * np.linalg.norm(emb2_a))
    b_score = np.dot(emb1_b, emb2_b) / (np.linalg.norm(emb1_b) * np.linalg.norm(emb2_b))
    score = (a_score + b_score) / 2
    return score

if __name__ == "__main__":
    root_path = ""
    phones = os.listdir(root_path)
    phones = [phone for phone in phones if os.path.isdir(os.path.join(root_path, phone))]
    phones = sorted(phones)
    print(f"Total # of phones: {len(phones)}")
    total_split_files = 0

    all_data = {}
    for phone in tqdm(phones):
        all_data[phone] = {}
        diarize_paths = os.listdir(os.path.join(phone))
        diarize_paths = [os.path.join(phone,_path) for _path in diarize_paths if os.path.isdir(os.path.join(phones, _path))
                        and re.match(r'.*diarize.*', _path)
                        and "channel" not in _path]
        diarize_paths = sorted(diarize_paths)
        
        for diarize_path in diarize_paths:
            if not os.exists(os.path.join(diarize_path, "1.wav")):
                print(f"Error: {diarize_path} has no 1.wav")
                continue
            else:
                emb = np.load(os.path.join(diarize_path, "1.npy"))
                assert emb.shape[0] == 512, f"Error: {diarize_path} has wrong shape: {emb.shape}"
            npy_files = get_npy_files(diarize_paths[0])
            all_data[phone][diarize_path] = {}
            all_data[phone][diarize_path]["split_files"] = npy_files
            all_data[phone][diarize_path]["mean_emb"] = emb
            total_split_files += len(npy_files)

    print(f"Total # of split files: {total_split_files}")
    analyze_data(all_data, 2, 2)
    analyze_data(all_data, 2, 3)
    analyze_data(all_data, 2, 4)
    analyze_data(all_data, 2, 5)
    if os.path.e

    # 开始比对,同一个手机号目录下任意两条音频相似度0.7的音频数量
    count = 0

    for phone in all_data.keys():
        audio_num = len(all_data[phone].keys())
        check_pass = True
        if audio_num > 1:
            for diarize_path1 in all_data[phone].keys():
                for diarize_path2 in all_data[phone].keys():
                    if diarize_path1 == diarize_path2:
                        continue
                    emb1 = all_data[phone][diarize_path1]["mean_emb"]
                    emb2 = all_data[phone][diarize_path2]["mean_emb"]
                    score = calc_score(emb1, emb2)
                    if score < 0.7:
                        check_pass = False
                        break
            if check_pass:
                count += 1
    print(f"count = {count}")


    # Out putscore.txt
    # <id1> <id2> <label> <score>
    with open("score.txt", "w") as f:
        all_mean_emb = []
        for phone in data1.keys():
            for d in data1[phone].keys():
                all_mean_emb.append([phone, d, data1[phone][d]["mean_emb"]])
        for i in range(len(all_mean_emb)):
            for j in range(i+1, len(all_mean_emb)):
                data1 = all_mean_emb[i]
                data2 = all_mean_emb[j]
                phone1 = data1[0]
                phone2 = data2[0]
                diarize_path1 = data1[1]
                diarize_path2 = data2[1]
                label = "target" if phone1 == phone2 else "nontarget"
                emb1 = data1[2]
                emb2 = data2[2]
                score = calc_score(emb1, emb2)
                f.write(f"{phone1} {phone2} {label} {score:.4f}\n")

            






