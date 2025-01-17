OED - Open Exposure Data
========================

On this page:
-------------

* :ref:`intro_OED`
* :ref:`why_OED`
* :ref:`property`
* :ref:`liability`
* :ref:`cyber`
* :ref:`links_OED`

|

.. _intro_OED:

Introduction
************

----

Open Exposure Data (OED) is a standard that provides the industry with a robust, open, and transparent data format with the 
aim to deliver a common framework for encoding, transmitting, and interpreting data. The aim of OED is to improve interoperability 
between platforms and models and to reduce frictional costs by significantly decreasing data processing efforts and supporting 
more efficient cross-model analytics.


|
.. _why_OED:

Why OED?
********

----

The need for a new (re)insurance industry exposure data standard arose from the lack of such an existing standard for Oasis 
based models. Exposure data is the starting point for catastrophe risk analysis, and without such a standard in place it is 
impossible to give users guidance and documentation on how to prepare their input data and enable appropriate validation 
within Oasis based modelling platforms.

The `Oasis financial model (FM) <https://github.com/OasisLMF/ktools/blob/2ab2f9e864c2d77b91cc5c2ab1ced4a1aab0e595/docs/md/
FinancialModule.md#L4>`_ enables a wide variety of model developers to use one consistent financial model: it is a key part of 
the utility of the Oasis framework. However, it is important that financial fields in the exposure data are populated correctly 
so they can be interpreted accurately in the FM.

The OED also provides companies with a starting point for implementing a model-developer-independent exposure data 
repository, which is strategically beneficial as it prevents firms being locked in to any one particular model developer.

Although OED is designed to work well with Oasis based models, the scope of OED is wider than Oasis. For example, financial 
fields exist in OED which are not yet implemented in Oasis, and secondary modifiers exist in OED which are not currently 
used by any Oasis based model. However, Oasis LMF continue to expand the scope of their `FM <https://github.com/OasisLMF/
ktools/blob/2ab2f9e864c2d77b91cc5c2ab1ced4a1aab0e595/docs/md/FinancialModule.md#L4>`_ with the aim to support as much 
of the OED functionality as possible. An in depth overview of the OED can be found `here <https://github.com/OasisLMF/
ODS_OpenExposureData/blob/main/Docs/2_OED_Overview.rst>`_.

OED can support :ref:`property`, :ref:`liability` and :ref:`cyber` classes of business.




|
.. _property:

Property
********

----

The OED format for property comprises of four input files:

* **Location (loc)**
* **Account (acc)**
* **Reinsurance info (RIinfo)**
* **Reinsurance scope (RIscope)**

Together, these four files efficiently and practically represent exposure data that can be interpreted by a catastrophe model. 
The fields in each file and their corresponding data type are described in the ‘OED Input Fields’ tab in the `OED Data Spec 
spreadsheet <https://github.com/OasisLMF/ODS_OpenExposureData/releases/latest>`_. 

.. note::
    Detailed documentation for the OED input files can be found `here <https://github.com/OasisLMF/ODS_OpenExposureData/blob/main/Docs/3_OED_Import_Format.rst>`_.
|

Location ('loc') Import File
############################

----

The ``location`` file contains details relating to each location such as the value and type of asset (including primary and secondary 
modifiers), geographical information, the perils covered and the financial structures within the insurance contract relating 
to the location.

This file is the only mandatory file of the four to run a model and to produce the ground-up losses.

For simple cases, one location is represented by one row in the file. However, for cases with location level financial 
structures that vary by peril, or where multiple special conditions associated with a particular location exist, one 
location can be represented by multiple rows. This is necessary to allow the full complexity of financial contracts to be 
represented in a limited number of input files.
 
For example, a simple location covering wind ('WW1' – see the Perils section in document 5) and flood ('OO1') with a 100 
deductible for buildings (which applies to the combined loss from both perils if both perils happen in a single event) 
could be represented as follows:

|

.. csv-table::
    :widths: 25,25,30,20,35,35
    :header: "LocNumber", "BuildingTIV", "LocPerilsCovered", "LocPeril", "LocDedType1Building", "LocDed1Building"
    
    "1", "100,000", "OO1;WW1", "OO1;WW1", "0", "100"

|

If the same location had a 100 deductible for wind but a 1000 deductible for flood that applied to losses from each peril 
separately, this would be represented in the location input file as shown below:

|

.. csv-table::
    :widths: 25,25,30,20,35,35
    :header: "LocNumber", "BuildingTIV", "LocPerilsCovered", "LocPeril", "LocDedType1Building", "LocDed1Building"

    "1", "100,000", "OO1;WW1", "WW1", "0", "100"
    "1", "100,000", "OO1;WW1", "OO1", "0", "1000"

|

The field names in the examples above are described further in `documents 4, 5
and 6 <https://github.com/OasisLMF/ODS_OpenExposureData/tree/main/Docs>`_.

The minimum fields required in a location file are **LocNumber, AccNumber, PortNumber, CountryCode, LocPerilsCovered, 
LocCurrency, BuildingTIV, ContentsTIV, BITIV, OtherTIV**.

The full set of fields in a location import file can be found by filtering on ‘Loc’ in the 'Input File' column of the 
'OED Input Fields' sheet within the `Open Exposure Data Spec spreadsheet
<https://github.com/OasisLMF/ODS_OpenExposureData/releases/latest/download/OpenExposureData_Spec.xlsx>`_. 

There are over 200 potential fields that could be used within the location file. However, it is not mandatory to use a 
field that is not populated. 


|
Account (acc) Import File
#########################

----

The ``account`` file contains details of the policies and accounts that exist within the import portfolios. Most of the fields 
in this file relate to financial structures, including special conditions.

This file is always required when modelling for insured (or gross) losses.

An account may contain multiple policies and typically each row will represent one policy. However, for cases with policy 
level financial structures that vary by peril or where a policy contains multiple special conditions, one policy may have 
multiple rows in the account file. 

The minimum fields required in an account file are **AccNumber**, **AccCurrency, PolNumber, PortNumber, PolPerilsCovered**.

The full set of fields in an account import file can be found by filtering on ‘Acc’ in the 'Input File' column of the 'OED 
Input Fields' sheet within the `Open Exposure Data Spec spreadsheet
<https://github.com/OasisLMF/ODS_OpenExposureData/releases/latest/download/OpenExposureData_Spec.xlsx>`_. 

Similarly, to the loc file, there are over 200 potential fields that could be used within the account file and it is not mandatory 
to use a field that is not populated. 


|
Reinsurance Info (RIinfo) Import File
#####################################

----

The ``reinsurance info`` file contains details of the reinsurance contracts that relate to the underlying portfolios, accounts 
and locations. There must be exactly one entry per reinsurance contract in this file. Any financial terms relating to 
reinsurance contracts should be entered in this file with the exception of the **CededPercent** for a surplus treaty (which 
should be entered in the reinsurance scope file).

For a list of the reinsurance financial terms available and examples about how to specify such terms see the reinsurance 
section and associated examples.If there is no reinsurance, this import file is not required. If there is reinsurance, the 
minimum fields required are **ReinsNumber, ReinsPeril, ReinsCurrency, InuringPriority, ReinsType, PlacedPercent**.

**ReinsNumber** must be unique, as this links with the reinsurance scope file.

The **RiskLevel** of a reinsurance contract refers to the level at which ‘risk’ terms apply. A ‘risk’ can either be defined 
at Location ‘LOC’, Location Group ‘LGR’, Policy ‘POL’ or Account level ‘ACC’. If a reinsurance contract does not contain 
risk specific terms then the **RiskLevel** field should be left blank. Note that it is not only per-risk treaties that have 
risk level terms. A facultative contract, a quota share treaty or even a catastrophe XL may also have risk level terms and 
thus require a risk level to be defined. 

The full set of fields in a reinsurance info import file can be found by filtering on ‘ReinsInfo’ in the 'Input File' 
column of the `Open Exposure Data Spec spreadsheet
<https://github.com/OasisLMF/ODS_OpenExposureData/releases/latest/download/OpenExposureData_Spec.xlsx>`_.
There are over 20 potential fields that could be used within the reinsurance
info file. However, it is not mandatory to use a field that contains no data.


|
Reinsurance Scope (RIscope) Import File
#########################################

----

The ``reinsurance scope`` file contains details of two different but related pieces of information:

* The scope of the reinsurance contract: i.e. which portfolios, accounts, locations are covered by a particular 
  reinsurance contract.

* The **CededPercent** for a surplus treaty: which can vary for each risk covered by the treaty.

More information on the two points above are discussed `here
<https://github.com/OasisLMF/ODS_OpenExposureData/blob/main/Docs/3_OED_Import_Format.rst>`_,
and more information on reinsurance within the OED can be found in `document 8
<https://github.com/OasisLMF/ODS_OpenExposureData/blob/main/Docs/8_OED_Reinsurance.rst>`_.

The scope of what a reinsurance contract applies to is defined by the ten ‘filter fields’ available in the reinsurance 
scope file: **PortNumber, AccNumber, PolNumber, LocGroup, LocNumber, CedantName, ProducerName, LOB, CountryCode, ReinsTag.**

However, the minimum fields required are: **ReinsNumber**, at least one of the ten filter fields, and **CededPercent** for 
surplus treaties. A full list of the reinsurance variables can be found in the `Open Exposure Data Spec spreadsheet 
<https://github.com/OasisLMF/ODS_OpenExposureData/releases/latest/download/OpenExposureData_Spec.xlsx>`_ by 
filtering for ‘ReinsScope'



|
.. _liability:

Liability
*********

----

The current OED schema for liability is a first version with the aim that it develops as market adoption increases and paths 
for development are suggested.

A full, detailed list of the liability data fields with addition information of the fields can be found `here 
<https://github.com/OasisLMF/ODS_OpenExposureData/blob/develop/OpenExposureData/Liability/Docs/OExD_Liabs_DataFields.csv>`_.

More information about ODS Liability can be found in the `GitHub repository
<https://github.com/OasisLMF/ODS_OpenExposureData/blob/main/Docs/Liability/ReadMe.md>`_.



|
.. _cyber:

Cyber
*****

----

Like liability, the OED schema for cyber is a first version with the aim it develops as market adoption increases. The cyber 
modelling space is still in its infancy and is expected to develop relatively quickly so the OED is expected to develop in
parallel to be appropriate for cyber data capture and modelling requirements. 

Detailed documentation for the OED cyber documentation can be found `Open Exposure Data Spec spreadsheet 
<https://github.com/OasisLMF/ODS_OpenExposureData/blob/develop/OpenExposureData/Cyber/Docs/OED_Cyber_Data_Spec_v1.0.0.xlsx>`_.

More information about ODS Cyber can be found in the `GitHub repository
<https://github.com/OasisLMF/ODS_OpenExposureData/blob/main/Docs/Cyber/ReadMe.md>`_.



|
.. _links_OED:

Links for further information
*****************************

----

Further information and community views of ODS can be found on the ODS website: `<https://oasislmf.org/open-data-standards>`_.

The GitHub repository for OED can be found `here <https://github.com/OasisLMF/ODS_OpenExposureData>`_.

Also available is documentation on `OED currency support <https://github.com/OasisLMF/OasisLMF/blob/main/docs/
OED_currency_support.md>`_ and `OED validation guidelines <https://github.com/OasisLMF/OasisLMF/blob/main/docs/
OED_validation_guidelines.md>`_.
