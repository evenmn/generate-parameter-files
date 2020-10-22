# No reference

citation = "No reference"

molecule = "HOH"

params = {"HHH":       {"A": 0.0,
                        "eta": 9,
                        "Zi": 0.443,
                        "Zj": 0.443,
                        "sigmai": 0.3584,
                        "sigmaj": 0.3584,
                        "alphai": 0.0,
                        "alphaj": 0.0,
                        "r1s": 4.43,
                        "r4s": 2.5,
                        "W": 0.0,
                        "rc": 5.5,
                        "B": 0.0,
                        "xi": 0.0,
                        "r0": 0.0,
                        "C": 0.0,
                        "cos(theta)": 0.0},

          "OOO":       {"A": 501.735673,
                        "eta": 9,
                        "Zi": -0.886,
                        "Zj": -0.886,
                        "sigmai": 0.6,
                        "sigmaj": 0.6,
                        "alphai": 2.4,
                        "alphaj": 2.4,
                        "r1s": 4.43,
                        "r4s": 2.5,
                        "W": 18.03961,
                        "rc": 5.5,
                        "B": 0.0,
                        "xi": 0.0,
                        "r0": 0.0,
                        "C": 0.0,
                        "cos(theta)": 0.0},

          "OHH":       {"A": 1.624562,
                        "eta": 9,
                        "Zi": -0.886,
                        "Zj": 0.443,
                        "sigmai": 0.6,
                        "sigmaj": 0.3584,
                        "alphai": 2.4,
                        "alphaj": 0.0,
                        "r1s": 4.43,
                        "r4s": 1.51113,
                        "W": 0.0,
                        "rc": 5.5,
                        "B": 95.48961,
                        "xi": 0.75,
                        "r0": 1.4,
                        "C": 0.0,
                        "cos(theta)": -0.138267391},

          "HOO":       {"A": 1.624562,
                        "eta": 9,
                        "Zi": 0.443,
                        "Zj": -0.886,
                        "sigmai": 0.3584,
                        "sigmaj": 0.6,
                        "alphai": 0.0,
                        "alphaj": 2.4,
                        "r1s": 4.43,
                        "r4s": 1.51113,
                        "W": 0.0,
                        "rc": 5.5,
                        "B": 0.0,
                        "xi": 0.0,
                        "r0": 0.0,
                        "C": 0.0,
                        "cos(theta)": 0.0},

          "HOH":       {"A": 0.0,
                        "eta": 0.0,
                        "Zi": 0.0,
                        "Zj": 0.0,
                        "sigmai": 0.0,
                        "sigmaj": 0.0,
                        "alphai": 0.0,
                        "alphaj": 0.0,
                        "r1s": 0.0,
                        "r4s": 0.0,
                        "W": 0.0,
                        "rc": 0.0,
                        "B": 0.0,
                        "xi": 0.0,
                        "r0": 0.0,
                        "C": 0.0,
                        "cos(theta)": 0.0},

          "HHO":       {"A": 0.0,
                        "eta": 0.0,
                        "Zi": 0.0,
                        "Zj": 0.0,
                        "sigmai": 0.0,
                        "sigmaj": 0.0,
                        "alphai": 0.0,
                        "alphaj": 0.0,
                        "r1s": 0.0,
                        "r4s": 0.0,
                        "W": 0.0,
                        "rc": 0.0,
                        "B": 0.0,
                        "xi": 0.0,
                        "r0": 0.0,
                        "C": 0.0,
                        "cos(theta)": 0.0},

          "OHO":       {"A": 0.0,
                        "eta": 0.0,
                        "Zi": 0.0,
                        "Zj": 0.0,
                        "sigmai": 0.0,
                        "sigmaj": 0.0,
                        "alphai": 0.0,
                        "alphaj": 0.0,
                        "r1s": 0.0,
                        "r4s": 0.0,
                        "W": 0.0,
                        "rc": 0.0,
                        "B": 0.0,
                        "xi": 0.0,
                        "r0": 0.0,
                        "C": 0.0,
                        "cos(theta)": 0.0},

          "OOH":       {"A": 0.0,
                        "eta": 0.0,
                        "Zi": 0.0,
                        "Zj": 0.0,
                        "sigmai": 0.0,
                        "sigmaj": 0.0,
                        "alphai": 0.0,
                        "alphaj": 0.0,
                        "r1s": 0.0,
                        "r4s": 0.0,
                        "W": 0.0,
                        "rc": 0.0,
                        "B": 0.0,
                        "xi": 0.0,
                        "r0": 0.0,
                        "C": 0.0,
                        "cos(theta)": 0.0}}

for group in params.keys():
    A = params[group]["A"]
    Zi = params[group]["Zi"]
    Zj = params[group]["Zj"]
    eta = params[group]["eta"]
    sigmai = params[group]["sigmai"]
    sigmaj = params[group]["sigmaj"]
    alphai = params[group]["alphai"]
    alphaj = params[group]["alphaj"]

    params[group]["H"] = A * (sigmai + sigmaj)**eta
    params[group]["D"] = alphai * Zj**2 + alphaj * Zi**2
