# How to Run

This guide explains how to set up and run the Car System Agentic AI project. The project is designed to work primarily with **Jupyter notebooks**, with two installation options: UV (recommended) or traditional pip.

## Prerequisites

- Python 3.9 or higher
- Jupyter environment (VS Code, Cursor, JupyterLab, or Jupyter Notebook)

## Installation Options

### Option 1: UV (Recommended)

UV provides faster dependency resolution and better environment management.

#### Installing UV

```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

### Option 2: Traditional pip

If you prefer using pip and virtual environments:

## Setup

### With UV (Recommended)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd car-system-agentic-ai
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```
   This will:
   - Create a virtual environment in `.venv/`
   - Install all project dependencies
   - Install the project in development mode

3. **Verify installation:**
   ```bash
   uv run python -c "import sys; sys.path.insert(0, 'src'); import services; print(f'Services version: {services.__version__}')"
   ```

### With pip

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd car-system-agentic-ai
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   
   # On Linux/macOS
   source .venv/bin/activate
   
   # On Windows
   .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -e .
   pip install -e ".[dev]"  # For development dependencies
   ```

4. **Verify installation:**
   ```bash
   python -c "import sys; sys.path.insert(0, 'src'); import services; print(f'Services version: {services.__version__}')"
   ```

## Running the Application

### Basic Usage

```bash
# Run Python scripts with the project environment
uv run python your_script.py

# Import and use the package
uv run python -c "
import car_system_agentic_ai
print('Car System AI is ready!')
"
```


## Working with Notebooks (Primary Usage)

This project is designed to be used primarily through Jupyter notebooks. Here are the different ways to set up your notebook environment:

### Option 1: VS Code/Cursor (Recommended)

This is the most convenient way to work with the project:

1. **Open your project in VS Code/Cursor**
2. **Create or open a `.ipynb` file**
3. **Select the correct kernel:**
   - Click "Select Kernel" in the top-right corner
   - Choose `.venv (Python 3.12.3)` (this is your project environment)
   - The kernel will show as "Recommended" if detected correctly

4. **Test your setup:**
   ```python
   # First cell - Setup
   exec(open('./setup.py').read())
   
   # Second cell - Import and test
   from notebooks import *
   print(f"✅ Services version: {services.__version__}")
   ```

### Option 2: JupyterLab/Notebook

#### With UV:
```bash
# Start JupyterLab with your environment
uv run jupyter lab

# Or start Jupyter Notebook
uv run jupyter notebook
```

#### With pip:
```bash
# Make sure your virtual environment is activated
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows

# Install Jupyter in your environment (if not already installed)
pip install jupyter jupyterlab

# Start Jupyter
jupyter lab
# or
jupyter notebook
```

### Option 3: Google Colab

If using Google Colab, you'll need to install the package:

```python
# In a Colab cell
!git clone <repository-url>
%cd car-system-agentic-ai

# Setup path manually in Colab
import sys
sys.path.insert(0, '/content/car-system-agentic-ai/src')

# Test installation
import services
print(f"Services version: {services.__version__}")
```
### Troubleshooting Notebooks

**Issue: Package not found**
- Make sure you selected the correct kernel (`.venv` environment)
- Restart the kernel: Kernel → Restart Kernel

**Issue: Wrong Python version**
- Check kernel selection - should show your project's Python version
- In VS Code/Cursor, click "Select Kernel" and choose the `.venv` option

**Issue: Dependencies missing**
- Ensure you ran `uv sync` or `pip install -e ".[dev]"`
- Restart the kernel after installing new dependencies
