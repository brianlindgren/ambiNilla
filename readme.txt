ambiNilla v.1

Notes:
This patch is derived from this ambisonic panner: https://github.com/cpmpercussion/SimpleAmbisonics/ I streamlined the workflow to support ease of transferring new coefficients to PD, and made a small math update.

Math Ref:
http://www.angelofarina.it/Aurora/HOA_ACN_N3D_formulas.htm

Instructions:

1. Input speaker coordinates in the python script. Generate coefficient list.
2. Name the list (no spaces) and place it in the "ambiCoefficients" folder.
3. Instantiate an "ambiDec" abstraction with the first argument as the list name and the second as the number of channels.
4. Make sure the channel selector is set to the correct output or add a new channel count for your setup (or delete and remove the switch if not needed).
5. Create as many "catch~ speaker$1" as needed and route to "dac~"s (16 are included in the example patch).
5. Instantiate one or more "ambiPanner" abstractions. Connect signal input and set the proper azimuth and elevation (in radians).