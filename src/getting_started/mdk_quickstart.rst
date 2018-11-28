Model Development Kit  (MDK) Quickstart Guide
=============================================

The model development kit (MDK) is the `oasislmf <https://pypi.org/project/oasislmf/>`_ Python package. It provides various features and tools for developing, implementing, running and testing models compatible with the Oasis framework. Installation instructions are provided on the PyPI package home page. This quickstart guide will cover the following topics.

* Command line interface
* Implementing and testing lookups
* Working with Oasis models as objects
* Exposure management

Command line interface (CLI)
----------------------------

The package provides a command line interface (CLI) with different groups of commands for doing different things.

* `test` - for testing models via the Oasis API and also testing keys servers; this is not fully implemented at this stage
* `bin` - for generating and processing model binary files
* `model` - various subcommands for working with models locally, including transforming source exposure and/or accounts (financial terms) files to the canonical Oasis format, writing an Rtree file index for the area peril lookup component of the built-in lookup framework, writing keys files from lookups, generating Oasis input CSV files (GUL + optionally FM), generating losses from a preexisting set of Oasis input CSV files, running a model end-to-end
* `version` - displays the installed package version
* `config` - displays the MDK configuration file format for running a model end-to-end (via `model run`)

Available subcommands within a command group can be explored by using the `-h` or `--help` switch, e.g.::

	$ oasislmf model --help
    ...
	    transform-source-to-canonical
	                        transform-source-to-canonical
	    run                 run
	    transform-canonical-to-model
	                        transform-canonical-to-model
	    generate-keys       generate-keys
	    generate-peril-areas-rtree-file-index
	                        generate-peril-areas-rtree-file-index
	    generate-oasis-files
	                        generate-oasis-files
	    generate-losses     generate-losses

	optional arguments:
	  -h, --help            show this help message and exit
	  -V, --verbose         Use verbose logging.
	  -C CONFIG, --config CONFIG
	                        The oasislmf config to load
