# [DocLayout-YOLO: Advancing Document Layout Analysis with Mesh-candidate Bestfit and Global-to-local perception](https://arxiv.org/abs/2405.14458)


Official PyTorch implementation of **DocLayout-YOLO**.

[DocLayout-YOLO: Advancing Document Layout Analysis with Mesh-candidate Bestfit and Global-to-local perception](https://arxiv.org/abs/2405.14458).\
Zhiyuan Zhao, Hengrui Kang, Bin Wang, Conghui He\
[![arXiv](https://img.shields.io/badge/arXiv-2405.14458-b31b1b.svg)](https://arxiv.org/abs/2405.14458)[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/kadirnar/Yolov10)

<details>
  <summary>
  <font size="+1">Abstract</font>
  </summary>
Document Layout Analysis (DLA) plays a critical role in real-world document understanding systems, yet it confronts a challenging speed-accuracy dilemma: multimodal methods leveraging text and visual features provide higher accuracy but suffer from glacial speed, whereas unimodal methods relying solely on visual features offer faster speed but at the cost of compromised accuracy. In addressing this dilemma, we introduce DocLayout-YOLO, which not only enhances accuracy but also preserves the speed advantage through optimization from pre-training and model perspectives in a document-tailored manner. In terms of robust document pretraining, we innovatively regard document synthetic as a 2D bin packing problem and introduce Mesh-candidate Bestfit, which enables the generation of large-scale, diverse document datasets. The model, pre-trained on the resulting DocSynth300K dataset, significantly enhances fine-tuning performance across a variety of document types. In terms of model enhancement for document understanding, we propose a Global-to-local Controllable Receptive Module which emulates the human visual process from global to local perspectives and features a controllable module for feature extraction and integration. Furthermore, to validate performance across different document types, we propose a complex and challenging benchmark named DocStructBench. Experimental results on extensive downstream datasets show that the proposed DocLayout-YOLO excels at both speed and accuracy. Code, data, and model will be made publicly available.
</details>


## Installation
`conda` virtual environment is recommended. 
```
conda create -n doclayout_yolo python=3.9
conda activate doclayout_yolo
pip install -r requirements.txt
pip install -e .
```

## Data Preparation

1. specify data root path

Find your ultralytics config file (for Linux user in $HOME/.config/Ultralytics/settings.yaml) and change ```datasets_dir``` to project root path.

2. Download prepared yolo-format D4LA and doclaynet data from below and put to ./layout_data, the file structure is as follows:

```bash
./layout_data
├── D4LA
│   ├── images
│   ├── labels
│   ├── test.txt
│   └── train.txt
└── doclaynet
    ├── images
    ├── labels
    ├── val.txt
    └── train.txt
```


## Acknowledgement

The code base is built with [ultralytics](https://github.com/ultralytics/ultralytics) and [YOLO-v10](https://github.com/lyuwenyu/RT-DETR).

Thanks for the great implementations! 

## Citation

If our code or models help your work, please cite our paper:
```BibTeX
@misc{wang2024yolov10,
      title={YOLOv10: Real-Time End-to-End Object Detection}, 
      author={Ao Wang and Hui Chen and Lihao Liu and Kai Chen and Zijia Lin and Jungong Han and Guiguang Ding},
      year={2024},
      eprint={2405.14458},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
}
```
