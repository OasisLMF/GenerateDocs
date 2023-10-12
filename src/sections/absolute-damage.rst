Absolute Damage
===============

Introduction
------------

The absolute damage option allows model providers to include absolute damage amounts rather than damage factors in the 
damage bin dictionary. If the damage factors are less than or equal to 1 in the damage bin dictionary, the factor will 
be applied as normal during the loss calculation, by applying the sampled damage factor to the TIV to give a simulated 
loss; but with absolute damage factors, where the factor is greater than 1, the TIV is not used in the calculation at 
all, but rather the absolute damage is applied as the loss.

|

**Example**

    **Example 1:** if the sampled damage factor is 0.6 and the TIV is 100,000, the sampled loss will be 60,000

    **Example 2:** if the sampled damage factor is 500 and the TIV is 100,000, the sampled loss will be 500

|

An example toy model with the absolute damage factor option is availible to use from `here <https://github.com/OasisLMF/
OasisModels/tree/develop/PiWindAbsoluteDamage>`_.