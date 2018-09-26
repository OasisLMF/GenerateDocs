Oasis API
=========

Summary
-------

.. note:: 
  The Oasis REST API currently supports running model analyses. 
  We are extending the API to include exposure management capabilities.

.. qrefflask:: src.server.app:APP
  :undoc-static:

A typical interaction with the Oasis REST API is illustrated in the following diagram. 
Exposure is uploaded to the platform, an analysis is started, the analysis status is polled, and when the anlaysis completes the outputs are downloaded.

.. figure:: /images/oasis_api.png
    :alt: Oasis REST API

API Details
-----------

.. autoflask:: src.server.app:APP
  :undoc-static:

Analysis Settings Schema
------------------------

The following schema defines the analysis settings document that is used to configure an analysis.
This document defines:

* General analysis settings, such as the number of Monte Carlo samples.
* Specific model settings, such as running/not-running specific sub-perils.
* What outputs to generate, for what financial perspectives and by what reporting groups.

.. jsonschema:: schema_test.json
