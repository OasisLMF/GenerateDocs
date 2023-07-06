ODS - Open Data Standards
=========================

|
On this page:

* :ref:`intro`
* :ref:`structure`
* :ref:`committee`
* :ref:`links`



.. _intro:

Introduction
------------

Open Data Standards (ODS) are a set of specifications and guidelines that define how data should be structured, formatted,
and shared in an open and interoperable manner. These standards enable data to be easily exchanged, accessed, and 
understood by different systems, organizations, and users. Its aim is to be the standard used for exposure data, result 
outputs and contract(s) terminology for the (Re)Insurance industry and other interested parties in catastrophe modelling 
and exposure management across all classes of business.

ODS are central to the evolution of catastrophe modelling. They are key to ensuring continued data consistency, 
transparency, collaboration, and scalability. This enables a significant reduction in work and cost involved to run a 
portfolio of exposures through different models; instead of there being a range of data formats and standards 
from model providers, the ODS facilitates a single, unambiguous format. Detailed documentation on the ODS strategy can be 
found `here <https://github.com/OasisLMF/ODS_OpenExposureData/blob/develop/ODS_2021_Planning_%26_Strategy_v1.pdf>`_.

The ODS is primarily comprised of two parts: 

* :doc:`../../sections/OED`
* :doc:`../../sections/ORD`

OED and ORD define the standardise formats for exposure data that's put into a model, and the results data that is output. 
They are both designed to assist with overcoming interoperability problems current in the catastrophe modelling community.

.. note::
    **It's important to know that ODS is NOT an Oasis standard, but an initiative developed by the market for the market.**



|
.. _structure:

ODS structure with Oasis
************************

Oasis implements ODS as they view open data as central to continued growth in the catastrophe modelling and (re)insurance 
instusties. Oasis LMF are continuously expanding the ODS functionality they support on their platform, especially in 
their `financial module (FM) <https://github.com/OasisLMF/ktools/blob/2ab2f9e864c2d77b91cc5c2ab1ced4a1aab0e595/docs/md/
FinancialModule.md#L4>`_.

The diagram below highlights the proposed, long-term structure of ODS and all the key components. Interoperability is vital 
to ensure efficient interaction across multiple databases, systems and external exposure management and data storage 
facilities.

.. image:: ../images/ODS_Diagram.png
   :width: 600

Detailed documentation on which financial fields are supported in the Oasis kernel can be found `here 
<https://github.com/OasisLMF/OasisLMF/blob/master/docs/OED_financial_terms_supported.xlsx>`_.



|
.. _committee:

How ODS is Governed
*******************

ODS is curated by Oasis LMF and governed by the Open Data Standards Steering Committee (SC), comprised of industry experts 
representing (re)insurers, brokers, service providers and catastrophe model vendors. Its agreed that ODS should not be owned 
by one particular company or entity for specific commercial gain and is currently only being ‘looked after’ by Oasis LMF. 
This will likely change in the coming years. ODS is a market initiative which will rely on wide collaboration from the 
market to develop and progress. The SC will evolve over time and include Subject Matter Experts to assist with areas 
requiring specific domain experience, including data validation and support for enhancing and automating the 
interoperability of these standards.

ODS Committee Members:
######################

.. image:: ../images/ODS_committee_members.png
   :width: 600


ODS Governance
##############

ODS is governed by a steering committee that meets periodically and is chaired by Oasis LMF.

The governance and process around releases and updates of ODS can be found `here <https://github.com/OasisLMF/
ODS_OpenExposureData/tree/develop/Docs>`_ but a schematic of the overview is shown below: 

.. image:: ../images/ODS_Gov_Process_Structure_v0.3.png
    :width: 600


A **Technical Working Group (TWG)** will maintain and update the assets that define the data standards. Although the TWG has a 
few core members from Oasis LMF and Nasdaq, its dynamic and will involve the users from the community who have proposed the 
updates or changes.



|
.. _links:

Links for further information
*****************************

Further information and community views of ODS can be found on the ODS website: `<https://oasislmf.org/open-data-standards>`_.

The GitHub repository for ODS can be found `here <https://github.com/OasisLMF/ODS_OpenResultsData/tree/main>`_.