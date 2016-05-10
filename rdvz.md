# Automatic Rendez-vous

## Initial tests

1. Check coplanarity
2. *If needed* check that the orbits go in the same direction
3. Check that the chaser orbit is circular
4. Check that the target orbit is circular
5. Check that the chaser orbit is lower than the target orbit

## Initial Telemetry
### Input Parameters

* Chaser orbit *radius* **r**.  
* Target orbit *radius* **R**.
* Altitude difference **Dr**.
* Gravitational parameter **mu**.
* Current date **t**.
* Current angular separation **alpha**

### Hohman transfer parameters
* Transfer orbit period **T((r+R)/2)**. *Needs formula*
* Target angular separation **delta**. *Needs formula*
* Transfer orbit periapsis speed **vp**. *Needs formula*
* Transfer Delta-v **Dv**. *Needs formula*
* Burn time for transfer **Bt**. *Needs formula*

### Transfer timing parameters
* Relative angular speed **Dw**. *Needs formula*
* Time to transfer **Dt**. *Needs formula*
* Date of transfer **tT**. *Needs formula*

## Wait for transfer

1. Warp until **tT-Bt/2**+error margin
2. Align prograde
3. Wait for **tT-Bt/2**

## Burn

1. Burn prograde until speed matches **vp**  

## Wait for RDVZ

1. Warp until the date of apoapsis - margin of error
2. stage
