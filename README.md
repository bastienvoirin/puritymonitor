> [!WARNING]  
> This Python package is **still under** migration/**development** from its initial (legacy) version of August 2024.

# Python package for noble liquid (e.g. liquid argon) purity monitors based on radioactive electron sources (e.g. Bi-207)

<p align="center">
<a href="https://github.com/bastienvoirin/puritymonitor"><img src="https://img.shields.io/badge/Python-3776AB?&logo=Python&logoColor=fff" /></a>
<a href="https://github.com/bastienvoirin/puritymonitor/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat" /></a>
<a href="https://pypi.org/project/puritymonitor/"><img src="https://img.shields.io/pypi/v/puritymonitor" /></a>
<a href="https://anaconda.org/conda-forge/puritymonitor"><img src="https://img.shields.io/conda/vn/conda-forge/puritymonitor.svg"/></a>
<a href="https://github.com/bastienvoirin/puritymonitor"><img src="https://tokei.rs/b1/github/bastienvoirin/puritymonitor?category=files&style=flat" /></a>
<a href="https://github.com/bastienvoirin/puritymonitor"><img src="https://tokei.rs/b1/github/bastienvoirin/puritymonitor?style=flat" /></a>
</p>

![](/static/dual_pm.svg)

## Usage

[Manual](/docs/manual%20(under%20development).pdf).

## Installation

### Through `pip` and PyPI

```sh
```

### Through `conda`

```sh
```

### Development/editable installation

#### Global installation (not recommended)

Setup and install (once)

```sh
# Clone and enter the package repository
git clone https://github.com/bastienvoirin/puritymonitor.git
cd puritymonitor

# Install the `puritymonitor` package from its source in editable mode
pip install -e .
```

Use in Python programs

```py
import puritymonitor
```

#### Using a virtual environment (recommended)

Setup (once)

```sh
# Clone and enter the package repository
git clone https://github.com/bastienvoirin/puritymonitor.git
cd puritymonitor

# Create a new virtual environment
python3 -m venv .venv # Unix/macOS
py -m venv .venv      # Windows
```

Activate (each time)

```sh
# Activate the virtual environment
source .venv/bin/activate # Unix/macOS
.venv\Scripts\activate    # Windows
```

Install (once)

```sh
# Install the `puritymonitor` package from its source in editable mode
pip install -e .
```

Use in Python programs

```py
import puritymonitor
```

Deactivate (each time)

```sh
# Deactivate the virtual environment
deactivate
```

## License

[MIT License](/LICENSE) © [Bastien Voirin](https://github.com/bastienvoirin).
