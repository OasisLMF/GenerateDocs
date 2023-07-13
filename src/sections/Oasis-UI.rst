Oasis UI
========

|
On this page:

* :ref:`intro_UI`
* :ref:`walkthrough`
* :ref:`bitesize`
* :ref:`git_repos_UI`
* :ref:`risk_metrics`



|
.. _intro_UI:

Introduction
------------

The Oasis User Interface (UI) is a web-browser application and is the front-end of the Oasis framework. It enables a user to 
import their exposure and financial data before executing a cat model. The results produced by the model are based on the 
user-defined outputs, which are extensively customisable, catering for most user requirements. The UI is simple and 
intuitive to use, and demonstration videos can be found below. There is an extended training video with voice instructions 
and a shorter “bitesize” version capturing the major components of the process.


|
.. _walkthrough:

UI Demo Video - Walkthrough
***************************

..  youtube:: tHRetuhpQzA


|
.. _bitesize:

UI Demo Video - bitesize
************************

..  youtube:: yYTXNS4tgfc


|
.. _git_repos_UI:

GitHub repository
*****************

`OasisUI GitHub repository <https://github.com/OasisLMF/OasisUI#readme>`_.

|
.. _risk_metrics:

Risk metrics
************

The Oasis UI enables the user to generate multiple output reports for several summary levels and perspectives in a single 
run. The Oasis kernel is a Monte-Carlo simulation engine and allows users to specify the number of samples to run.  The 
number of samples required to achieve convergence will vary depending on the model and portfolio, as well as the required 
outputs.

There are two types of statistical outputs that can be delivered in the reports:
    * Numerically integrated – meaning the loss statistic is calculated directly from the underlying probability 
      distribution of loss by numerical integration
    * Sample statistic – meaning the probability distributions of loss are sampled many times and the loss statistic is 
      calculated from the samples

The list of available reports are as follows:
    * Sampled losses
    * Average annual loss and standard deviation
    * Event loss tables
    * Period loss tables
    * Single loss exceedance curve (AEP/OEP)
    * Multiple loss exceedance curve (AEP/OEP)

By summary levels:
    * Location
    * Line of business
    * County
    * State
    * Programme (whole portfolio)
    * Policy (insured loss only)

By Perspective:
    * Ground up
    * Insured loss

|

Output Reports
**************

The following screenshot shows the suite of output reports that can be generated from the UI. 
Multiple reports can be generated for each summary level:

.. figure:: /images/Multiple_Outputs_2.png
    :alt: Oasis UI analysis summary
    :width: 600
|

Customising Plots
*****************

The following screenshot shows how the user can custom their own result plots before exporting for reporting purposes:

.. figure:: /images/Summary_Plots.png
    :alt: Oasis UI analysis summary
    :width: 600
|

Exposure and Loss Maps
**********************

Risk level exposure and losses can be visualised on a map as shown below:

.. figure:: /images/Exposure_Map.png
    :alt: Oasis UI analysis summary
    :width: 600
|
.. figure:: /images/Loss_map_zoomed_in.png
    :alt: Oasis UI analysis summary
    :width: 600
|
  







