# ambiNilla v.3 #

v.3 - 
3rd order ambisonic added
can switch between 0, 1, 2, and 3rd orders
bug fixes

v.2 - 
2nd order ambisonic
can write raw ambisonic (undecoded) output to file

v.1 - 
1st order ambisonic

changelog:

## Notes: ##
The encoder is derived from this ambisonic panner: [https://github.com/cpmpercussion/SimpleAmbisonics/](https://github.com/cpmpercussion/SimpleAmbisonics/) I streamlined the workflow to support ease of transferring new coefficients to PD, and made a small math update. Functions for elevation as well.

## Math Ref: ##
[http://www.angelofarina.it/Aurora/HOA_ACN_N3D_formulas.htm](http://www.angelofarina.it/Aurora/HOA_ACN_N3D_formulas.htm)

## Instructions: ##

- Input speaker coordinates in the python script. Generate coefficient list.
- Name the list (no spaces) and place it in the 'ambiCoefficients' folder.
- Instantiate an ```ambiDec``` abstraction with the first argument as the list name and the second as the number of channels.
- Make sure the channel selector is set to the correct output or add a new channel count for your setup (or delete and remove the switch if not needed).
- Create as many ```catch~ speaker$1``` as needed and route to ```dac~``` 's (16 are included in the example patch).
- Instantiate one or more 'ambiPanner' abstractions. Connect signal input and set the proper azimuth and elevation (in radians).