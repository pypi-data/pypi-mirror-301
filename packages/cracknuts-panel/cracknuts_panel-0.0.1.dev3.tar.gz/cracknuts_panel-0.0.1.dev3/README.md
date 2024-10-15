# cracknuts_panel

Jupyter widget for cracknuts.

### For user in Users in chinese mainland

1. set mirror for pip
2. set mirror for npm (Only developer need.)

## Installation

// Not yet.

```sh
pip install cracknuts_panel
```

## Development installation

You need install nodejs and python environment.

Clone `cracknuts_panel` and `cracknuts` code to local.

```shell
git clone https://codeup.aliyun.com/667fc48e96794f5c6d920349/cracknuts_panel.git
git clone https://codeup.aliyun.com/667fc48e96794f5c6d920349/cracknuts.git
```

Create a virtual environment and then install cracknuts_panel and cracknuts in *editable* mode with the
optional development dependencies:

On Linux:

```shell
cd cracknuts_panel
python3 -m venv --prompt cracknuts_panel .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

```shell
cd cracknuts
pip install -e ".[dev]"
```

On Windows:

```shell
cd cracknuts_panel
python -m venv --prompt cracknuts_panel .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

```shell
cd cracknuts
pip install -e ".[dev]"
```

You then need to install the JavaScript dependencies and run the development server.

```sh
npm install
npm run dev
```

To enable `HMR` you should set environment `ANYWIDGET_HMR=1`  

```shell
# powershell
$env:ANYWIDGET_HMR=1
```

```shell
# bash
ANYWIDGET_HMR=1 jupyter lab
```

Open `demo/*.ipynb` in JupyterLab, VS Code, or your favorite editor to start developing.
