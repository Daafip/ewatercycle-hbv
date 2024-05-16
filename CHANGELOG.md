## Changelog

### v1.0.0
working basic version after various testing [versions](https://test.pypi.org/project/ewatercycle-HBV/)
#### v1.1.0
upgrade to new version: added support for updating memory vector on the fly for Data assimilation
##### v1.1.1
Fixed bug with Tlag and setting memory vector correctly 
##### v1.1.2
Adding `.finalize()` method - clears up the directory. Especially useful for DA. 
### V1.2.0
- pretty big issue with setting values fixed - won't affect most use but will cause issues for Data Assimilation
- use opportunity to name all HBV packages/naming/images to 1.2.0 
### V1.3.1
- now supports camels.txt files natively. Just download the ones you want from there and add it. 
- make sure you also include the alpha value which is a model output from the run, defaults to 1.26 but varies per catchment. Eq1 of camels paper.
### v1.3.2. - 1.3.3
- now correctly slices the ds to given start and end time whoops
### v1.3.4 - 1.3.9
- formalises forcing: either `.txt`  or (two) `.nc` forcing supplied & run corresponding code
### v1.4.0
- Refactor `forcing_file` attribute to `camel_file` -> as essentially it's now a txt file of specific class which the from_camels functions is run on in model startup
- change selection of dataset period to be inclusive
#### v.1.4.1 
- changes to config file: alpha is not needed in model, only in forcing per definition. 
- now removes any netcdf files created when using camels or test data
#### v.1.4.2
- updated parameter function to return nicely formated parameter dict
### 1.5.0
- changes output model parameter from `Q_m` to `Q`!!! **this is not backward compatible**, Docker images version 1.3.0.
#### 1.5.1
- fix bug/implementation error with time indexing, docker image version 1.3.1
#### 1.5.2
- typo in bmi implementation: docker image 1.3.2
### 1.6.0
  - now compatible with ewatercycle V2.1 `LumpedMakkinkForcing` which generates evaporation from era5/CMIP.
#### 1.6.1
  - bug fix occuring when loading makkink data
### 1.7.0
  - new version of HBV bmi which adds snow 
#### 1.7.1
  - bug fix with definitions of state variable names
### 1.8.0
- Refactor potential evaporation from `pev` to `evspsblpot` & `tasmean` to `tas` to match convention
#### 1.8.1
- Rename `LumpedCamelsForcing` to `CamelsForcing`
#### 1.8.2
- No longer removes config on `finalize`, should be up to user
#### 1.8.3
- Local model: `HBVLocal` also availible in wrapper
#### 1.8.4
- On generation of forcing adds a unique id (string) to be able to generate a lot of forcing at once
