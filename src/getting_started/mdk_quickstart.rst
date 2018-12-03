Model Development Kit  (MDK) Quickstart Guide
=============================================

The model development kit (MDK) is the `oasislmf <https://pypi.org/project/oasislmf/>`_ Python package. It provides various features and tools for developing, implementing, running and testing Oasis models. Installation instructions are provided on the PyPI package home page. This quickstart guide will cover the following topics.

* Command line interface
* Implementing and testing lookups
* Working with Oasis models as objects
* Exposure management
* Utilities

Command line interface (CLI)
----------------------------

The package provides a command line interface (CLI) with different groups of commands for doing different things.

* ``test`` - (to be deprecated) for testing models via the Oasis API and also testing keys servers
* ``bin`` - for generating and processing model ktools-compatible binary files from input CSV files, and also validating the file conversion tools
* ``model`` - various subcommands for working with models locally, including transforming source exposure and/or accounts (financial terms) files to the canonical Oasis format, writing an Rtree file index for the area peril lookup component of the built-in lookup framework, writing keys files from lookups, generating Oasis input CSV files (GUL + optionally FM), generating losses from a preexisting set of Oasis input CSV files, running a model end-to-end
* ``version`` - displays the installed package version
* ``config`` - displays the MDK configuration file format for running a model end-to-end (via ``model run``)

Available subcommands within a command group can be explored by using the ``-h`` or ``--help`` option, e.g.
::

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

Model
~~~~~

The ``model`` commands are the most important in terms of functionality, so we start with a description of how these can be used, with examples using the `PiWind <https://github.com/OasisLMF/OasisPiWind>`_ demonstration model.

Source -> canonical exposure/accounts file transformation
_________________________________________________________

The ``transform-source-to-canonical`` subcommand can be used to transform a source exposure or accounts CSV file (in either EDM or OED format) to an appropriate canonical Oasis format. The transformation is done by converting the source CSV to XML, applying an XSLT transformation, and an optional XSD schema validation (if one is provided), and converting the transformed XML back to CSV.

The command can be run either by providing all the arguments directly in the invocation, or by defining them as keys in a (JSON) command configuration file and using the ``-C`` (or ``--config``) option. It is probably simpler to use the first option.
::

    oasislmf model transform-source-to-canonical [-C /path/to/cmd/configuration/file] |
                                                 -s /path/to/source/file
                                                 -x /path/to/transformation/file
                                                 [-y 'exposures'|'accounts']
                                                 [-v /path/to/validation/file]
                                                 [-o /path/to/output/file]

The mandatory arguments are the source and (XSLT) transformation file paths, while the (XSD) validation and output file paths are optional. The ``-y`` option can be used to indicate type of the source file - whether it contains exposure (``exposures``) or accounts, i.e. financial terms, (``accounts``) - the default is ``exposures``. If no output file path is provided then it will be created in the working directory where the command was run, with a default filename of ``canexp.csv`` for exposure or ``canacc.csv`` for accounts. If a configuration file is used it should define the keys ``source_file_path`` and ``transformation_file_path``, and optionally ``source_file_type``, ``validation_file_path``, ``output_file_path``.


We describe an example using the following `sample PiWind OED source file <https://github.com/OasisLMF/OasisPiWind/blob/master/tests/data/SourceLocOEDPiWind2.csv>`_ with 2 exposures.
::

	AccNumber,LocNumber,LocName,LocGroup,IsPrimary,IsTenant,BuildingID,LocInceptionDate,LocExpiryDate,PercentComplete,CompletionDate,CountryCode,Latitude,Longitude,StreetAddress,PostalCode,City,SubArea2,SubArea,LowResCresta,HighResCresta,AreaCode,AreaName,AddressMatch,GeocodeQuality,Geocoder,OrgOccupancyScheme,OrgOccupancyCode,OrgConstructionScheme,OrgConstructionCode,OccupancyCode,ConstructionCode,YearBuilt,NumberOfStories,NumberOfBuildings,FloorArea,FloorAreaUnit,LocUserDef1,LocUserDef2,LocUserDef3,LocUserDef4,LocUserDef5,LocPerilsCovered,BuildingTIV,OtherTIV,ContentsTIV,BITIV,BIPOI,LocCurrency,LocGrossPremium,LocTax,LocBrokerage,LocNetPremium,NonCatGroundUpLoss,LocParticipation,PayoutBasis,ReinsTag,CondTag,CondPriority,LocDedCode1Building,LocDedType1Building,LocDed1Building,LocMinDed1Building,LocMaxDed1Building,LocDedCode2Other,LocDedType2Other,LocDed2Other,LocMinDed2Other,LocMaxDed2Other,LocDedCode3Contents,LocDedType3Contents,LocDed3Contents,LocMinDed3Contents,LocMaxDed3Contents,LocDedCode4BI,LocDedType4BI,LocDed4BI,LocMinDed4BI,LocMaxDed4BI,LocDedCode5PD,LocDedType5PD,LocDed5PD,LocMinDed5PD,LocMaxDed5PD,LocDedCode6All,LocDedType6All,LocDed6All,LocMinDed6All,LocMaxDed6All,LocLimitCode1Building,LocLimitType1Building,LocLimit1Building,LocLimitCode2Other,LocLimitType2Other,LocLimit2Other,LocLimitCode3Contents,LocLimitType3Contents,LocLimit3Contents,LocLimitCode4BI,LocLimitType4BI,LocLimit4BI,LocLimitCode5PD,LocLimitType5PD,LocLimit5PD,LocLimitCode6All,LocLimitType6All,LocLimit6All,BIWaitingPeriod,LocPeril,YearUpgraded,SurgeLeakage,SprinklerType,RoofCover,RoofYearBuilt,RoofGeometry,RoofEquipment,RoofFrame,RoofMaintenance,BuildingCondition,RoofAttachedStructure,RoofDeck,RoofPitch,RoofAnchorage,RoofDeckAttachment,RoofCoverAttachment,GlassType,LatticeType,FloodZone,SoftStory,Basement,BasementLevelCount,WindowProtection,FoundationType,WallAttachedStructure,AppurtenantStructure,ConstructionQuality,GroundEquipment,EquipmentBracing,Flashing,BuildingShape,ShapeIrregularity,Pounding,Ornamentation,SpecialEQConstruction,Retrofit,CrippleWalls,FoundationConnection,ShortColumn,Fatigue,Cladding,BIPreparedness,BIRedundancy,BuildingElevation,BuildingElevationUnit,Datum,GroundElevation,GroundElevationUnit,Tank,Redundancy,InternalPartition,ExternalDoors,Torsion,MechanicalEquipmentSide,ContentsWindVuln,ContentsFloodVuln,ContentsQuakeVuln,SmallDebris,FloorsOccupied,FloodDefenseElevation,FloodDefenseElevationUnit,FloodDebrisResilience,BaseFloodElevation,BaseFloodElevationUnit,BuildingHeight,BuildingHeightUnit,BuildingValuation,TreeExposure,Chimney,BuildingType,Packaging,Protection,SalvageProtection,ValuablesStorage,DaysHeld,BrickVeneer,FEMACompliance,CustomFloodSOP,CustomFloodZone,MultiStoryHall,BuildingExteriorOpening,ServiceEquipmentProtection,TallOneStory,TerrainRoughness,NumberOfEmployees,Payroll
	+11111,1,10002082046,0,0,0,0,0,0,0,0,0,52.76698052,-0.895469856,0,LE13 0HL,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1000,5000,1900,2,1,0,0,0,0,0,0,0,64,220000,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,100,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,198000,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
	+11111,2,10002082047,0,0,0,0,0,0,0,0,0,52.76697956,-0.89536613,0,LE13 0HL,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1000,5000,1900,2,1,0,0,0,0,0,0,0,64,790000,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,100,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,711000,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0

The transformation command, with command logging output, is
::

	$ oasislmf model transform-source-to-canonical -s /path/to/OasisPiWind/tests/data/SourceLocOEDPiWind2.csv -x /path/to/OasisPiWind/flamingo/PiWind/Files/TransformationFiles/MappingMapToOED_CanLocA.xslt -o /path/to/output-dir/canexp-oed-piwind.csv

	Generating a canonical exp file /path/to/output-dir/canexp-oed-piwind.csv from source exp file /path/to/OasisPiWind/tests/data/SourceLocOEDPiWind2.csv

	Output file /path/to/output-dir/canexp-oed-piwind.csv successfully generated

This will produce the following canonical OED file.
::

	ROW_ID,AccNumber,LocNumber,LocName,LocGroup,IsPrimary,IsTenant,BuildingID,LocInceptionDate,LocExpiryDate,PercentComplete,CompletionDate,CountryCode,Latitude,Longitude,StreetAddress,PostalCode,City,AreaCode,AreaName,GeogScheme1,GeogName1,GeogScheme2,GeogName2,GeogScheme3,GeogName3,GeogScheme4,GeogName4,GeogScheme5,GeogName5,AddressMatch,GeocodeQuality,Geocoder,OrgOccupancyScheme,OrgOccupancyCode,OrgConstructionScheme,OrgConstructionCode,OccupancyCode,ConstructionCode,YearBuilt,NumberOfStories,NumberOfBuildings,FloorArea,FloorAreaUnit,LocUserDef1,LocUserDef2,LocUserDef3,LocUserDef4,LocUserDef5,LocPerilsCovered,BuildingTIV,OtherTIV,ContentsTIV,BITIV,BIPOI,LocCurrency,LocGrossPremium,LocTax,LocBrokerage,LocNetPremium,NonCatGroundUpLoss,LocParticipation,PayoutBasis,ReinsTag,CondTag,CondPriority,LocDedCode1Building,LocDedType1Building,LocDed1Building,LocMinDed1Building,LocMaxDed1Building,LocDedCode2Other,LocDedType2Other,LocDed2Other,LocMinDed2Other,LocMaxDed2Other,LocDedCode3Contents,LocDedType3Contents,LocDed3Contents,LocMinDed3Contents,LocMaxDed3Contents,LocDedCode4BI,LocDedType4BI,LocDed4BI,LocMinDed4BI,LocMaxDed4BI,LocDedCode5PD,LocDedType5PD,LocDed5PD,LocMinDed5PD,LocMaxDed5PD,LocDedCode6All,LocDedType6All,LocDed6All,LocMinDed6All,LocMaxDed6All,LocLimitCode1Building,LocLimitType1Building,LocLimit1Building,LocLimitCode2Other,LocLimitType2Other,LocLimit2Other,LocLimitCode3Contents,LocLimitType3Contents,LocLimit3Contents,LocLimitCode4BI,LocLimitType4BI,LocLimit4BI,LocLimitCode5PD,LocLimitType5PD,LocLimit5PD,LocLimitCode6All,LocLimitType6All,LocLimit6All,BIWaitingPeriod,LocPeril,YearUpgraded,SurgeLeakage,SprinklerType,RoofCover,RoofYearBuilt,RoofGeometry,RoofEquipment,RoofFrame,RoofMaintenance,BuildingCondition,RoofAttachedStructure,RoofDeck,RoofPitch,RoofAnchorage,RoofDeckAttachment,RoofCoverAttachment,GlassType,LatticeType,FloodZone,SoftStory,Basement,BasementLevelCount,WindowProtection,FoundationType,WallAttachedStructure,AppurtenantStructure,ConstructionQuality,GroundEquipment,EquipmentBracing,Flashing,BuildingShape,ShapeIrregularity,Pounding,Ornamentation,SpecialEQConstruction,Retrofit,CrippleWalls,FoundationConnection,ShortColumn,Fatigue,Cladding,BIPreparedness,BIRedundancy,BuildingElevation,BuildingElevationUnit,Datum,GroundElevation,GroundElevationUnit,Tank,Redundancy,InternalPartition,ExternalDoors,Torsion,MechanicalEquipmentSide,ContentsWindVuln,ContentsFloodVuln,ContentsQuakeVuln,SmallDebris,FloorsOccupied,FloodDefenseElevation,FloodDefenseElevationUnit,FloodDebrisResilience,BaseFloodElevation,BaseFloodElevationUnit,BuildingHeight,BuildingHeightUnit,BuildingValuation,TreeExposure,Chimney,BuildingType,Packaging,Protection,SalvageProtection,ValuablesStorage,DaysHeld,BrickVeneer,FEMACompliance,CustomFloodSOP,CustomFloodZone,MultiStoryHall,BuildingExteriorOpening,ServiceEquipmentProtection,TallOneStory,TerrainRoughness,NumberOfEmployees,Payroll
	1,11111,1,10002082046,0,0,0,0,0,0,0,0,0,52.76698052,-0.895469856,0,LE13 0HL,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1000,5000,1900,2,1,0,0,0,0,0,0,0,64,220000,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,100,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,198000,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
	2,11111,2,10002082047,0,0,0,0,0,0,0,0,0,52.76697956,-0.89536613,0,LE13 0HL,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1000,5000,1900,2,1,0,0,0,0,0,0,0,64,790000,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,100,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,711000,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0

Canonical -> model exposure file transformation
_______________________________________________

The ``transform-canonical-to-model`` subcommand can be used to transform a canonical exposure CSV file (in either EDM or OED format) to a format that can be processed by the model lookup. The transformation is done by converting the source CSV to XML, applying an XSLT transformation, and an optional XSD schema validation (if one is provided), and converting the transformed XML back to CSV.

The command can be run either by providing all the arguments directly in the invocation, or by defining them as keys in a (JSON) command configuration file and using the ``-C`` (or ``--config``) option. It is probably simpler to use the first option.
::

    oasislmf model transform-canonical-to-model [-C /path/to/cmd/configuration/file] |
                                                 -c /path/to/canonical/file
                                                 -x /path/to/transformation/file
                                                 [-v /path/to/validation/file]
                                                 [-o /path/to/output/file]

The mandatory arguments are the canonical and (XSLT) transformation file paths, while the (XSD) validation and output file paths are optional. If no output file path is provided then it will be created in the working directory where the command was run, with a default filename of ``modexp.csv``. If a configuration file is used it define the keys ``canonical_exposures_file_path`` and ``transformation_file_path``, and optionally ``validation_file_path`` and ``output_file_path``.

We can use the sample PiWind OED canonical exposure file generated in the example above as the source file. The transformation command, with command logging output, is
::

	oasislmf model transform-canonical-to-model -c /path/to/canexp-oed-piwind.csv -x /path/to/OasisPiWind/flamingo/PiWind/Files/TransformationFiles/MappingMapToOED_piwind_modelloc.xslt -o /path/to/output-dir/modexp-oed-piwind.csv

	Generating a model exposures file /path/to/output-dir/modexp-oed-piwind.csv from canonical exposures file /path/to/canexp-oed-piwind.csv

	Output file /path/to/output-dir/modexp-oed-piwind.csv successfully generated

This will produce the following canonical OED file.
::

	ROW_ID,ID,LAT,LON,COVERAGE,CLASS_1,CLASS_2
	1,1,52.76698052,-0.895469856,1,R,R
	2,2,52.76697956,-0.89536613,1,R,R

Generating keys files
_____________________

The ``generate-keys`` subcommand can be used to generate keys files from model lookups - the keys file links the model exposure with the model hazard and vulnerability components by defining an area peril ID and a vulnerability ID for each location/exposure, for all combinations of peril and coverage types supported by the model. There are two ways of running the command, depending on whether the model lookup is a custom lookup implementing the base Oasis lookup (``OasisBaseKeysLookup``) or the data-driven built-in lookup provided within the package (as with PiWind). For the custom lookups the command syntax is given by
::

    oasislmf model generate-keys [-C /path/to/cmd/configuration/file] |
                                 -v /path/to/model/version/file
                                 -d /path/to/keys/or/lookup/data
                                 -l /path/to/lookup/package
                                 -x /path/to/model/exposure/file
                                 [-f "oasis" | "json" ]
                                 [-k /path/to/keys/file]
                                 [-e /path/to/keys/errors/file]

All file path arguments can be given relative or absolute to the wher the command is run. The model version file should be a single line CSV file defining the model supplier ID, model ID and version string, e.g.::

    OasisLMF,PiWind,0.0.0.1

The ``-f`` option is used to indicate whether the keys file should be an Oasis style keys file (``"oasis"``; this is the default option), which has the format
::

    LocID,PerilID,CoverageTypeID,AreaPerilID,VulnerabilityID
    ..
    ..

or simply a listing of the lookup-generated keys, which are dicts with the following format
::

	{
	    'id': <loc. ID>,
	    'peril_id': <sub peril ID - must be a code that matches relevant Oasis flag>,
	    'coverage_type': <cov. type - must be a code that matches relevant Oasis flag>,
	    'area_peril_id': <area peril ID>,
	    'vulnerability_id': <vuln. ID>,
	    'message': <an optional message - best to keep it short or copy status flag>,
	    'status': <status flag - 'success', 'nomatch' or 'fail'
	}

The command also generates a second file called the keys errors file, which lists all those locations/exposures for which the model lookup has been unable to assign area peril and vulnerability IDs either because of an internal error or because of insufficient or incomplete data. With the ``"oasis"`` output option the keys errors file has the following format
::

	LocID,PerilID,CoverageTypeID,Message
	..
	..

The keys and keys errors file paths are optional - if either or both are not provided then timestamped files are created in the working directory where the command was run. If using a (JSON) command configuration file the file must define the following keys: ``model_version_file_path``, ``keys_data_path``, ``lookup_package_path``, and optionally ``keys_format``, ``model_exposures_file_path``, ``keys_file_path``, ``keys_errors_file_path``.

With built-in lookups like PiWind, which are automated lookups entirely driven by data and a lookup configuration file, and do not require a model version file, custom lookup source code or data, the command syntax is given by
::

    oasislmf model generate-keys [-C /path/to/cmd/configuration/file] |
                                 -g /path/to/lookup/configuration/file
                                 [-f "oasis" | "json" ]
                                 -x /path/to/model/exposure/file
                                 [-k /path/to/keys/file]
                                 [-e /path/to/keys/errors/file]

The lookup configuration file is better understood in the context of the built-in lookup framework, which will be described in more detail later on. But essentially the configuration file defines the location of the lookup data, and also the peril, coverage type and vulnerability components of the model. The `PiWind lookup configuration <https://github.com/OasisLMF/OasisPiWind/blob/master/keys_data/PiWind/lookup.json>`_ can be used as a template.

Here's an example of generating a PiWind keys file using this command, starting with a sample 10 row model exposure file.
::

	ID,LAT,LON,COVERAGE,CLASS_1,CLASS_2
	1,52.76698052,-0.895469856,1,R,R
	2,52.76697956,-0.89536613,1,R,R
	3,52.76697845,-0.895247587,1,R,R
	4,52.76696096,-0.895473908,1,R,R
	5,52.76695804,-0.895353484,1,R,R
	6,52.76695885,-0.89524749,1,R,R
	7,52.7670776,-0.895274721,1,R,R
	8,52.76712254,-0.895273583,1,R,R
	9,52.76718545,-0.895271991,1,R,R
	10,52.76724836,-0.895270399,1,R,R

The command, with logging output, is given below.
::

	oasislmf model generate-keys -g /path/to/OasisPiWind/keys_data/PiWind/lookup.json -x /path/to/OasisPiWind/tests/data/ModelLocPiWind10.csv

	Getting model info and lookup
	STARTED: oasislmf.keys.lookup.__init__
	STARTED: oasislmf.keys.lookup.__init__
	COMPLETED: oasislmf.keys.lookup.__init__ in 0.0s
	STARTED: oasislmf.keys.lookup.__init__
	STARTED: oasislmf.keys.lookup.__init__
	COMPLETED: oasislmf.keys.lookup.__init__ in 0.0s
	COMPLETED: oasislmf.keys.lookup.__init__ in 0.0s
	STARTED: oasislmf.keys.lookup.__init__
	STARTED: oasislmf.keys.lookup.__init__
	COMPLETED: oasislmf.keys.lookup.__init__ in 0.0s
	STARTED: oasislmf.keys.lookup.get_vulnerabilities
	COMPLETED: oasislmf.keys.lookup.get_vulnerabilities in 0.05s
	COMPLETED: oasislmf.keys.lookup.__init__ in 0.05s
	COMPLETED: oasislmf.keys.lookup.__init__ in 0.06s
		{u'model_version': u'0.0.0.1', u'model_id': u'PiWind', u'supplier_id': u'OasisLMF'}, <oasislmf.keys.lookup.OasisLookup object at 0x1053b3b10>

	Saving keys records to file
	STARTED: oasislmf.keys.lookup.bulk_lookup
	COMPLETED: oasislmf.keys.lookup.bulk_lookup in 0.0s

	10 successful results saved to keys file /path/to/oasislmf-piwind-0.0.0.1-keys-20181203174128.csv

	0 unsuccessful results saved to keys errors file /path/to/oasislmf-piwind-0.0.0.1-keys-errors-20181203174128.csv

	Finished keys files generation (0.025 seconds)

There are no errors in the keys, and the generated keys file should look as below.
::

	LocID,PerilID,CoverageTypeID,AreaPerilID,VulnerabilityID
	1,1,1,54,3
	2,1,1,54,3
	3,1,1,54,3
	4,1,1,54,3
	5,1,1,54,3
	6,1,1,54,3
	7,1,1,54,3
	8,1,1,54,3
	9,1,1,54,3
	10,1,1,54,3