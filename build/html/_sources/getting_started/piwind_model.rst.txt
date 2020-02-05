PiWind - toy model
====================

Oasis has developed a toy model, PiWind, available `here <https://github.com/OasisLMF/OasisPiWind>`_.
PiWind is a wind storm model for a small area of the UK.
The data is mocked up to illustrate the Oasis data formats and functionality, and is not meant to be a usable risk model.

There are three main components to a catastrophe risk model deployed in Oasis. 
A fuller discussion of the components of a hazard model can be found in :ref:`what_is_a_catastrophe_model`.

* Hazard footprint data: 
    This holds the hazard intensity data for each event in the stochastic event set. 
    The hazard intensity footprint is defined on a model specific geospatial grid, and each grid cell is assigned an AreaPerilID.
    Note that a model may cover multiple perils, each with a different area peril grid. For example, a hurricane model will usually cover both wind and storm surge perils. Each peril has a defined hazard intensity measure, such as wind speed in metres per second.
    The Oasis Platform allows uncertainty to be specified in the hazard intensity measure in a particular grid cell for each event.

* Vulnerability data 
    This holds curves that define expected levels of damage as a proportion of replacement value given the level of hazard intensity for structures of different characteristics.
    For example, a wood-framed building will have a different vulnerability to wind damage as compared to a building of concrete construction.
    The curves also define the uncertainty in damage at different hazard levels.
    The Oasis Platform does not make any assumptions about the form of the damage distributions and represents them as discrete distributions.

* Keys lookup logic 
    This is model specific logic that maps a set of exposure attributes into the model specific grid and vulnerability type.
    A unique mapping is made for each location, coverage and peril combination. 
    This also provides informative messages about any exposures that will not be modelled.
    An exposure may not be modelled if there is insufficiently detailed address information, or if the exposure is not within the geographic scope of the model.
    
The PiWind model is a very small example model, so it's files can be saved to a GitHub repository and easilly queried.
For real models the data sets can get much larger, in such cases more than 1 TB for a single model.
The following link is to a Jupyter notebook that illustrates the setup of the PiWind model and how it can be ran using the Oasis MDK:
`Running PiWind <https://hub.gke.mybinder.org/user/oasislmf-oasispiwind-qjo1vxcf/notebooks/running_piwind.ipynb>`_
