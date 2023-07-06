ODS Tools
=========

|
On this page:

* :ref:`intro`
* :ref:`installation`
* :ref:`links`



.. _intro:

Introduction
------------

ODS Tools is a Python package designed to support users of the Oasis Loss Modelling Framework (Oasis LMF). This package 
includes a range of tools for working with Oasis data files, including loading, conversion and validation. This package is 
in accordance with :doc:`../../sections/ODS`. 

|

**How does Oasis use ODS Tools...**

Within Oasis, ODS Tools has 5 primary purposes:

* **OED Validation** - this tool checks to 
* **Currency conversion** - ...
* **Loading exposure data** - ...
* **Accessing OED files** - ...
* **Manipulating OED files** - ...

More information on these applications with documebtation on how to implements these features can be found `here 
<https://github.com/OasisLMF/ODS_Tools/blob/master/README.md>`_.

|

.. _installation:

Installation and Application
****************************

ODS Tools can be installed via pip by running the following command:

.. code-block:: python 

    pip install ods-tools

Once installed, ODS Tools can be used utilised via the command line interface to quickly convert oed files.

Example :

.. code-block:: python 

    ods_tools convert --location path_to_location_file --path output folder

.. note::
    See ``ods_tools convert --help`` for more options.
|

ODS Tools has many useful applications mnaipulating with open exposure data. The ODS Tools package can be used for `loading 
exposure data <https://github.com/OasisLMF/ODS_Tools/blob/master/README.md#loading-exposure-data>`_, `accessing the OED file 
as a DataFrame <https://github.com/OasisLMF/ODS_Tools/blob/master/README.md#access-oed-file-as-dataframe>`_ once the config 
is complete, and `modifying and save the DataFrame <https://github.com/OasisLMF/ODS_Tools/blob/master/
README.md#saving-change-to-the-oed-dataframe>`_. Additonally the `validity <https://github.com/OasisLMF/ODS_Tools/blob/
master/README.md#oed-validation>`_ of OED file can be checked, and the package supports `currency conversion <https://
github.com/OasisLMF/ODS_Tools/blob/master/README.md#currency-conversion-support>`_.


|
.. _links:

Links for further information
*****************************

Further information on ODS_Tools can be found `here <https://github.com/OasisLMF/
ODS_Tools/blob/master/README.md>`_.