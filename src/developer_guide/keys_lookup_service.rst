Keys Service
====================================

Inrotduction
------------
The keys service in the Oasis Loss Modelling Framework is the process which is used to map exposure data (in OED format) into the into the model specific keys required to execute analyses against that model in the core calculation kernel. This document specifies the requirements form the keys service for a typical implementation of an Oasis LMF complient model. It should be noted that this document does not cover the example of a complex model implementation, where the requirements are much more loose, but focusses on the standard implementation where all of the regular ktools components are utilised in the calculation kernel.

High Level Overview
-------------------
At a high level, a keys service implementation should accept, as input, an OED Location file and return a JSON stream including the oasis keys per location/coverage type/sub-peril, along with reasons for non-mapped location/coverage-type/sub-peril combinations where they are outside of the remit of the model

.. figure:: /images/keys_service.png
    :alt: Keys Service High Level Diagram


Return JSON specification
-------------------------
The return JSON should subscribe to the following defintion:

.. code-block:: JSON

        {
        "loc_id": <integer location id from input OED file>,
        "peril_id": <sub-peril id for model (see below)>,
        "coverage_type": <coverage type id (see below)>,
        "area_peril_id": <integer id of the area peril in the footprint file>
        "vulnerability_id": <integer id of the vulnerability function in the vulnerability file>,
        "status": <one of the accepted statuses (see below)>,
        "message": <message to accompany status>
        }



Perils Covered
--------------
It is the responsibility of the keys service to identify the exposures in the input location file are to be modelled. Included in this definition is the identification of risks by perils covered. The keys service implementation should use the “LocPerilsCovered” field in the input location OED file to identify and filter out those locations which are covered by the model and those which are not. If a location in the input file has only location perils covered which are not considered by the model, then this location should receive a failure status (see below), be rejected by the keys sevice and not be assigned an areaperil id value.

Coverage Type
-------------
The coverage type field returned in the JSON stream should comply to the oasislmf standard supported coverage types:

    • **1**: Buildings
    • **2**: Other
    • **3**: Contents
    • **4**: Business Interuption (BI)

Status
------
The status returned by the keys service should comply with the accepeted status values included in the oasislmf package. These accepted statuses are:

    • **success**: the location/coverage type/sub-peril combination has an area peril and vulnerbaility id mapped
    • **fail**: the location/coverage type/sub-peril combination has neither area peril or vulnerbaility id mapped
    • **fail_ap**: the location/coverage type/sub-peril combination has no area peril but a successful vulnerbaility id mapped
    • **fail_v**: the location/coverage type/sub-peril combination has a successful area peril but no vulnerbaility id mapped
    • **notatrisk**:  the location/coverage type/sub-peril combination is within the realm of the model but deamed to be not at risk. This can be used to show that the risk is considered (and so the TIV will be counted in any exposure metrics) but will never generate a loss from the events in the footprint.

Note, there are two additonal defined statuses but these should not be included in the keys service return:

    • **nomatch**: this is a legacy status which is no longer used
    • **noreturn**: this is a status used by oasislmf to highlight exposure records for which no keys service returns were made, wither successful or not. 


Messages
--------
A free text message can be returned with the keys service return JSON. This message should be used to describe the resaon for no oasis key being assigned (e.g. location is outside of model domain) and should be concise while clear enough for a user to understand the issue. Messages only need to be returned with one of the fail stauses. 

Best Practice
-------------
The following list details the expectations from the keys service implementation:

    1. **OED location file fields**: The keys service implementation should accept valid OED location file fields
    2. **Case Sensitivity**: The OED field names should not be case sensitive, so the keys service implementation should not be sensetive to a particular format
    3. **Peril mapping**: It is the responsibility of the keys service to interpret the “LocPerilsCovered” field in the OED input file and assess whether the risk is in scope for the model or not.
    4. **Complete reporting**: The keys service should return records for all risks submitted in the input location file. If a risk is deamed to be out of scope, then the keys service should report that back to oasislmf and not simply ignore the record.
    5. **Coverage Types**: The keys servcie implementation should return records for all coverage types which are included in the model. If the model does not include damage for a particular coverage type at all (e.g. BI) then there is no need to return any values for this coverage type.
    6. **Not at Risk**: If a risk is deamed to be within scope for the model but not at risk for any of the events in the footprint, then the record should be returned with the “notatrisk” status and not with a dummy areaperil value, say. Not at risk items will be included in exposure counts but will not be entered into the calculation kernel.
