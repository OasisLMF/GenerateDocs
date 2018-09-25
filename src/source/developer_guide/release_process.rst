Release process
===============

Continuous Integration
----------------------

A critical feature of any production system is a robust process for building, testing and deploying new releases. 
Of critical importance for a catastrophe modelling platform is that software updates do not materially impact the modelled numbers, and if they do then a robust change management process is required. 
We use Jenkins as a Continuous Integration system, included regession of the models in the Oasis Model Library.
A schematic of our build process is shown below:

.. figure:: /images/oasis_ci.png
    :alt: Oasis build process

Changelogs for each component can be viewed in the relevant :ref:`github_repositories`.


Releases Process and Versioning
-------------------------------

We operate on a monthly release cycle. 
We use semantic versioning (`SemVer <https://semver.org/>`_) to label our releases. 
Given a version number MAJOR.MINOR.PATCH, increment the:

* MAJOR version when you make incompatible API changes,
* MINOR version when you add functionality in a backwards-compatible manner, and
* PATCH version when you make backwards-compatible bug fixes.

The latest stable builds are listed in :ref:`github_repositories`.

Features
--------
Our development work is prioritized to maximise value to the Oasis community. 
We rank the features based on discussions with the membership, balancing with technology requirements and the logical sequencing required in some areas. 
We maintain a backlog of main features with a target schedule for a 12-month rolling horizon. 
The backlog is available for review and comment `here <https://trello.com/b/7O0krVYr/backlog>`_.
