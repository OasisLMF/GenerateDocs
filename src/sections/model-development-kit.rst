MDK - Model Development Kit
===========================

Introduction
************

Catastrophe models are generally made up of three modules: 

• The hazard module which represents the event catalogues
• The vulnerability module which describes the damage caused by the events
• And the Exposure module which maps the items at risk into the model

These modules of are usually developed independently by people with the relevant expertise, and then brought together to be 
calibrated and validated, eventually forming a complete catastrophe model. However, it’s rare that the resulting catastrophe 
model is ready for immediate deployment and use because the model development and deployment systems are often quite 
different. This can lead to an often complex and lengthy process to convert the new model into a deployable set of assets, 
which can result in loss of fidelity.

Model Development Kit
*********************

This problem motivated us to build the Oasis Model Development Kit, which is an easy to install set of tools available as a 
Command Line Interface. The MDK is an open source python package which allows you to develop, test and run the components 
of an Oasis model from your workstation with minimal setup. The hazard, vulnerability and exposure modules can be developed 
and tested independently side by side but can also be used to run end to end analyses to test the generated Ground Up Losses 
(GUL)throughout the development. The MDK even allows you to run the Oasis financial module so that you can test insurance 
and reinsurance losses as well throughout the process. 

Deployment
**********

But the real benefit of the MDK is that it uses the same underlying components for model development which are used in the 
full deployment of an Oasis model. The OasisLMF python package forms the basis of the MDK, but it is also the same software 
which is used in a fully deployed model in Oasis. The codebase and the peripheral assets are all the same, which means that 
we can have a seamless transition from development to deployment without the need for any transformation step, and the 
associated risk of loss in fidelity.
