import os
from setuptools import setup, find_packages

requirements = [
    "torch>=1.12.0",
    "torchaudio>=0.12.0",
    "silero-vad-nuaazs>=0.0.4",
    "wespeaker-nuaazs>=0.0.5",
    # "silero-vad @ git+https://github.com/pengzhendong/silero-vad.git",
    # "wespeaker @ git+https://gitee.com/iint/wespeaker-nuaazs",
    "wget==3.2",
    "websockets==12.0",
    # "silero-vad==0.0.3",
    "fire==0.4.0",
    "numpy",  # ==1.22.4
    "PyYAML==6.0",
    "scipy==1.10.0",
    "tableprint==0.9.1",
    "torchnet==0.0.4",
    "tqdm==4.62.3",
    # "scikit-learn==1.0.1",
    "matplotlib",  # ==3.5.1
    "flake8==3.8.2",
    "flake8-bugbear",
    "flake8-comprehensions",
    "flake8-executable",
    "flake8-pyi==20.5.0",
    "mccabe",
    "h5py",
    "pycodestyle==2.6.0",
    "pyflakes==2.2.0",
    "lmdb==1.3.0",
    "onnxruntime",
    "soundfile==0.10.3.post1",
    "pypeln==0.4.9",
    "pre-commit==3.5.0",
    "cryptography",
    "datetime",
    "wget",
    "pandas",
    "uuid",
    "cryptography",
    "fire"
]

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="dguard",
    install_requires=requirements,
    version="0.1.19",
    author="Sheng Zhao",
    author_email="zhaosheng@nuaa.edu.cn",
    description=("Speech Diarization and Speaker Embedding"),
    license="BSD",
    keywords="example documentation tutorial",
    url="http://github.com/nuaazs/VAF_2",
    packages=find_packages(),
    long_description=read("dguard/README.md"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    entry_points={
        "console_scripts": [
            "dguard = dguard.interface.cli:main",
            "dguard_info = dguard.cli.info:main",
            "dguard_metrics_multi = dguard.bin.compute_score_metrics_multi:main",
            "dguard_metrics_merge = dguard.bin.compute_score_metrics_merge:main",
            "dguard_plot = dguard.bin.plot:main",
            "dguard_plot_radar = dguard.bin.plot_radar:main",
            "dguard_mean = dguard.bin.mean_csv:main",
        ]
    },
)
