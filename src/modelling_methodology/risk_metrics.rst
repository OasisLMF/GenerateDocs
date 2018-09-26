Risk metrics
============

The Oasis UI enables the user to generate multiple output reports for several summary levels and perspectives in a single run.  
Reports are delivered as csv files which can be viewed through the user interface, downloaded or launched in Microsoft Excel.
The Oasis kernel is a Monte-Carlo simulation engine allowing users to specify the number of samples to run.  
The required number of samples to achieve convergence will vary depending on the model and portfolio, as well as the required outputs.
There are two types of statistical outputs, and both types will generally be delivered in the final report if more than 1 sample is run.
    Numerically integrated – meaning the loss statistic is calculated directly from the underlying probability distribution of loss by numerical integration.
    Sample statistic – meaning the probability distributions of loss are sampled many times and the loss statistic is calculated from the samples.

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

The following screenshot shows the range of reports that can be created via the Oasis UI:

.. figure:: /images/flamingo_run_analysis.png
    :alt: Oasis UI run analysis

The following screenshot shows the analysis summary that can be created via the Oasis UI.
More detailed outputs can be downloaded for analysis outside the platform.

.. figure:: /images/falmingo_output_summary.png
    :alt: Oasis UI analysis summary
 