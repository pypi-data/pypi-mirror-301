model_info = {
    "resnet293_cjsd8000_wespeaker_split": {
        "embedding_size": "256",
        "sample_rate": "16000",
        "mode": "wespeaker",
        "subdir": "cjsd",
        "add_time": "2024-05-01",
        "author": "zhaosheng",
    },
    "resnet101_cjsd8000_wespeaker_split": {
        "embedding_size": "256",
        "sample_rate": "16000",
        "mode": "wespeaker",
        "subdir": "cjsd",
        "add_time": "2024-05-01",
        "author": "zhaosheng",
    },
    "resnet101_cjsd8000_wespeaker_split_lm": {
        "embedding_size": "256",
        "sample_rate": "16000",
        "mode": "wespeaker",
        "subdir": "cjsd",
        "add_time": "2024-05-01",
        "author": "zhaosheng",
    },
    "resnet152_cjsd8000_wespeaker_split": {
        "embedding_size": "256",
        "sample_rate": "16000",
        "mode": "wespeaker",
        "subdir": "cjsd",
        "add_time": "2024-05-01",
        "author": "zhaosheng",
    },
    "resnet152_cjsd8000_wespeaker_split_lm": {
        "embedding_size": "256",
        "sample_rate": "16000",
        "mode": "wespeaker",
        "subdir": "cjsd",
        "add_time": "2024-05-01",
        "author": "zhaosheng",
    },
    "resnet221_cjsd8000_wespeaker_split": {
        "embedding_size": "256",
        "sample_rate": "16000",
        "mode": "wespeaker",
        "subdir": "cjsd",
        "add_time": "2024-05-01",
        "author": "zhaosheng",
    },
    "resnet221_cjsd8000_wespeaker_split_lm": {
        "embedding_size": "256",
        "sample_rate": "16000",
        "mode": "wespeaker",
        "subdir": "cjsd",
        "add_time": "2024-05-01",
        "author": "zhaosheng",
    },
    "resnet293_cjsd8000_wespeaker_split": {
        "embedding_size": "256",
        "sample_rate": "16000",
        "mode": "wespeaker",
        "subdir": "cjsd",
        "add_time": "2024-05-01",
        "author": "zhaosheng",
    },
    "resnet293_cjsd8000_wespeaker_split_lm": {
        "embedding_size": "256",
        "sample_rate": "16000",
        "mode": "wespeaker",
        "subdir": "cjsd",
        "add_time": "2024-05-01",
        "author": "zhaosheng",
    },
    # raw wespeaker vox
    "voxceleb_campp_lm": {
        "embedding_size": "512",
        "sample_rate": "16000",
        "mode": "wespeaker",
        "subdir": "wespeaker",
        "add_time": "2024-05-01",
        "author": "zhaosheng",
    },
    "voxceleb_ecapa1024_lm": {
        "embedding_size": "192",
        "sample_rate": "16000",
        "mode": "wespeaker",
        "subdir": "wespeaker",
        "add_time": "2024-05-01",
        "author": "zhaosheng",
    },
    "voxceleb_ecapa1024": {
        "embedding_size": "192",
        "sample_rate": "16000",
        "mode": "wespeaker",
        "subdir": "wespeaker",
        "add_time": "2024-05-01",
        "author": "zhaosheng",
    },
    "voxceleb_ecapa512_lm": {
        "embedding_size": "192",
        "sample_rate": "16000",
        "mode": "wespeaker",
        "subdir": "wespeaker",
        "add_time": "2024-05-01",
        "author": "zhaosheng",
    },
    "voxceleb_ecapa512": {
        "embedding_size": "192",
        "sample_rate": "16000",
        "mode": "wespeaker",
        "subdir": "wespeaker",
        "add_time": "2024-05-01",
        "author": "zhaosheng",
    },
    "voxceleb_resnet152_lm": {
        "embedding_size": "256",
        "sample_rate": "16000",
        "mode": "wespeaker",
        "subdir": "wespeaker",
        "add_time": "2024-05-01",
        "author": "zhaosheng",
    },
    "voxceleb_resnet221_lm": {
        "embedding_size": "256",
        "sample_rate": "16000",
        "mode": "wespeaker",
        "subdir": "wespeaker",
        "add_time": "2024-05-01",
        "author": "zhaosheng",
    },
    "voxceleb_resnet293_lm": {
        "embedding_size": "256",
        "sample_rate": "16000",
        "mode": "wespeaker",
        "subdir": "wespeaker",
        "add_time": "2024-05-01",
        "author": "zhaosheng",
    },
    "voxceleb_resnet34": {
        "embedding_size": "256",
        "sample_rate": "16000",
        "mode": "wespeaker",
        "subdir": "wespeaker",
        "add_time": "2024-05-01",
        "author": "zhaosheng",
    },
    "voxceleb_resnet34_lm": {
        "embedding_size": "256",
        "sample_rate": "16000",
        "mode": "wespeaker",
        "subdir": "wespeaker",
        "add_time": "2024-05-01",
        "author": "zhaosheng",
    },
    "voxceleb_gemini_dfresnet114_lm": {
        "embedding_size": "256",
        "sample_rate": "16000",
        "mode": "wespeaker",
        "subdir": "wespeaker",
        "add_time": "2024-05-01",
        "author": "zhaosheng",
    },
    "eres2net_cn_common_200k": {
        "embedding_size": "192",
        "sample_rate": "16000",
        "mode": "wespeaker",
        "subdir": "wespeaker",
        "add_time": "2024-05-01",
        "author": "zhaosheng",
        "wavform_normalize": True,
    },
    "campp_cn_common_200k": {
        "embedding_size": "192",
        "sample_rate": "16000",
        "mode": "wespeaker",
        "subdir": "wespeaker",
        "add_time": "2024-05-01",
        "author": "zhaosheng",
        "wavform_normalize": True,
    },
}

for _model in model_info.keys():
    if "pt" not in model_info[_model].keys():
        model_info[_model][
            "pt"
        ] = f"https://www.modelscope.cn/api/v1/models/nuaazs/vaf/repo?Revision=master&FilePath=encrypted_{_model}.pt"
    if "yaml" not in model_info[_model].keys():
        model_info[_model][
            "yaml"
        ] = f"https://www.modelscope.cn/api/v1/models/nuaazs/vaf/repo?Revision=master&FilePath=encrypted_{_model.replace('_lm','')}.yaml"


if __name__ == "__main__":
    # print all pt and yaml path
    for _model in model_info.keys():
        # print(f"# {_model}")
        pt = model_info[_model]["pt"]
        print(f'wget "{pt}" -O encrypted_{_model}.pt')
        yaml = model_info[_model]["yaml"]
        print(f'wget "{yaml}" -O encrypted_{_model}.yaml')
        # print(model_info[_model]['yaml'])
        # print('# -------------------')
