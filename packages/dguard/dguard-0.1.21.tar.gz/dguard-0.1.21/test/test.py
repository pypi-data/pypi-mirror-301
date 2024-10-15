# coding = utf-8
# @Time    : 2024-06-02  15:59:00
# @Author  : zhaosheng@nuaa.edu.cn
# @Describe: Test Whole Dguard Pipeline.

from dguard import DguardModel as dm
from dguard import DguardMos as dmos
# 打印模型列表
dm.info()

# 初始化模型
model = dm(
    embedding_model_names=["eres2net_cn_common_200k", "campp_cn_common_200k"],
    device="cuda",
    length=10, # 每个片段10秒
    channel=0, # 选择第一个通道
    max_split_num=5, # 最多分割5个片段
    start_time=0,    # 每个音频从0秒开始处理
    mean=True,    # 返回所有片段特征的平均值
    verbose=True, # 输出详细日志,默认在DGUARD_MODEL_PATH/logs/%Y%m%d-%H%M%S.log
    apply_vad=True, # 声纹编码前自动应用VAD
    vad_smooth_threshold=0.25, # VAD处理的平滑阈值,两个语音段之间的间隔小于该值时合并
    vad_min_duration=0.3, # VAD处理的最小语音段持续时间,平滑后的语音段小于该值时被丢弃
    save_vad_path=None, # 不自动保存VAD结果
    diar_num_spks=5,
    diar_min_num_spks=1,
    diar_max_num_spks=10,
    diar_min_duration=0.3,
    diar_window_secs=1.5,
    diar_period_secs=0.75,
    diar_frame_shift=10,
    diar_batch_size=4, # 聚类时进行子片段声纹编码的批处理大小
    diar_subseg_cmn=True
)
# 初始化Mos模型
mos_model = dmos()

# 初始化文件地址
file1 = "/home/zhaosheng/Documents/dguard_project/test/data/1channel2person.wav"
file2 = "/home/zhaosheng/Documents/dguard_project/test/data/2channel2person.wav"
file3 = "/home/zhaosheng/Documents/dguard_project/test/data/test.wav"

# from IPython import embed; embed()

# 对比文件相似度
r = model.file_similarity(file1,file2)
print(r)
# 返回类型：dict(str,float)
# {'scores':
#     {'eres2net_cn_common_200k': 0.5876691341400146,
#     'campp_cn_common_200k': 0.4882011413574219},
# 'mean_score': 0.5379351377487183}

# 对比文件相似度（列表，多个测试对）
r = model.file_similarity_list([[file1,file2],[file1,file3]])
print(r)
# 返回类型：list[dict(str,float)]

# 说话人分离
r = model.diarize(file1)
print(r)
# 返回类型：list[tuple(str,float,float,int)]
# [('dguard', 0.322, 3.352, 0), ('dguard', 3.49, 6.36, 2), ('dguard', 7.298, 8.423, 3),
# ('dguard', 47.81, 48.19, 2), ('dguard', 48.578, 49.148, 2), ...]


# 说话人编码
r = model.encode(file1)
print(r)
# 返回类型：tensor

r = model.encode(file1,detail=True)
print(r)
# 返回类型：dict(emb:tensor,embs:list[tensor])

# 说话人编码（列表，多个文件）
r = model.encode_list([file1,file2],detail=True)
print(r)
# 返回类型：list[dict(emb:tensor,embs:list[tensor])]

# Mos 测试
r = mos_model.dnsmos(file3)
print(r)
# {'filename': '/home/zhaosheng/Documents/dguard_project/test/data/test.wav',
# 'len_in_sec': 75.96,
# 'sr': 16000,
# 'num_hops': 66,
# 'OVRL_raw': 2.9168801,
# 'SIG_raw': 3.17129,
# 'BAK_raw': 3.828116,
# 'OVRL': 2.708826004664847,
# 'SIG': 3.012322904099133,
# 'BAK': 3.8180661826496265,
# 'P808_MOS': 2.8329244}