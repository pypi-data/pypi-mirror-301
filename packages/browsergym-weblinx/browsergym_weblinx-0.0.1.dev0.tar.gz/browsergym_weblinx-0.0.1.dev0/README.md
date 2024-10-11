# agentlab-weblinx-mvp
MVP version of agentlab-weblinx, we will either merge as fork/PR or create a public repo at release

First, you can set the cache dir:
```bash
export BROWSERGYM_WEBLINX_CACHE_DIR=".cache/browsergym/weblinx"
```

Then, you can run the following code to test the environment:

```python
import browsergym_weblinx

# pattern: weblinx.<demo_id>.<step>
tasks = browsergym_weblinx.list_tasks(split=split, test_json_path="./test.json")
env = browsergym_weblinx.make(f"browsergym/{tasks[100]}")
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
pip install twine
# First, create files into dist/
python setup.py sdist bdist_wheel

# Then, upload to pypi
twine upload dist/*
```