Versioning
==========

|

.. _intro_versioning:

Introduction
************

----

This page lists what features were released with each verion.

|

.. _1.28_versioning:

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

.. _1.27_versioning:

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

.. _1.26_versioning:

1.26
****

* Feature/group id cleanup
* adding numba to stitching function
* Refactor group id seed
* Support optionally using ``gulpy`` in the ``oasislmf model run`` job
* Feature/gulpy option in cli test

----

|

.. _1.25_versioning:

1.25
****

----

* Feature/docs
* Add supported OED versions to model metadata (model_settings.json)
* Feature/976 quantile
* Footprint server profiling

|

.. _1.24_versioning:

1.24
****

----

8* allow event subset to be passed in analysis settings
* Footprint server
* Enable the use of summary index files by ktools component aalcalc

|

.. _1.23_versioning:

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

.. _1.22_versioning:

1.22
****

* fmpy: areaperil_id 8 bytes support
* Generate Quantile Event Loss Table (QELT) and Quantile Period Loss Table (QPLT)
* support parquet for OED
* stashing
* Step policies: support files with both step and non-step policies

----

|

.. _1.21_versioning:

1.21
****

----

* Max Ded back allocation
* fmpy: areaperil_id 8 bytes support
* Generate Quantile Event Loss Table (QELT) and Quantile Period Loss Table (QPLT)
* support parquet for OED

|

.. _1.20_versioning:

1.20
****

----

* Generate Moment Event Loss Table (MELT), Sample Event Loss Table (SELT), Moment Period Loss Table (MPLT) and Sample 
  Period Loss Table (SPLT)

|

.. _1.19_versioning:

1.19
****

----

* improve memory usage of fmpy

|

.. _1.18_versioning:

1.18
****

----

* correction for PolDed6All fields
* Add PALT to genbash
* Pol Fac Contracts

|

.. _1.17_versioning:

1.17
****

----

* Error handling for invalid oasislmf.json config files

|

.. _1.16_versioning:

1.16
****

----

* Store analysis run settings to outputs via the MDK

|

.. _1.15_versioning:

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

.. _1.14_versioning:

1.14
****

----

**Nothing notable**

|

.. _1.13_versioning:

1.13
****

----

* Add CLI flags for lookup multiprocessing options
* Added fmpy support for stepped policies
* Added user defined return periods option to analysis_settings.json
* Enabled Fmpy to handle multiple input streams

|

.. _1.12_versioning:

1.12
****

----

* Peril Handling in Input Generation
* Added experimental financial module written in Python 'fmpy'
* Define relationships between event and occurrence in model_settings

|

.. _1.11_versioning:

1.11
****

----

**Nothing notable**

|

.. _1.10_versioning:

1.10
****

----

* Extract and apply default values for OED mapped FM terms
* Split calc. rules files
* Include unsupported coverages in type 2 financial terms calculation
* Integration of GUL-FM load balancer
* Refactor oasislmf package

|

.. _1.9_versioning:

1.9
****

----

* Add type 2 financial terms tests for multi-peril to regression test
* Added Scripts for generated example model data for testing

|

.. _1.8_versioning:

1.8
****

----

* Install complex_itemstobin and complex_itemstocsv by default
* Add FM Tests May 2020
* Add JSON schema validation on CLI
* Add api client progressbars for OasisAtScale

|

.. _1.7_versioning:

1.7
****

----

* item file ordering of item_id
* extend calcrules
* Add exception wrapping to OasisException
* Pre-analysis exposure modification (CLI interface)

|

.. _1.6_versioning:

1.6
****

----

* Extend calcrules to cover more combinations of financial terms
* Improve performance in write_exposure_summary()
* Long description field to model_settings.json schema
* Total TIV sums in exposure report
* Group OED fields from model settings

|

.. _1.5_versioning:

1.5
****

----

* Step Policy features supported
* Command line option for setting group_id
* CLI option to set a complex model gulcalc command
* Update to the Model Settings schema

|

.. _1.4_versioning:

1.4
****

----

* all custom lookups now need to set a loc_id column in the loc. dataframe
* new gulcalc stream type

|

.. _1.3_versioning:

1.3
****

----

**Nothing notable**

|

.. _1.2_versioning:

1.2
****

----

**Nothing notable**

|