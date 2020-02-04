Frequently Asked Questions
==========================

How do I access the Oasis framework? 
------------------------------------

The Oasis platform can be accessed in multiple ways depending on the user’s requirements. 
Oasis can be hosted on an AWS (Amazon Web Services) environment and is compatible with most cloud-based servers.
Models can be run by using either the Oasis user interface (UI) or the application programming interface (API). 
The UI is accessed via a web login, while the API which is hosted by Oasis on their AWS server, enables the models to be run directly from a company’s internal system for those wanting to incorporate Oasis into their existing workflow.
Oasis is also available through Nasdaq and their Modex user interface.

What models do I have access to in Oasis?
-----------------------------------------

Although there are numerous models available on the Oasis platform, access to them depend on the agreements in place between the user and the model vendor. All available models will be accessible in the UI or via the API.
A list of the current models in Oasis can be found `here <https://oasislmf.org/community/model-providers>`_.


How do I gain access to more models?
------------------------------------

More models can be added to the user account once agreements with the vendors are in place. 
However, the majority of models can be accessed on a limited basis for testing or evaluation purposes via an AWS environment.


How much will it cost to use the Oasis platform? 
------------------------------------------------

The cost of using Oasis varies depending on the models, the data used, the size of the organisation and the number of users. An approximate guidance to model license costs, based on the most material models (US EQ & Hurricane, Japan EQ & Typhoon, European WS and UK Flood), over a 3-year deal are shown below. 
Prices do not include hosting costs or taxes and are in USD. 
This should be used as a guide only and will vary.

    • Small company in the region of $479,000
    • Medium company in the region of $663,000
    • Large company in the region of $930,000


Models can be accessed for free as Open Access Models where they will be hosted internally on the Oasis AWS server. The suite of models available are continuously increasing based on demand and requirements. 
Initial models available are the GEM (Global Earthquake Model) and the Columbia University climate and extreme weather event model developed by Adam Sobel. The focus of the Open Access Models will be primarily based on validation projects rather than commercial rollups and pricing.
Contact Oasis for more information on the Open Access models.

Can I use the Oasis software under Windows or is it currently just Linux and Mac?
---------------------------------------------------------------------------------

The Oasis model developer tool kit (MDK) software is not fully supported for Windows currently. 
However you should be able to run it in Docker for Windows.

What is the difference between “analytical” and “sample” in the results?
------------------------------------------------------------------------

The Analytical outputs refer to the mean losses across the whole loss curve and is the true reflection of the ground-up losses when financial terms are not applied. 
The Sample outputs refers to the losses across the number of samples selected by the user and is the most accurate view when applying financial terms and calculating the insured loss. 


What are “samples”?
-------------------

Samples are based on the Monte-Carlo simulation methodology that is adopted by Oasis. 
Each sample represents a “simulation year” that contains a randomly generated number of events. 
For example, year one could experience five events; year two might only experience one event with zero events occurring in year three and so on. Each event can produce a loss depending on the locations of the risks and the severity of the event while some events may not produce a loss at all. 
This generates the losses per sample perspective.


How do I know how many samples to run?
--------------------------------------

This is a complex question that is largely based on the size of the portfolio being run and the user requirements. In general, for commercial purposes, to get a more accurate reflection of insured losses across a portfolio of risks that contain financial terms, the smaller the portfolio, the more samples should be run. Exposing a small number of risks to larger amounts of samples, increases the loss distribution around the mean and the convergence across the sample set. This reduces volatility and uncertainty especially in the tail of the loss curve, which is driven by the more severe, less frequent events.
Reducing uncertainty, ultimately provides a more accurate reflection of the risk.
Following that, a large portfolio should not be limited to only running a small sample set. 
Regardless of size of the portfolio, reducing uncertainty and increasing the accuracy, is recommended for all cat modelling exercises. 
It is, however, worth considering how increasing the number of samples will impact performance and server space.

What is the uncertainty and how does it affect the outcomes?
------------------------------------------------------------

As models are based on probabilistic distribution of losses along a severity curve, uncertainty is an important factor to consider when using any model. There is always statistical uncertainty around most aspects of a cat model as developing stochastic events, vulnerability functions, hazard lookups and calculating financial losses will all contain elements of uncertainty.
Including uncertainty is always recommended when using a cat model for commercial purposes, especially for pricing and setting risk appetites. However, removing uncertainty could be useful during model validation exercises and when validating its impact.

What is demand surge and what impact does it have on the losses?
----------------------------------------------------------------

Demand Surge refers to the increase in rebuilding costs following a severe cat event, usually when a large area has been affected. The demand for rebuilding increases disproportionately to the supply of materials and available labour and so the costs increases.
The impact of demand surge on the losses is dependent on multiple factors such as severity of the event, location of the event and the size and type of the area affected. As a basic rule of thumb, demand surge can increase losses by up to 20% in some cases as an approximation.

What does the Oasis API do?
---------------------------

The Oasis Application Programming Interface (API), is an interface that enables systems to “talk” to each other which is a key function when a user wants to utilise multiple external tools in one place, such as an internal business system. Oasis models can be run directly using the API and the results can be captured without the need to access any third-party tools directly.

What is OED, ORD and the “Open Standard”?
-----------------------------------------

OED is the Open Exposure Database and ORD is the Open Results Database. 
These make up the “open standard” data formats used in Oasis where the exposure data being imported into a model and the results being produced by that model are consistent across all models regardless of the vendor. Historically, all input and output formats have been proprietary which makes transferring of data and analytical work between models and users difficult. 
The “open standards” are governed and curated by a steering committee that is made up of participants from insurers, reinsurers, brokers and cat model vendors. The “open standard” is a market initiative to increase transparency and efficiency throughout the cat modelling community.
