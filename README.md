# FunSPICE

FunSPICE is a Python based linear symbolic SPICE style circuit solver, producing equation based results rather than numeric ones like a typical SPICE simulator. Element parameters can be set to single variables, expressions of multiple variables, complex numbers, and real constants. Say goodbye to doing lengthy FUNdamental circuit analysis by hand, because FunSPICE will do it for you! FunSPICE only solves linear circuits, thus circuits such as rectifiers, peak detectors, sample-hold, multipliers, translinear loops, square root, etc won't solve properly as linear circuit analysis methods don't always apply. All the FunSPICE code is licensed under BSD and is free as in free beer, see the license for more information. 

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
Here is a short list of element templates, see the included notebooks for more details on usage:
- {'type':'V', 'k':k, 'j':j, 'val':'V'}
- {'type':'I', 'k':k, 'j':j, 'val':'Is'}
- {'type':'R', 'k':k, 'j':j, 'val':'R'}
- {'type':'L', 'k':k, 'j':j, 'val':'L'}
- {'type':'C', 'k':k, 'j':j, 'val':'C'}
- {'type':'E', 'k':k, 'j':j, 'p':p, 'q':q, 'val':'A_v'}
- {'type':'G', 'k':k, 'j':j, 'p':p, 'q':q, 'val':'G'}
- {'type':'F', 'k':k, 'j':j, 'p':p, 'q':q, 'val':'A_i'}
- {'type':'H', 'k':k, 'j':j, 'p':p, 'q':q, 'val':'Z'}
- {'type':'X', 'p1':p1, 'n1':n1,' p2':p2, 'n2':n2, 'val':'n'}
- {'type':'M', 'd':0, 'g':1, 's':2, 'ro':'ro', 'gm':'gm', 'cgs':'cgs', 'cgd':'cgd'}
- {'type':'B', 'c':0, 'b':1, 'e':2, 'ro':'ro', 'beta':'beta', 'gm':'gm', 'cbe':'cbe', 'cbc':'cbc'}
- {'type':'O', 'p':p, 'n':n, 'o':o,'val':'A_v'}

### How It Works
FunSPICE reads and parses the user created array of element dictionaries (passed into FunSPICE constructor), which is the netlist for the circuit. The element node indices and values are used to build the main circuit matrix. FunSPICE uses a MNA (Modified Nodal Analysis) matrix stamping algorithm to build the circuit matrix up, then puts the final matrix into row reduced form where the final results are accessed. 

## Authors

* **Adam Gleason**


## License

This project is licensed under the 3-Clause BSD Open Source License - see the [LICENSE.md](LICENSE.md) file for details

