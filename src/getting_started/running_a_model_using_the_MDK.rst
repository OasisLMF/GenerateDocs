Run a model using the Oasis MDK 
===============================

The Model Development Kit (MDK) is the best way to get started using the Oasis platform.
The MDK is a command line tookit providing command line access to Oasis' modelling functionality. 
It is installed as a Python package, and available from PYPI: `OasisLMF PYPI module <https://pypi.python.org/pypi/oasislmf>`_.

The OasisLMF package has the following dependencies:

*Debian*: 
    g++, build-essential, libtool, zlib1g-dev, autoconf, unixobdbc-dev
*RHEL*:
    Development Tools, zlib-devel

To install the OasisLMF package run:

.. code-block:: python

    pip install oasislmf

.. warning:: Windows is not directly supported for running the MDK.
    You can run the Oasis MDK on Linux or MacOS.
    You can only run on Windows using a docker container or Linux Subsystem (WSL).

