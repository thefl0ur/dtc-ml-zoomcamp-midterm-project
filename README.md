# Wine quality prediction

This project implements a complete ML pipeline for predicting white wine quality based on results of a physicochemical tests.

Midterm project for [ML Zoomcamp](https://datatalks.club/blog/machine-learning-zoomcamp.html) by [DataTalks.Club](https://datatalks.club/)

## Description of the problem

Evaluating wine quality usually requires expert tasters and time-consuming sensory tests. This process can be subjective, expensive, and inconsistent.

This project aims to address this problem by exploring how data and machine learning can help to predict quality more objectively and efficiently.

The project try to understand which chemical have the most influence on quality and taste.

Because of data imbalance, we will try to detect if wine should be classified as `excellent` or not, depending on its quality ( >= 8).


## Running project

### 1. Get data

As dataset project uses dataset [Wine Quality](https://archive.ics.uci.edu/dataset/186/wine+quality) from UC Irvine Machine Learning Repository.
Dataset related to red and white variants of the Portuguese "Vinho Verde" wines.

Alternatively, same dataset can be acquired from [Kaggle](https://www.kaggle.com/datasets/arnavs19/wine-quality-uci-machine-learning-repository/data).

To reproduce results, download dataset and place file named `winequality-white.csv` into `data` folder.

As I don't and wan't to struggle with licenses, dataset is not included into this repo.

### 2. Prepare

#### 2.1 Environment
Project uses [`uv`](https://docs.astral.sh/uv/) as dependency and environment manager. Although, thanks to standardization, it is not necessary to use it for reproduction.

Follow instruction for you case. Instruction provided for linux, may variate depending on your flavor/OS.

##### 2.1.1 with uv
1. Init virtual environment
```bash
uv venv
```
2. Activate environment
```bash
source .venv/bin/activate 
```
3. Install dependencies  
Pass `--dev` argument to install additional deps, needed for running notebook/training script/local server
 ```bash
uv sync [--dev]
```

##### 2.1.2 without uv

1. Init virtual environment
```bash
python -m venv .venv
```
2. Activate environment
```bash
source .venv/bin/activate 
```
3. Install dependencies  
Pass `".[dev]"` to command in order  to install additional deps, needed for running notebook/training script/local server
 ```bash
pip install .
```


#### 2.2 Train model

Script for training provided as `scripts/train.py`.

To train execute next command.

```bash
python3 scripts/train.py data/winequality-white.csv -o model/
```

script params:
* `input_file` - file with dataset
* `-o`/`--output_dir` - where to store trained model. Default is current dir. 

#### 2.3 Build image

For simplicity `Makefile` is provided.

Execute `make build` to build Docker image.

### 3 Run service

#### 3.1 run locally

Dev-dependencies required to run

```bash
MODEL_PATH=model/trained_model.json litestar --app server.app:create_app run --port 8081
```

#### 3.2 run with Docker

Execute command

```bash
make run
```

#### 3.3 Deployed service

One instance of this app deployed to [`Render`](https://render.com/). You can access it on `https://mlz-bsqg.onrender.com/`

> On free tier, [`Render`](https://render.com/) downs service while it is not active, on first request it can be pretty long, while instance is spinning up.

Deploy is based on `docker`-image. Follow [official](https://render.com/docs/deploying-an-image) guide to deploy.

### 4 Access result

Send `json`-data to `/predict` rout in order to get prediction, how big probability of wine being excellent.

Examples below shows how to send request to service.

#### local/docker

```bash
curl -X POST 127.0.0.1:8081/predict -d '{"fixed acidity":6.2,"volatile acidity":0.66,"residual sugar":1.2,"chlorides":0.029,"free sulfur dioxide":29,"pH":3.33,"sulphates":0.39,"alcohol":12.8}'
```

#### web

```bash
curl -X POST https://mlz-bsqg.onrender.com/predict -d '{"fixed acidity":6.2,"volatile acidity":0.66,"residual sugar":1.2,"chlorides":0.029,"free sulfur dioxide":29,"pH":3.33,"sulphates":0.39,"alcohol":12.8}'
```
