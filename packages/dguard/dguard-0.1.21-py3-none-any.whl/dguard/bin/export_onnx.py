# This code incorporates a significant amount of code adapted from the following open-source projects:
# alibaba-damo-academy/3D-Speaker (https://github.com/alibaba-damo-academy/3D-Speaker)
# and wenet-e2e/wespeaker (https://github.com/wenet-e2e/wespeaker).
# We have extensively utilized the outstanding work from these repositories to enhance the capabilities of our project.
# For specific copyright and licensing information, please refer to the original project links provided.
# We express our gratitude to the authors and contributors of these projects for their
# invaluable work, which has contributed to the advancement of this project.

# Open Neural Network Exchange (ONNX)
# ONNX is a universal model representation format that can be used across multiple deep learning frameworks and platforms.
# It allows models to be exported from one framework to ONNX format, and then loaded and executed in other ONNX-supported frameworks or engines.
# Unlike JIT, ONNX is not limited to a specific framework and focuses on cross-framework deployment and inference.
# coding = utf-8
# @Time    : 2024-04-24  12:20:58
# @Author  : zhaosheng@nuaa.edu.cn
# @Describe: .

import os
import torch
import torch.nn as nn
import yaml
import os

from dguard.utils.config import build_config
from dguard.utils.builder import build
from dguard.wespeaker_nuaazs.models.speaker_model import get_speaker_model
from dguard.wespeaker_nuaazs.utils.checkpoint import load_checkpoint
from tqdm import tqdm


class Model(nn.Module):
    def __init__(self, model, mean_vec=None):
        super(Model, self).__init__()
        self.model = model
        self.register_buffer("mean_vec", mean_vec)

    def forward(self, feats):
        outputs = self.model(feats)  # embed or (embed_a, embed_b)
        embeds = outputs[-1] if isinstance(outputs, tuple) else outputs
        embeds = embeds - self.mean_vec
        return embeds


def convert_model(pt_file, yaml_file, onnx_file):
    if (not os.path.exists(pt_file)) or (not os.path.exists(yaml_file)):
        print(f"# Error: {pt_file} or {yaml_file} does not exist!")
        return False
    with open(yaml_file, "r") as fin:
        configs = yaml.load(fin, Loader=yaml.FullLoader)
        print(f"Load raw config: {configs}")

    model = get_speaker_model(configs["model"])(**configs["model_args"])
    load_checkpoint(model, pt_file)

    mean_vec = torch.zeros(
        configs["model_args"]["embed_dim"], dtype=torch.float32
    )
    model = Model(model, mean_vec)
    model.eval()

    feat_dim = configs["model_args"].get("feat_dim", 80)
    num_frms = 200
    example_input = torch.ones(1, num_frms, feat_dim)
    output = model(example_input)
    print(f"Example input shape: {example_input.shape}")
    print(f"Output shape: {output.shape}")
    torch.onnx.export(
        model,
        example_input,
        onnx_file,
        do_constant_folding=True,
        verbose=False,
        opset_version=14,
        input_names=["feats"],
        output_names=["embs"],
        dynamic_axes={"feats": {0: "B", 1: "T"}, "embs": {0: "B"}},
    )
    print("Export model successfully, see {}".format(onnx_file))
    return True


def convert_models(
    models, yamls, pt_folder, onnx_folder, yaml_folder, re_partten
):
    for model, yaml in tqdm(zip(models, yamls)):
        pt_file = os.path.join(pt_folder, model.split(".")[0] + ".pt")
        yaml_file = os.path.join(yaml_folder, yaml.split(".")[0] + ".yaml")
        onnx_file = os.path.join(onnx_folder, model.split(".")[0] + ".onnx")
        convert_model(pt_file, yaml_file, onnx_file)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--config", type=str, default="tnet", help="")
    parser.add_argument("--checkpoint", type=str, default="tnet", help="")
    parser.add_argument("--output_file", type=str, default="tnet", help="")
    args = parser.parse_args()
    convert_models(
        [args.checkpoint.split("/")[-1]],
        [args.config.split("/")[-1]],
        "pt",
        "onnx",
        "yaml",
        ".*",
    )
