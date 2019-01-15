# FunSPICE

FunSPICE is a Python based linear symbolic SPICE style circuit solver, producing equation based results rather than numeric ones like a typical SPICE simulator. Element parameters can be set to single variables, expressions of multiple variables, complex numbers, and constants. FunSPICE only solves linear circuits, thus circuits such as rectifiers, peak detectors, sample-hold, multipliers, translinear loops, square root, etc won't solve properly as linear circuit analysis methods don't apply.

### Summary

### Supported Elements
- Voltage Source (V)
- Current Source (I)
- Resistor (R)
- Inductor (L)
- Capacitor (C)
- Voltage Controlled Voltage Source (E)
- Voltage Controlled Current Source (G)
- Current Controlled Current Source (F)
- Current Controlled Voltage Source (H)
- Ideal 1:N Transformer (X)
- MOSFET SSM with variable ro, gm, cgd, cgs (M)
- BJT SSM with variable ro, beta, gm, cbe, cbc (B)
- OPAMP with infinite or defined gain function (O)

### Supported Features
- Symbolic and numeric AC complex vector circuit analysis
- **print_results():** print all circuit matrix results
- **polezeros(tf):** extract pole and zero frequencies from a transfer function (tf) equation
- **sens(function, var):** compute the sensitivity of function with respect to the symbol var
- **abeta(tf):** extracts the open loop gain and feedback factor from a closed loop tf.

### Future Development Wish List
- Add BULK terminal to MOSFET model
- Current Conveyor/Transimpedance Amplifier AC model (Z)
- Current probe (A)
- Named node ('vi' as opposed to 1)
- Named current results by element/probe ('iv1')
- Specialized AC analysis (S-Param, Noise Figure, PSRR, etc.)

### Future Analysis Ideas
- **S-Parameters:** put port elements in the circuit, and it solves S11, S21, etc in terms of circuit variables. Even and odd mode impedance analysis would be nice too.
- **Noise Figure:** put port elements in the circuit and it solves for NF in terms of the circuit variables for each device and noise source in the circuit (automatically include fet gate noise, bjt shot noise, op amp input referred noise, etc. symbolically)
- **PSSR:** Solve PSRR transfer functions for each defined power rail to a specified node in the circuit (Vo for example)
- Differential and CM: put in a differential source and it solves for Av_d, Av_cm, CMRR, Zin_d, Zin_cm

## Getting Started

### Prerequisites

Python Anacoda, which comes with SymPy, NumPy, and many other amazing scientific libraries and tools.

### Installing

See https://docs.anaconda.com/anaconda/install/ to install Anaconda

### Usage

Once Anaconda is installed, see the FunSPICE Summary to get started.

FunSPICE Element Documentation notebook provides documentation for all the supported elements in FunSPICE

FunSPICE Analysis Template notebook can be copied and modified to perform your own circuit analysis.

FunSPICE can be used with regular python scripts as well, Jupyter is not required, however it makes visualization easier in my opinion.

Here is a template to get started, starting from the import

```
from FunSPICE import *
init_printing()

netlist = [
<insert your list of elements here>
]

funspice = FunSPICE(netlist)
funspice.print_results()
<Add your own results access statements and math operations here>
```
## Authors

* **Adam Gleason**


## License

This project is licensed under the 3-Clause BSD Open Source License - see the [LICENSE.md](LICENSE.md) file for details

