Simulation methodology
======================

The Oasis kernel provides a robust loss simulation engine for catastrophe modelling.
Insurance practitioners are used to dealing with losses arising from events. 
These losses are numbers, not distributions. 
Policy terms are applied to the losses individually and then aggregated and further conditions or reinsurances applied.
Oasis takes the same perspective, which is to generate individual losses from the probability distributions.
The way to achieve this is random sampling called “Monte-Carlo” sampling from the use of random numbers, as if from a roulette wheel, to solve equations that are otherwise intractable.

Modelled and empirical intensities and damage responses can show significant uncertainty, 
Sometimes this uncertainty is multi-modal, meaning that there can be different peaks of behaviour rather than just a single central behaviour.
Moreover, the definition of the source insured interest characteristics, such as location or occupancy or construction, can be imprecise. 
The associated values for event intensities and consequential damages can therefore be varied and their uncertainty can be represented in general as probability distributions rather than point values. 
The design of Oasis therefore makes no assumptions about the probability distributions and instead treats all probability distributions as probability masses in discrete bins.
This includes closed interval point bins such as the values [0,0] for no damage and [1,1] for total damage. 

The simulation approach taken by the Oasis calculation kernel computes a single cumulative distribution function (CDF) for the damage by “convolving” the binned intensity distribution with the vulnerability matrices.
Sampling can then be done against the CDF. 

.. figure:: /images/simulation_approach.png
    :alt: Oasis simulation approach
