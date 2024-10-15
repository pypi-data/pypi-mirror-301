# Copyright (c) 2020 Mobvoi Inc. (authors: Binbin Zhang)
#               2021 Hongji Wang (jijijiang77@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import torch
import logging
from cryptography.fernet import Fernet
import io


def load_checkpoint(model: torch.nn.Module, path: str, encrypt=False, key=None):
    if encrypt:
        with open(path, "rb") as f:
            encrypted_data = f.read()
        decrypted_data = Fernet(key).decrypt(encrypted_data)
        b = io.BytesIO(decrypted_data)
        checkpoint = torch.load(b, map_location="cpu")
    else:
        checkpoint = torch.load(path, map_location="cpu")
    missing_keys, unexpected_keys = model.load_state_dict(
        checkpoint, strict=False
    )
    for key in missing_keys:
        logging.warning("missing tensor: {}".format(key))
    for key in unexpected_keys:
        logging.warning("unexpected tensor: {}".format(key))


def save_checkpoint(model: torch.nn.Module, path: str):
    if isinstance(model, torch.nn.DataParallel):
        state_dict = model.module.state_dict()
    elif isinstance(model, torch.nn.parallel.DistributedDataParallel):
        state_dict = model.module.state_dict()
    else:
        state_dict = model.state_dict()
    torch.save(state_dict, path)
