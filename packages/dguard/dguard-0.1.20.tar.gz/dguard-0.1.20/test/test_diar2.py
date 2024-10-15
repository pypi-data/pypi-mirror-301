from dguard import DguardModel as dm
import os
import numpy as np
import torchaudio
from tqdm import tqdm
import torch

# 初始化模型，全部使用默认参数
model = dm(
    embedding_model_names=["resnet293_cjsd8000_wespeaker_split","resnet221_cjsd8000_wespeaker_split"],
    device="cpu",
    length=10,
    channel=1,
    max_split_num=10,
    start_time=0,
    mean=True,
    verbose=True,
    apply_vad=False,
    vad_min_duration=0.25,
    vad_smooth_threshold=0.25,
    save_vad_path=None,
    diar_num_spks=None,
    diar_min_num_spks=1,
    diar_max_num_spks=5,
    diar_min_duration=0.25,
    diar_window_secs=1.5,
    diar_period_secs=0.75,
    diar_frame_shift=10,
    diar_batch_size=4,
    diar_subseg_cmn=True
)

def diar_file(filepath):
    save_split_path = os.path.join(os.path.dirname(filepath),os.path.basename(filepath).split('.')[0]+"_diarize")
    os.makedirs(save_split_path,exist_ok=True)
    r = model.vad_file(filepath)
    data = r["pcm"]
    data = data.reshape(1, -1)
    torchaudio.save(f"{save_split_path}/1.wav", data, r["sample_rate"])
    
    speaker_wavs = sorted([_f for _f in os.listdir(save_split_path) if _f.endswith(".wav")])
    print(f"Sorted speaker wavs: {speaker_wavs}")
    # 说话人编码，时长最长的说话人
    speaker_wav = speaker_wavs[0]
    speaker_wav_filepath = os.path.join(save_split_path, speaker_wav)
    emb_data_r = model.encode(speaker_wav_filepath,channel=0)
    emb_data = emb_data_r["emb"]
    emb_data_all = emb_data_r["embs"]
    for _index,_data in enumerate(emb_data_all):
        _data = _data.detach().cpu().numpy()
        assert _data.shape == (512,), f"emb_data shape is {_data.shape}"
        np.save(f"{speaker_wav_filepath.replace('.wav',f'_{_index}.npy')}", _data)

    emb_data = emb_data.detach().cpu().numpy()
    assert emb_data.shape == (512,), f"emb_data shape is {emb_data.shape}"
    # save to file
    save_path = f"{speaker_wav_filepath.replace('.wav','.npy')}"
    np.save(save_path, emb_data)
    
    data,sr = torchaudio.load(speaker_wav_filepath)
    wav_length = data.shape[1]/sr
    return emb_data,wav_length,sr

def get_args():
    import argparse
    parser = argparse.ArgumentParser(description="Diarization")
    parser.add_argument("--root", type=str, default="/workplace/data_path/zhaosheng/raw_data", help="ROOT path for data")
    parser.add_argument("--log", type=str, default="diar.log", help="Log file path")
    parser.add_argument("--total", type=int, default=8, help="Total number of threads")
    parser.add_argument("--index", type=int, default=0, help="Total number of threads")
    #########################################
    rank = int(os.environ.get("LOCAL_RANK",0))
    world_size = int(os.environ.get("WORLD_SIZE",1))
    args.total = world_size
    args.index = rank
    #########################################
    args = parser.parse_args()
    args.log = args.log.replace(".log", f"_{args.index}.log")
    args.errlog = args.log.replace(".log", "_err.log")
    return args

def main():
    
    args = get_args()
    root = args.root
    phones = [f for f in os.listdir(root) if os.path.isdir(os.path.join(root, f))]
    phones = sorted(phones)
    tiny_length = len(phones) // args.total
    if args.index == args.total - 1:
        phones = phones[args.index*tiny_length:]
    else:
        phones = phones[args.index*tiny_length:(args.index+1)*tiny_length]
    error = False
    
    print("Start diarization\n")
    print(f"Total #{len(phones)} phones\n")
    with open(args.log, "w") as f:
        f.write("phone,id,wav_path,raw_length,emb_shape\n")
    for phone in tqdm(phones):
        # try:
        now_phone_emb = []
        phone_path = os.path.join(root, phone)
        for wav in os.listdir(phone_path):
            if not wav.endswith(".wav"):
                continue
            wav_path = os.path.join(phone_path, wav)
            # try:
            emb_data,wav_length,sr = diar_file(wav_path)
            now_phone_emb.append([emb_data, wav_path])
            # except Exception as e:
            #     print(f"Error: {wav_path}, {e}")
            #     with open(args.errlog, "a") as f:
            #         f.write(f"Error: {wav_path}, {e}\n")
            #     continue

            with open(args.log, "a") as f:
                f.write(f"{phone},{wav_path},{wav_length},{emb_data.shape}\n")
        scores = []
        emb_data_list = [_[0] for _ in now_phone_emb]
        wav_path_list = [_[1] for _ in now_phone_emb]
        if len(emb_data_list) > 1:
            for i in range(len(emb_data_list)):
                for j in range(i+1, len(emb_data_list)):
                    emb_data_i = emb_data_list[i]
                    wav_path_i = wav_path_list[i]
                    emb_data_j = emb_data_list[j]
                    wav_path_j = wav_path_list[j]
                    sim = model.cosine_similarity(emb_data_i, emb_data_j)["mean_score"]
                    if sim < 0.5:
                        error = True
                        print(f"Error: {wav_path_i} and {wav_path_j} similarity is {sim}")
                    scores.append([wav_path_i, wav_path_j, sim])
        with open(f"{phone_path}/scores.txt", "w") as f2:
            for score in scores:
                f2.write(f"{score[0]},{score[1]},{score[2]}\n")
        if error:
            with open(f"{phone_path}/error", "w") as f3:
                f3.write(f"\n")
        # except Exception as e:
        #     print(f"Error: {phone}, {e}")
        #     with open(args.errlog, "a") as f:
        #         f.write(f"Error: {phone}, {e}\n")
        #     continue

if __name__ == "__main__":
    main()