Financial modelling and exposure data
=====================================

.. note:: 
    To date, the focus of the Oasis Financial Module has been to provide a complete solution for direct insurance policies.
    In 2018, a major development focus is to start building out reinsurance capabilities.
    We are working with the Oasis community to prioritise, specify and test the data structures and calculation methodologies.

Insurance policies have terms and conditions applying at many different levels and with many variations in the calculation rules. 
Here are some examples that show makes the calculations tricky. 
The diagrams work from bottom to top, with the ground up losses coming in at the bottom and the insurance losses streaming out at the top.

Simplest: 
    This is when the ground-up losses are accumulated to the highest level and policy terms and conditions applied. 
    There could be many policies (termed “layers” in Oasis) applicable to the same portfolio (termed a “programme” in Oasis).

.. figure:: /images/fm_simplest.png
    :alt: Simplest FM example

Simple: 
    The next level of complexity is to include coverage terms, such as location buildings or contents deductibles, and then aggregate the net figures up to the policy level for the excess of loss. 
    The next step is to apply location terms such as limits, before summarising up to the location level after coverage deductibles. 
    The results of these calculations are then fed up to the overall policy terms.

.. figure:: /images/fm_simple.png
    :alt: Simple FM example    
    
Less Simple: 
    Another stage of complication is when the higher level is based on aggregations which have already been suppressed in calculating a lower level. 
    An example is where policy coverage deductibles and limits are applied after location terms. 
    Here the post-location losses have to be “back-allocated” to the coverage level, usually in proportion to the proportion of coverage to the post-location losses, and then aggregated.

.. figure:: /images/fm_less_simple.png
    :alt: Less simple FM example    
    
Complex: 
    And then we have a myriad of cases where terms and conditions apply at many levels, from location coverage to location to locational areas such as municipalities) to areas where perils are sub-limited, to policy coverages and then to the policy as a whole.
    At each level there can be different policy terms applied. 
    These can be very complex indeed reflecting the appetite of underwriters to put in conditions whenever there is a loss!

.. figure:: /images/fm_complex.png
    :alt: Complex FM example

The Oasis kernel's Financial Module is a data-driven process design for calculating the losses on (re)insurance contracts. 
It has an abstract design in order to cater for the many variations in contract structures and terms. 
The way Oasis works is to be fed data in order to execute calculations, so for the insurance calculations it needs to know the structure, parameters and calculation rules to be used. 
This data must be provided in the files used by the Oasis Financial Module:

fm_programme: 
    defines how coverages are grouped into accounts and programmes

fm_profile: 
    defines the layers and terms

fm_policytc: 
    defines the relationship of the contract layers

fm_xref: 
    specifies the summary level of the output losses

A full specification of the Financial Module can be found in the ktools documentation :ref:`/docs/general`.

The Oasis platform also provides functionality to consume exposure data in commonly used formats, and transform this to the abstract data structures used at run time.
