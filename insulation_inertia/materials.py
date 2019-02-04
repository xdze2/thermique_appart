
materials = {}

# in SI:
materials['concrete']  = {'k':1.8, 'rho':2300, 'Cp':1000}
materials['wood_wool'] = {'k':0.04, 'rho':160, 'Cp':2100}
materials['PSE'] = {'k':0.04, 'rho':34, 'Cp':145}
materials['clay'] = {'k':1.28, 'rho':880, 'Cp':1450}

# Compute Thermal diffusivity : 
for props in materials.values():
    if 'kappa' not in props:
        props['kappa'] = props['k']/props['rho']/props['Cp']