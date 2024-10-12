# agentlab-weblinx-mvp
MVP version of agentlab-weblinx, we will either merge as fork/PR or create a public repo at release

## Running experiments

If you just want to run experiments, you should be able to simply run the following code:

```bash
# export HF_TOKEN to be your huggingface token
# note: you need to request access to the dataset
export HF_TOKEN="<your_huggingface_token>"

# install agentlab fork
git clone https://github.com/mcGill-NLP/agentlab-weblinx-fork
cd agentlab-weblinx-fork

# optional: create a virtual environment
python -m venv venv && source venv/bin/activate

# install agentlab
pip install -e .

# now, you can run the agent
cd ../
pip install weblinx-browsergym
git clone https://github.com/McGill-NLP/agentlab-weblinx-mvp
python agentlab-weblinx-mvp/run_agent.py
```

## Install agentlab

Install the agentlab package:

```bash
git clone https://github.com/mcGill-NLP/agentlab-weblinx-fork
cd agentlab-weblinx-fork
pip install -e .
```

Then, you can run the following code to test the environment:

```python
import weblinx_browsergym

# pattern: weblinx.<demo_id>.<step>
tasks = weblinx_browsergym.list_tasks(split=split, test_json_path="./test.json")
env = weblinx_browsergym.make(f"browsergym/{tasks[100]}")
obs, info = env.reset()
action = 'click(bid="baf79046-bd85-4867")'
obs, reward, done, info = env.step(action)

assert done is True, "Episode should end after one step"
assert 0 <= reward <= 1, "Reward should be between 0 and 1"
```


## Get snapshots (dom object, axtree, extra properties)

To get snapshots, you need to first install `playwright`:

```bash
pip install -r requirements.txt
playwright install
```

Then, you can run the following code to get snapshots:

```bash
python processing/get_snapshots.py
```

## Create a `test.json` file

To create a `test.json` file, run the following code:

```bash
python processing/create_test_json.py
```

# Copy and zip demos into `bg_wl_data` folder

We store a copy of the full data in the `bg_wl_data` folder, followed by creating zips. To copy the files, run the following code:

```bash
python processing/prepare_data_for_agentlab.py
```

You can upload this `bg_wl_data` folder to huggingface hub with:

```bash
huggingface-cli upload-large-folder McGill-NLP/weblinx-browsergym ./bg_wl_data --repo-type=dataset
```

# Run agent

To run the agent, you can use the following code:

```bash
# optional: set directory where the cache is stored
export BROWSERGYM_WEBLINX_CACHE_DIR="./bg_wl_data"
python run_agent.py
```

## Build and release python package

To build and release the python package, you can run the following code:

```bash
pip install twine wheel

# delet existing dist/ folder
rm -r dist/

# First, create files into dist/
python setup.py sdist bdist_wheel

# Then, upload to pypi
twine upload dist/*
```