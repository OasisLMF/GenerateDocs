Oasis Models
============

On this page
------------

* :ref:`intro_models`
* :ref:`piwind_models`



|

.. _intro_models:

Oasis Models
------------

Oasis makes available a number of example models to demonstrate how different functionality options are implemented in 
Oasis. The available models are:

----

Deterministic Model
*******************

This is a single event model which allows users to apply deterministic losses to a portfolio, defining the damage factors 
in the OED location file. It is similar to the ``exposure`` feature in the oasislmf package, but can be deployed as a model in 
it's own right to model deterministic losses which can then be passed through the Oasis financial module.

----

Paris Windstorm
****************

This is very small, single peril model used for demonstration of how to build a simple model in Oasis.

----

PiWind
******

This is the original test model in Oasis and is an example of a multi-peril model implementation representing ficticious 
events with wind and flood affecting the Town of Melton Mowbray in England.

More information on this model can be found here: :ref:`piwind_models`

----

PiWind Absolute Damage
**********************

----

PiWind Complex Model
********************

This is a version of the PiWind model which uses the complex model integreation approach to generate ground up losses in a 
custoim module, which then sits in the workflow and replaces the standard ground up loss calculation from Oasis.

----

PiWind Postcode
***************

This is a variant of the original PiWind model designed for running exposures whose locations are known at postcode level 
rather than by latitude and longitude. This model demonstrates the disaggregation features of Oasis.

----

PiWind Post Loss Amplification
******************************

This is a version of the PiWind model with post loss amplification factors applied. Major catastrophic events can 
give rise to inflated and/or deflated costs depending on that specific situation. To account for this, the ground up 
losses produced by the GUL calculation component are multiplied by post loss amplification factors, by the component 
plapy.

PiWind Single Peril
*******************

This is a simplified variant of the original PiWind model which has single peril (wind only) and would be a good basis for 
a single peril model in Oasis.

|

.. note::
    More information about these models can be found `here <https://github.com/OasisLMF/OasisModels/tree/develop>`_.


----

|

.. _piwind_models:

PiWind - toy model
------------------

----

Oasis has developed a toy model, PiWind, available `here <https://github.com/OasisLMF/OasisPiWind>`_. PiWind is a wind storm 
model for a small area of the UK. The data is mocked up to illustrate the Oasis data formats and functionality, and is not 
meant to be a usable risk model. The PiWind toy model is availible to use from `here <https://github.com/OasisLMF/
OasisModels/tree/develop/PiWind>`.

There are three main components to a catastrophe risk model deployed in Oasis. A fuller discussion of the components of a 
hazard model can be found in :doc:`modelling-methodology`.

**Hazard footprint data:**
    This holds the hazard intensity data for each event in the stochastic event set. The hazard intensity footprint is
    defined on a model specific geospatial grid, and each grid cell is assigned a unique identifier.Note that a model may 
    cover multiple perils, each with a different overlaid area peril grid. For example, a hurricane model will usually 
    cover both wind and storm surge perils. Each peril has a defined hazard intensity measure, such as wind speed in metres 
    per second.The Oasis Platform allows uncertainty to be specified in the hazard intensity measure in a particular grid 
    cell for each event.

**Vulnerability data:**
    This holds curves that define the distribution of damage as a proportion of replacement value given the level of hazard 
    intensity.Different curves as specified for structures with different building characteristics.For example, a 
    wood-framed building will have a different vulnerability to wind damage as compared to a building of concrete 
    construction.The curves also define the uncertainty in damage at different hazard levels.The Oasis Platform does not 
    make any assumptions about the form of the damage distributions and represents them all as discrete distributions.

**Keys lookup logic:**
    This is model specific logic that maps a set of exposure attributes into the model specific grid and vulnerability type.
    A unique mapping is made for each location, coverage and peril combination. The lookup also provides informative 
    messages about any exposures that will not be modelled.For example, an exposure may not be modelled if there is 
    insufficiently detailed address information or if the exposure is not within the geographic scope of the model.
    
The PiWind model is a very small example model, so it's files can be saved to a GitHub repository and easily queried.For 
real models the data sets can get much larger, in some cases more than 1 TB for a single model.The following link is to a 
Jupyter notebook that illustrates the setup of the PiWind model and how it can be ran using the Oasis MDK: 
`Running PiWind <https://mybinder.org/v2/gh/OasisLMF/OasisPiWind/master>`_.