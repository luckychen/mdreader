# mdreader

A lightweight Linux desktop Markdown viewer with LaTeX equation rendering.

## Features

- Render standard Markdown (headers, lists, tables, code blocks, links, images)
- LaTeX math equation support via MathJax
- Dark mode toggle
- Live reload when file changes
- Clean, native GUI

## Requirements

- Python 3.10+
- Linux desktop environment

## Installation

### Option 1: Install from GitHub into existing conda environment

If you already have a conda environment and want to install mdreader into it:

```bash
# Activate your conda environment
conda activate your_env_name

# Install from GitHub
pip install git+https://github.com/YOUR_USERNAME/mdreader.git
```

### Option 2: Clone and install locally

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/mdreader.git
cd mdreader

# Create and activate a new conda environment (recommended)
conda env create -f environment.yml
conda activate mdreader

# Install the package
pip install .
```

### Option 3: Install into existing environment from local clone

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/mdreader.git
cd mdreader

# Activate your existing conda environment
conda activate your_env_name

# Install dependencies first (if not already installed)
conda install -c conda-forge pyside6 markdown-it-py watchdog

# Install mdreader
pip install .
```

### Development Install

For development with editable code:

```bash
git clone https://github.com/YOUR_USERNAME/mdreader.git
cd mdreader
conda env create -f environment.yml
conda activate mdreader
pip install -e .
```

## Usage

### Command Line

```bash
# Open a markdown file
mdreader example.md

# Launch without a file (use Ctrl+O to open)
mdreader
```

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+O   | Open file |
| Ctrl+D   | Toggle dark mode |
| Ctrl+Q   | Quit |

## Example

```markdown
# Example Document

## Einstein's Mass-Energy Equivalence

The famous equation:

$$E = mc^2$$

## Gaussian Integral

The Gaussian integral:

$$\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}$$

## Inline Math

The energy is given by $E = mc^2$ where $m$ is mass and $c$ is the speed of light.

## Code Example

```python
def hello():
    print("Hello, World!")
```

## Table

| Name  | Value |
|-------|-------|
| Pi    | 3.14159 |
| e     | 2.71828 |
```

## Dependencies

All dependencies use business-friendly licenses (MIT/BSD/LGPL):

- **PySide6** (LGPL) - Qt GUI framework
- **markdown-it-py** (MIT) - Markdown parser
- **watchdog** (MIT) - File system watcher for live reload

## Uninstall

```bash
pip uninstall mdreader
```

## License

MIT License - business-friendly and open source.# Updated Wed 01 Jul 2026 11:46:00 AM PDT
