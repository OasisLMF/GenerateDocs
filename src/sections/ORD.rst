ORD - Open Results Data
=======================

|
On this page:

* :ref:`intro_ORD`
* :ref:`tables`
* :ref:`summary_levels_example`
* :ref:`links_ORD`


|
.. _intro_ORD:

Introduction
------------

ORD was initially developed during the Lloyd's Lab innovation project (Cohort 3) in 2019, by a working group led by Oasis, 
that focussed on constructing model agnostic results formats and appropriate data formats. These model outputs cover an 
extensive suite of results that can be isolated by aspects of the exposure data, financial and statistical perspectives.

Like :doc:`../../sections/OED`, the purpose of ORD is to ensure model outputs 
are consistent, transparent, and model agnostic. The ORD package is intended to contain the outputs of all current 
catastrophe models and to be extensible to cope with future requirements that may arise. The ORD outputs come in the form 
of results tables that capture all the possible data that a model could produce.

Listed below are the different result tables.


|
.. _tables:

Tables in the ORD format
************************

.. csv-table::
    :header: "Table", "Acronym", "Description", "Currently in Oasis"

    "Sample Event Loss Table", "SELT", "Sample losses for each event at the appropriate summary level", "Yes"
    "Quantile Event Loss Table", "QELT", "Distribution of losses at user specified quantiles for each event at the appropriate summary level", "No"
    "Moment Event Loss Table", "MELT", "Summary stats (mean, SD etc) for each event at the appropriate summary level", "Yes"
    "Sample Period Loss Table", "SPLT", "Sample losses for each event within each period at the appropriate summary level", "No"
    "Quantile Period Loss Table", "QPLT", "Distribution of losses at user specified quantiles for each event within each period at the appropriate summary level", "Yes"
    "Moment Period Loss Table", "MPLT", "Summary stats (mean, SD etc) for each event within each period at the appropriate summary level", "Yes"
    "Average Loss Table", "ALT", "AAL (Average Annual Loss), SD", "Yes"
    "Exceedance Probability Table", "EPT", "Exceedance probabilities for VARs and TVaRs of maximum and aggregate event losses in a period", "Yes"
    "Per Sample Exceedance Probability", "PSEPT", "Exceedance probabilities for VARs and TVaRs of maximum and aggregate event losses in a period for each sample", "Yes"
    "Error Log", "ELOG", "Contains error codes for locations that were failed to be processed by the model", "No"
    "Aggregate summaries of exposure within model domain", "DOMEXP", "Model specific so needs to be in the Results area", "No"
    "Aggregate summaries of rejected exposure by reason rejected", "REJEXP", "Model specific so needs to be in the Results area", "Partly"

.. note::
    A model may not produce every result table; some may not be applicable from that scenario. However, this package covers 
    an extensive suite of model outputs for multiple perspectives and calculations. All the outputs are available in 
    order to cater to all model types and ensure continued interoperability.

The results can then be used to enable users to conduct comprehensive catastrophe risk analysis, quantify potential losses, 
and make informed risk management decisions. Results can be generated at a variety of summary levels, including single-way 
summaries and multi-way summaries. The way such complexity is represented in ORD is shown in the following example:



|
.. _summary_levels_example:

ORD summary levels example
**************************

    Consider an analysis run where the following output summaries are selected:

    * Summary 1: Single way summary of results by OccupancyCode
    * Summary 2: Single way summary of result by ConstructionCode
    * Summary 3: Multi-way summary of results by CountryCode x AreaCode x LOB

    This is represented as follows (using mean and SD as a proxy for any kind of results). On the left are the link files 
    and on the right are the summary files.

    **Summary 1**

    .. csv-table::
        :header: "SummaryId", "OccupancyCode", " ", "SummaryId", "MeanLoss", "SDLoss"

        "1", "1050", " --- ", "1", "23", "34.5"
        "2", "1150", " --- ", "2", "353", "529.5"
    
    **Summary 2**

    .. csv-table::
        :header: "SummaryId", "ConstructionCode", " ", "SummaryId", "MeanLoss", "SDLoss"

        "1", "5050", " --- ", "1", "234", "351"
        "2", "5100", " --- ", "2", "467", "700.5"
        "3", "5150", " --- ", "2", "346", "519"
    
    **Summary 3**

    .. csv-table::
        :header: "SummaryId", "CountryCode", "AreaCode", "LOB", " ", "SummaryId", "MeanLoss", "SDLoss"

        "1", "US", "FL", "A", " --- ", "1", "942", "1413"
        "2", "US", "TX", "A", " --- ", "2", "256", "384"
        "3", "US", "FL", "B", " --- ", "2", "390", "585"



|
.. _links_ORD:

Links for further information
*****************************

More information about tables can be found `here <https://github.com/OasisLMF/ODS_OpenResultsData/blob/main/Docs
/ORD_Data_Spec.xlsx>`_, as well as example tables of results, and more information on ORD descriptions can be found 
`here <https://github.com/OasisLMF/ODS_OpenResultsData/blob/main/ORD_Definitions.md>`_.

The GitHub repository for ORD can be found `here <https://github.com/OasisLMF/ODS_OpenResultsData/tree/main>`_.

