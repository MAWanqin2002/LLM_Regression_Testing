# Introduction
Experiment code for the CAIN 2024 short paper [(Why) Is My Prompt Getting Worse? Rethinking Regression Testing for Evolving LLM APIs](https://arxiv.org/abs/2311.11123)
ACM version: In Proceeding.

## Dataset
We use two datasets in this paper
- Github Dataset: ["Did you miss my comment or what?": understanding toxicity in open source discussions](https://dl.acm.org/doi/10.1145/3510003.3510111)
- Twitter Dataset: [Jigsaw Unintended Bias in Toxicity Classification](https://www.kaggle.com/competitions/jigsaw-unintended-bias-in-toxicity-classification/data)

In ./dataset folder, we've already collected valid links in Github Dataset. You can directly use the
"./dataset/Github.txt". For the Twitter dataset, we provided a dataloader to read "./dataset/train.csv", which can also be used directly.

## Prompts
The prompts are available at `ex_G.py` and `ex_T.py`.
- For Completion APIs, we directly send the prompts to the model.
- For ChatCompletion APIs, we send the prompts as the first user message to the model.


## Usage
Before running, please type your api key into ex_G.py and ex_T.py

To reproduce the accuracy and entropy in the paper, you can run with the following commands:

`python ex_G.py`

`python ex_T.py`


## Citation
If you found this code useful, please consider citing this paper.
The citation code will be updated after publication.
