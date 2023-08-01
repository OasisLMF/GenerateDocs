Versioning
==========

|

Introduction
************

----

This page lists what features were released with each verion.

|

1.28
****

----

* Add platform client unit tests
* Add testing for computation funcs
* [``gulmc``] implement hazard correlation
* Support for monetary / absolute damage functions
* Post Loss Amplification
* add option to have custom oed schema
* Implement account level financial structures
* Add the possibility to have both policy coverage and policy PD
* Stochastic disaggregation 4 & 6 File preparation for disaggregated locations
* Add generate and run to rest client

|

1.27
****

* Implement OED policy coverage terms in Financial Module
* Implement weighted vulnerability feature in ``gulmc``
* Feature/ods tools migration test
* Correlation map
* Parquet to csv comparison script
* Add ``gulmc`` option to the model runner
* Implement correlated random number generation in gulpy
* Feature/param loading
* Peril Specific Runs
* add ``peril_filter`` to run settings spec
* Stochastic disaggregation 7 Full Monte Carlo
* Make code PEP8 compliant

----

|

1.26
****

* Feature/group id cleanup
* adding numba to stitching function
* Refactor group id seed
* Support optionally using ``gulpy`` in the ``oasislmf model run`` job
* Feature/gulpy option in cli test

----

|

1.23
****

----

* Feature/oed2tests
* fmpy: areaperil_id 8 bytes support
* Step policies: add new calcrule (calcrule 28 + limit)
* Generate Quantile Event Loss Table (QELT) and Quantile Period Loss Table (QPLT)
* Option 'lookup_multiprocessing' not read from config file
* stashing
* support parquet for OED
* Replace refs to getmodelpy with modelpy

|

1.15
****

----

* Switched fmpy to the default financial module
* Added TIV reporting to summary info files
* Added check to raise an error if a locations file references account numbers missing from the account file
* The Group ids can now be set by the following internal oasis fields 'item_id', 'peril_id', 'coverage_id', and 
  'coverage_type_id'
* Added validation for unsupported special conditions
* 

|