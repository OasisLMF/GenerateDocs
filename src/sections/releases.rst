Releases
========

On this page
------------

* :ref:`versions_releases`
* :ref:`schedule_releases`
* :ref:`updates_releases`
* :ref:`ODS_tools_releases`

|

.. _versions_releases:

Current Stable Versions
***********************

----

* ``1.15.x`` `backports/1.15.x <https://github.com/OasisLMF/OasisLMF/tree/backports/1.15.x>`_ From Feb 2021

* ``1.23.x`` `backports/1.23.x <https://github.com/OasisLMF/OasisLMF/tree/backports/1.23.x>`_ From Dec 2021

* ``1.26.x`` `backports/1.26.x <https://github.com/OasisLMF/OasisLMF/tree/backports/1.26.x>`_ From Jun 2022

* ``1.27.x`` `backports/1.27.x <https://github.com/OasisLMF/OasisLMF/tree/backports/1.27.x>`_ From Jan 2023

* ``1.28.x`` `backports/1.28.x <https://github.com/OasisLMF/OasisLMF/tree/backports/1.28.x>`_ From Jul 2023

|

.. _schedule_releases:

Release Schedule
****************

----

* **Until end of 2023** - Until the year 2023, we will be following a six-month release cycle for our stable versions. During each 
  six-month period, we will release a new stable version with added features. These updates will adhere to the Semantic Versioning 
  (semver) format and will increment the minor version number. That version of oaisislmf is then 'frozen' into a branch matching 
  the new version number, so on release 1.28.0 the code base is copied to a branch ``backports/1.28.x`` where backported features 
  and fixes are applied.

* **After 2023** - Starting from 2023, we will transition to a yearly release cycle for our stable versions. Each year, we will 
  release a new stable version with additional features.

A full, detailed list of the changes from each release can be found `here <https://github.com/OasisLMF/OasisLMF/releases>`_.

|

.. _updates_releases:

Monthly Updates
***************

----

Every month, we will provide updates to the latest stable version. These updates will include new compatible features and bug 
fixes, ensuring that our software remains up-to-date and reliable.

During the monthly update, if any bug fixes are required, they will also be applied to the older stable versions. This approach 
guarantees that all stable versions receive necessary bug fixes, while maintaining a consistent output numbers for that stable 
version.

|

.. _ODS_tools_releases:

ODS Tools compatability
***********************

----

OasisLMF uses the ods_tools package to read exposure files and the setting files The version compatible with each OasisLMF is 
manage in the requirement files. Below is the summary:

* ``OasisLMF 1.23.x`` or before => no ``ods_tools``
* ``OasisLMF 1.26.x`` => uses ``ods_tools 2.3.2``
* ``OasisLMF 1.27.0`` => uses ``ods_tools 3.0.0`` or later
* ``OasisLMF 1.27.1`` => uses ``ods_tools 3.0.0`` or later
* ``OasisLMF 1.27.2`` => uses ``ods_tools 3.0.4`` or later

|
