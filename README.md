> [!WARNING]  
> This Python package is **still under** migration/**development** from its initial (legacy) version of August 2024.

# Python package for noble liquid (e.g. liquid argon) purity monitors based on radioactive electron sources (e.g. Bi-207)

## Installation

### Development/editable installation

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
# Activate the new virtual environment
source .venv/bin/activate # Unix/macOS
.venv\Scripts\activate    # Windows
```

Install (once)

```sh
# Install the puritymonitor package from its source in editable mode
pip install -e .
```

Deactivate (each time)

```sh
# Deactivate the virtual environment
deactivate
```

## Usage

[Manual](/docs/manual%20(under%20development).pdf).

## License

[MIT License](/LICENSE).
