Post Loss Amplification
=======================

There is a requirement in the Nazare project to include a Post Loss Amplification factor to losses produced by the GUL 
calculation component (either gulpy, gulmc or gulcalc). This represents an uplift to the loss based in inflated costs to 
make good damage following a major event, since costs of labour, materials, loss adjustment expenses, etc. go up with demand.

The proposal is to have a static, event-by-event based uplift factor after GUL calculation based on intensity and size of 
event as a whole. The factor also needs to take into account location (to some degree) and coverage type.

Model developers will be able to provide an additional (optional) uplift factor file and if the file is present, GUL losses 
(sample and NI) should be uplifted by supplied factor per event

The file will include the following data:

* event_id
* uplift_area_id
* coverage_type
* uplift_factor

In addition to the uplift factor file, modellers can provide a mapping file from uplift_area_id to OED field(s) and values. 
This will allow, say, a modeller to provide, say, Country based uplift factors or custom zones to be mapped from a FlexiLoc 
field in the OED file to be defined.

Total loss should not capped at TIV - i.e. losses out of the gul calculation component can be larger than TIV and FM to 
behave as normal - i.e. not affected

Runtime user supplied secondary-factor option are also required. This would involve a user providing an additional, flat 
factor to be applied to the uplift factor from the file. For example:

|

.. image:: /images/post_loss_amplification_table.png
    :width: 400 px
    :align: center
|

The uplift calculation should apply after the GUL calculation and should be it's own module so that it can be applied to 
gulcalc, gulpy or gulmc...or complex model wrapper implementations. However, if elements from the logic can be inherited by 
gulpy/gulmc to improve performance, this would also be an option for development.
