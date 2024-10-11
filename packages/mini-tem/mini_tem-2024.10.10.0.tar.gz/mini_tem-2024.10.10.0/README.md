# Mini TEM
This project aims at making a very lightweight simulation of a transmission electron microscope

## Use
To use this project you can use `mini_tem\i2tem.py` or `mini_tem\i2tem.json` to design your own microscope using the 
components provided (For now lenses, biprims, shifters, deflectors, samples and stigmators).

## Components
The class `Component` is used as an interface to standardize how the components are used. 
It's possible to make your own components by inheriting from it.
Some basic components are provided:

### Lenses
Lenses are the most important component of the microscope. They are used to focus the beam of electrons.

### Biprims
Biprims are used to split the electron beam into two beams.

### Shifters
Shifters are used to shift the beam of electrons along a direction perpendicular to the optical axis.

### Deflectors
Deflectors are used to deflect the beam of electrons along a direction parallel to the optical axis.

### Samples
Samples are used to simulate an interaction between the beam of electrons and an object.