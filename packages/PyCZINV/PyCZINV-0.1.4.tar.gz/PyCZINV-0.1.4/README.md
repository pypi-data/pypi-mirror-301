# PyCZINV

PyCZINV is a Python package designed for facilitating geophysical inversion processes, with a focus on applications within critical zone science. It aims to simplify and streamline the execution of joint inversion, coupled inversion, and time-lapse inversion to help researchers and practitioners easily derive the subsurface properties they are interested in.

## Features

- **Joint Inversion**: Combine data from different geophysical methods to improve inversion results.
- **Coupled Inversion**: Link inversion processes to consider mutual constraints.
- **Time-Lapse Inversion**: Analyze changes over time to observe dynamic processes.
- **Rock Physics**: Rock Physics models for hydrologic and geophysical properties transformation
- **Data Preprocessing**: Utilities for preparing your geophysical data for inversion.
- **Visualization**: Tools for visualizing inversion results and data.

## Installation

PyCZINV requires Python 3.6 or newer. You can install PyCZINV using pip:

```bash
pip install pyczinv




## Rock Physics Models

### 1. Voigt-Reuss-Hill (VRH) Mixing Model
The VRH model is used to estimate the effective bulk modulus, shear modulus, and density of composite materials made of different minerals. 

**Usage**:
```python
from PyCZINV import VRH_model

# Fraction, Bulk modulus (K), Shear modulus (G), and Density (rho) of minerals
f = [0.35, 0.25, 0.2, 0.125, 0.075]
K = [55.4, 36.6, 75.6, 46.7, 50.4]
G = [28.1, 45, 25.6, 23.65, 27.4]
rho = [2560, 2650, 2630, 2540, 3050]

Km, Gm, rho_b = VRH_model(f=f, K=K, G=G, rho=rho)
print(Km, Gm, rho_b)
