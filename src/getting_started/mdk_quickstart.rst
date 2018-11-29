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

* ``test`` - for testing models via the Oasis API and also testing keys servers; this is not fully implemented at this stage
* ``bin`` - for generating and processing model binary files
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

Source -> canonical file transformation
_______________________________________

The ``transform-source-to-canonical`` subcommand can be used to transform a source exposure or accounts CSV file (in either EDM or OED format) to an appropriate canonical Oasis format, provided certain model specific resources are provided as arguments. The transformation is done by converting the source CSV to XML, applying an XSLT transformation, and an optional XSD schema validation (if one is provided), and converting the transformed XML back to CSV.

The command can be run either by providing all the arguments directly in the invocation, or by defining them as keys in a (JSON) configuration file and using the ``-C`` (or ``--config``) option. It is probably simpler to use the first option.
::

    oasislmf model transform-source-to-canonical [-C /path/to/configuration/file] |
                                                 -s /path/to/source/file
                                                 -x /path/to/transformation/file
                                                 [-y 'exposures'|'accounts']
                                                 [-v /path/to/validation/file]
                                                 [-o /path/to/output/file]

The mandatory arguments are the source and (XSLT) transformation file paths, while the (XSD) validation and output file paths are optional. The ``-y`` option can be used to indicate type of the source file - whether it contains exposure (``exposures``) or accounts, i.e. financial terms, (``accounts``) - the default is ``exposures``. If no output file path is provided then it will be created in the working directory where the command was run, with a default filename of ``canexp.csv`` for exposure or ``canacc.csv`` for accounts. If using a configuration file it should be a JSON file with the keys ``source_file_path`` and ``transformation_file_path``, and optionally ``source_file_type``, ``validation_file_path``, ``output_file_path``.


We describe an example using a `sample PiWind OED source file <https://github.com/OasisLMF/OasisPiWind/blob/master/tests/data/SourceLocOEDPiWind2.csv>`_ with 2 exposures. Here's the source file.
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

