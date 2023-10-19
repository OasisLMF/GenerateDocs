Pytools
=======

Pytools comprises the pythons equivalent of some of the :doc:`../../sections/ktools` components. These have been developed 
to take advantage of python libraries dedicated to large compute efficiency to make running the oasis workflow more 
performant and reliable.

| 

The components of Pytools are:

* **modelpy**
* **gulpy** - more information can be found in the :ref:`gulpy-pytools` section
* **gulmc** - more information can be found in the :ref:`gulmc-pytools` section
* **fmpy** - more information can be found in the :doc:`../../sections/financial-module` section
* **plapy** - more information can be found in the :doc:`../../sections/post-loss-amplification` section

|

.. _gulpy-pytools:

gulpy
*****

----

``gulpy`` is the new tool for the computation of ground up losses that is set to replace ``gulcalc`` in the Oasis Loss Modelling 
Framework.

``gulpy`` is ready for production usage from oasislmf > version ``1.26.0``.

This document summarizes the changes introduced with ``gulpy`` in terms of command line arguments and features.

|

Command line arguments
######################

``gulpy`` offers the following command line arguments:

.. code-block:: sh

    $ gulpy -h
    usage: use "gulpy --help" for more information

    optional arguments:
    -h, --help            show this help message and exit
    -a ALLOC_RULE         back-allocation rule
    -d                    output random numbers instead of gul (default: False).
    -i FILE_IN, --file-in FILE_IN
                            filename of input stream.
    -o FILE_OUT, --file-out FILE_OUT
                            filename of output stream.
    -L LOSS_THRESHOLD     Loss treshold (default: 1e-6)
    -S SAMPLE_SIZE        Sample size (default: 0).
    -V, --version         show program version number and exit
    --ignore-file-type [IGNORE_FILE_TYPE [IGNORE_FILE_TYPE ...]]
                            the type of file to be loaded
    --random-generator RANDOM_GENERATOR
                            random number generator
                            0: numpy default (MT19937), 1: Latin Hypercube. Default: 1.
    --run-dir RUN_DIR     path to the run directory
    --logging-level LOGGING_LEVEL
                        logging level (debug:10, info:20, warning:30, error:40, critical:50). Default: 30.

|

The following gulcalc arguments were ported to gulpy with the same meaning and requirements:

.. code-block:: sh
    
    -a, -d, -h, -L, -S

|

The following gulcalc arguments were ported to gulpy but were renamed:

.. code-block:: sh

    # in gulcalc             # in gulpy
    -v                       -V, --version
    -i                       -o, --file-out

|

The following gulcalc arguments were not ported to gulpy:

.. code-block:: sh

    -r, -R, -c, -j, -s, -A, -l, -b, -v

|

The following arguments were introduced with gulpy:

.. code-block:: sh
    
    --file-in, --ignore-file-type, --random-generator, --run-dir, --logging-level

|

New random number generator: the Latin Hypercube Sampling algorithm
###################################################################

To compute random loss samples, it is necessary to draw random values from the effective damageability probability distribution 
function (PDF). Drawing random values from a given PDF is normally achieved by generating a random float value between 0 and 1 and 
by taking the inverse of the cumulative distribution function (CDF) for such random value. The collection of random values 
produced with this approach will be distributed according to the PDF.

To generate random values ``gulcalc`` uses the `Mersenne Twister generator <https://en.wikipedia.org/wiki/Mersenne_Twister>`_. In 
``gulpy``, instead, we introduce the `Latin Hypercube Sampling (LHS) <https://en.wikipedia.org/wiki/Latin_hypercube_sampling>`_ as 
the default algorithm to generate random values. Compared to the Mersenne Twister, LHS implements a sort of stratified random 
number generation that more evenly probes the range between 0 and 1, which translates in a faster convergence to the desired PDF.

In other words, in order to probe a given PDF to the same accuracy, the LHS algorithm requires a smaller number of samples than 
the Mersenne Twister.

|

Examples
########

|

Setting the Output
""""""""""""""""""

In order to run the ground-up loss calculation and stream the output to stdout in binary format, the following commands are 
equivalent:

.. code-block:: sh

    # with gulcalc                # with gulpy
    gulcalc -a0 -S10 -i -         gulpy -a0 -S10
    gulcalc -a1 -S20 -i -         gulpy -a1 -S20
    gulcalc -a2 -S30 -i -         gulpy -a2 -S30

|

Alternatively, the binary output can be redirected to file with:

.. code-block:: sh

    # with gulcalc                          # with gulpy                          # with gulpy [alternative]
    gulcalc -a0 -S10 -i gul_out.bin         gulpy -a0 -S10 -o gul_out.bin         gulpy -a0 -S10 --file-out gul_out.bin
    gulcalc -a1 -S20 -i gul_out.bin         gulpy -a1 -S20 -o gul_out.bin         gulpy -a1 -S20 --file-out gul_out.bin
    gulcalc -a2 -S30 -i gul_out.bin         gulpy -a2 -S30 -o gul_out.bin         gulpy -a2 -S30 --file-out gul_out.bin

|

Choosing the random number generator
""""""""""""""""""""""""""""""""""""

By default, ``gulpy`` uses the LHS algorithm to draw random numbers samples, which is shown to require less samples than the 
Mersenne Twister used by ``gulcalc`` when probing a given probability distribution function.

If needed, the user can force gulpy to use a specific random number generator:

.. code-block:: sh

    gulpy --random-generator 0   # uses Mersenne Twister (like gulcalc)
    gulpy --random-generator 1   # uses Latin Hypercube Sampling algorithm (new in gulpy)

|

Performance
###########

As of oasislmf version 1.0.26.rc1 ``gulpy`` is not used by default in the oasislmf MDK but it can be used by passing the ``--gulpy`` 
argument, e.g:

.. code-block:: sh

    # using gulcalc                 # using gulpy
    oasislmf model run              oasislmf model run --gulpy

|

Or to specify the use of gulpy in oasislmf json settings;

.. code-block:: JSON

    "gulpy": true

|

On a real windstorm model these are the execution times:

.. code-block:: sh

    # command                              # info on this run           # total execution time     # uses                 # speedup
    oasislmf model run                     [  10 samples  -a0 rule ]     3634 sec ~ 1h             getmodel + gulcalc     1.0x      [baseline for  10 samples]
    oasislmf model run --modelpy           [  10 samples  -a0 rule ]     1544 sec ~ 25 min         modelpy  + gulcalc     2.4x
    oasislmf model run --modelpy --gulpy   [  10 samples  -a0 rule ]     1508 sec ~ 25 min         modelpy  + gulpy       2.4x
    oasislmf model run                     [ 250 samples  -a0 rule ]    10710 sec ~ 3h             getmodel + gulcalc     1.0x      [baseline for 250 samples]
    oasislmf model run --modelpy           [ 250 samples  -a0 rule ]     8617 sec ~ 2h 23 min      modelpy  + gulcalc     1.2x
    oasislmf model run --modelpy --gulpy   [ 250 samples  -a0 rule ]     4969 sec ~ 1h 23 min      modelpy  + gulpy       2.2x

|

.. _gulmc-pytools:

gulmc
*****

----

``gulmc`` is a new tool that uses a "full Monte Carlo" approach for ground up losses calculation that, instead of drawing loss 
samples from the 'effective damageability' probability distribution (as done by calling ``eve | modelpy | gulpy``): it first 
draws a sample of the hazard intensity, and then draws an independent sample of the damage from the vulnerability function 
corresponding to the hazard intensity sample.

``gulmc`` was first introduced in oasislmf v1.27.0 and is ready for production usage from oasislmf v ``1.28.0`` onwards.


As of oasislmf version 1.27.0 ``gulmc`` is not used by default in the oasislmf MDK but it can be used by passing the ``--gulmc`` 
argument, e.g:

.. code-block:: sh

    # using gulpy                 # using gulmc
    oasislmf model run              oasislmf model run --gulmc

|

Or to specify the use of gulmc in oasislmf json settings;

.. code-block:: JSON

    "gulmc": true

|

This document summarizes the changes introduced with ``gulmc`` with respect to ``gulpy``.

.. note::   
    
    Note: features such as the Latin Hypercube Sampler introduced with ``gulpy`` are not discussed here as they are described at 
    length in the ``gulpy`` documentation.

|

Command line arguments
######################

``gulmc`` offers the following command line arguments:

.. code-block:: bash

    $ gulmc -h
    usage: use "gulmc --help" for more information

    options:
    -h, --help            show this help message and exit
    -a ALLOC_RULE         back-allocation rule. Default: 0
    -d DEBUG              output the ground up loss (0), the random numbers used for hazard sampling (1), the random numbers used for damage sampling (2). Default: 0
    -i FILE_IN, --file-in FILE_IN
                            filename of input stream (list of events from `eve`).
    -o FILE_OUT, --file-out FILE_OUT
                            filename of output stream (ground up losses).
    -L LOSS_THRESHOLD     Loss treshold. Default: 1e-6
    -S SAMPLE_SIZE        Sample size. Default: 0
    -V, --version         show program version number and exit
    --effective-damageability
                            if passed true, the effective damageability is used to draw loss samples instead of full MC. Default: False
    --ignore-correlation  if passed true, peril correlation groups (if defined) are ignored for the generation of correlated samples. Default: False
    --ignore-haz-correlation
                            if passed true, hazard correlation groups (if defined) are ignored for the generation of correlated samples. Default: False
    --ignore-file-type [IGNORE_FILE_TYPE ...]
                            the type of file to be loaded. Default: set()
    --data-server         =Use tcp/sockets for IPC data sharing.
    --logging-level LOGGING_LEVEL
                            logging level (debug:10, info:20, warning:30, error:40, critical:50). Default: 30
    --vuln-cache-size MAX_CACHED_VULN_CDF_SIZE_MB
                            Size in MB of the in-memory cache to store and reuse vulnerability cdf. Default: 200
    --peril-filter PERIL_FILTER [PERIL_FILTER ...]
                            Id of the peril to keep, if empty take all perils
    --random-generator RANDOM_GENERATOR
                            random number generator
                            0: numpy default (MT19937), 1: Latin Hypercube. Default: 1
    --run-dir RUN_DIR     path to the run directory. Default: "."

|

While all of ``gulpy`` command line arguments are present in ``gulmc`` with the same usage and functionality, the following 
command line arguments have been introduced in ``gulmc``:

.. code-block:: bash

    --effective-damageability
    --ignore-correlation
    --ignore-haz-correlation
    --data-server
    --vuln-cache-size
    --peril-filter

|
         
Comparing ``gulpy`` and ``gulmc`` output
########################################

``gulmc`` runs the same algorithm of ``eve | modelpy | gulpy``, i.e., it runs the 'effective damageability' calculation mode, 
with the same command line arguments. For example, to run a model with 1000 samples, alloc rule 1, and streaming the binary 
output to the ``output.bin`` file, can be done with:

.. code-block:: bash

    eve 1 1 | modelpy | gulpy -S1000 -a1 -o output.bin

or

.. code-block:: bash

    eve 1 1 | gulmc -S1000 -a1 -o output.bin

|

On the usage of ``modelpy`` and ``eve`` with ``gulmc``
""""""""""""""""""""""""""""""""""""""""""""""""""""""
Due to internal refactoring, ``gulmc`` now incorporates the functionality performed by ``modelpy``, therefore ``modelpy`` should 
not be used in a pipe with ``gulmc``:

.. code-block:: bash

    eve 1 1 | modelpy | gulpy -S1000 -a1 -o output.bin        # wrong usage, won't work
    eve 1 1 | gulpy -S1000 -a1 -o output.bin                  # correct usage


**NOTE** Both ``gulpy`` and ``gulmc`` can read the events stream from binary file, i.e., without the need of ``eve``, with:

.. code-block:: bash

    gulmc -i input/events.bin -S1000 -a1 -o output.bin

|

``gulmc`` handles hazard uncertainty
####################################

If the hazard intensity in the fooprint has no uncertainty, i.e.:

.. code-block:: csv

    event_id,areaperil_id,intensity_bin_id,probability
    1,4,1,1
    [...]

then ``gulpy`` and ``gulmc`` produce the same outputs. However, if the hazard intensity has a probability distribution, e.g.:

.. code-block:: csv

    event_id,areaperil_id,intensity_bin_id,probability
    1,4,1,2.0000000298e-01
    1,4,2,6.0000002384e-01
    1,4,3,2.0000000298e-01
    [...]

then, by default, ``gulmc`` runs the full Monte Carlo sampling of the hazard intensity, and then of damage. In order to reproduce the same results that `gulpy` produces can be achieved by using the `--effective-damageability` flag:

.. code-block:: bash

    eve 1 1 | gulmc -S1000 -a1 -o output.bin --effective-damageability

|

Probing random values used for sampling
#######################################

Since we now sample in two dimensions (hazard intensity and damage), the ``-d`` flag is revamped to output both random values 
used for sampling. While ``gulpy -d`` printed the random values used to sample the effective damageability distribution, in 
``gulmc``:

.. code-block:: bash

    gulmc -d1 [...]   # prints the random values used for the hazard intensity sampling
    gulmc -d2 [...]   # prints the random values used for the damage sampling

.. note::
    
    if the ``--effective-damageability`` flag is used, only ``-d2`` is valid since there is no sampling of the hazard intensity, 
    and the random value printed are those used for the effective damageability sampling.

.. note::
    
    if ``-d1`` or ``-d2`` are passed, the only valid ``alloc_rule`` value is ``0``. This is because, when printing the random 
    values, back-allocation is not meaningful. ``alloc_rule=0`` is the default value or it can be set with ``-a0``. If a value 
    other than 0 is passed to ``-a``, an error will be thrown.

|

``gulmc`` supports *aggregate vulnerability* definitions
########################################################

``gulmc`` supports aggregate vulnerability functions, i.e., vulnerability functions that are composed of multiple individual 
vulnerability functions.

``gulmc`` now can efficiently reconstruct the aggregate vulnerability functions on-the-fly and compute the aggregate (aka blended, 
aka weighted) vulnerability function. This new functionality works both in the "effective damageability" mode and in the full 
Monte Carlo mode.

Aggregate vulnerability functions are defined using two new tables, to be stored in the ``static/`` directory of the model data: 
``aggregate_vulnerability.csv`` (or ``.bin``) and ``weights.csv`` (or ``.bin``). Example tables:

* an ``aggregate_vulnerability`` table that defines 3 aggregate vulnerability functions, made of 2, 3, and 4 individual 
  vulnerabilities, respectively:

.. code-block:: csv

    aggregate_vulnerability_id,vulnerability_id
    100001,1
    100001,2
    100002,3
    100002,4
    100002,5
    100003,6
    100003,7
    100003,8
    100003,9

* a `weights` table that specifies a measure of concentration 'count' to calculate relative weights for each of the individual vulnerability functions in all ``areaperil_id``: 

.. code-block:: csv

    areaperil_id,vulnerability_id,count
    54,1,138
    54,2,224
    54,3,194
    54,4,264
    54,5,390
    54,6,107
    [...]
    154,1,1
    154,2,97
    154,3,273
    154,4,296
    [...]

|

items.csv (use only two aggregate vulnerability ids):

.. code-block:: csv

    item_id,coverage_id,areaperil_id,vulnerability_id,group_id
    1,1,154,8,833720067
    2,1,54,2,833720067
    3,2,154,8,956003481
    4,2,54,100001,956003481
    5,4,154,100002,2030714556
    [...]

|

**Notes**:

* if ``aggregate_vulnerability.csv`` or ``.bin`` is present, then ``weights.csv`` or ``weights.bin`` needs to be present too, or 
  ``gulmc`` raises an error.
* if ``aggregate_vulnerability.csv`` or ``.bin`` is not present, then ``gulmc`` runs normally, without any definition of aggregate 
  vulnerability.

|

Caching in ``gulmc``
####################

In order to speed up the calculation of losses in the full Monte Carlo mode, we implement a simple caching mechanism whereby the 
most commonly used vulnerability functions cdf are stored in memory for efficient re-usage. 

The cache size is set as the minimum between the cache size specified by the user with the new ``--vuln-cache-size`` argument 
(default: 200, units: MB) and the amount of memory needed to store all the vulnerability functions to be used in the calculations.

The cache dramatically speeds up the execution when the hazard intensity distribution is narrowly peaked (i.e., when most of the 
intensity falls in a few intensity bins), which implies a few vulnerability functions are used repeatedly.

The cache only stores individual vulnerability functions cdf, not the aggregate/weighted cdf, which would be too many to be stored.

Example: to allow the vulnerability cache size to grow up to 1000 MB can be done with:

.. code-block:: bash

    eve 1 1 | gulmc -S100 -a1 --vuln-cache-size=1000

|

``gulmc`` supports hazard correlation
#####################################

Hazard correlation parameters are defined analogously to damage correlation parameters.

Before entering into details, these are **breaking changes** vs the past:

* group ids are now always hashed. This ensures results are fully reproducible. Therefore ``hashed_group_id`` argument has been 
  dropped from the relevant functions.
* from this version, ``oasislmf model run`` will fail if an older model settings JSON file using ``group_fields`` is used vs the 
  new schema that uses ``damage_group_fields`` and ``hazard_group_fields`` as defined in the ``data_settings`` key. See more 
  details below.
* command line interface argument ``--group_id_cols`` for ``oasislmf model run`` has been renamed ``--damage_group_id_cols``. A 
  new argument ``--hazard_group_id_cols`` has been introduced to specify the columns to use for defining group ids for the hazard 
  sampling. They respectively default to:

.. code-block:: python
    DAMAGE_GROUP_ID_COLS = ["PortNumber", "AccNumber", "LocNumber"]
    HAZARD_GROUP_ID_COLS = ["PortNumber", "AccNumber", "LocNumber"]

|

Update to the model settings JSON schema
""""""""""""""""""""""""""""""""""""""""

The oasislmf model settings JSON schema is updated to support the new feature with a breaking change. Previous 
``correlation_settings`` and ``data_settings`` entries in the model settings such as:

.. code-block:: json

    "correlation_settings": [
        {"peril_correlation_group":  1, "correlation_value":  "0.7"},
    ],
    "data_settings": {
        "group_fields": ["PortNumber", "AccNumber", "LocNumber"],
    },

are not supported anymore. The ``correlation_settings`` must contain a new key ``hazard_correlation_value`` and the 
``correlation_value`` key is renamed to ``damage_correlation_value``:

.. code-block:: json

    "correlation_settings": [
        {"peril_correlation_group":  1, "damage_correlation_value":  "0.7", "hazard_correlation_value":  "0.0"},
        {"peril_correlation_group":  2, "damage_correlation_value":  "0.5", "hazard_correlation_value":  "0.0"}
    ],

|

Likewise, the ``data_settings`` entries are renamed from ``group_fields`` to ``damage_group_fields`` and now supports 
``hazard_group_fields``, which is `_optional_` key:

.. code-block:: json

    "data_settings": {
        "damage_group_fields": ["PortNumber", "AccNumber", "LocNumber"],
        "hazard_group_fields": ["PortNumber", "AccNumber", "LocNumber"]
    },

|

Correlations updated schema 
"""""""""""""""""""""""""""

The schema has been updated as follows in order to support correlation parameters:

* if ``correlation_settings`` is not present, ``damage_correlation_value`` and ``hazard_correlation_value`` are assumed zero. 
Peril correlation groups (if defined in supported perils) are ignored. No errors are raised. Example of valid model settings:

.. code-block:: json

    "lookup_settings":{
        "supported_perils":[
            {"id": "WSS", "desc": "Single Peril: Storm Surge", "peril_correlation_group": 1},
            {"id": "WTC", "desc": "Single Peril: Tropical Cyclone", "peril_correlation_group": 1},
            {"id": "WW1", "desc": "Group Peril: Windstorm with storm surge"},
            {"id": "WW2", "desc": "Group Peril: Windstorm w/o storm surge"}
        ]
    },

|

* if ``correlation_settings`` is present, it needs to contain , ``damage_correlation_value`` and ``hazard_correlation_value`` for 
  each ``peril_correlation_group`` entry.  

Example of a valid model settings:

.. code-block:: json

    "lookup_settings":{
        "supported_perils":[
            {"id": "WSS", "desc": "Single Peril: Storm Surge", "peril_correlation_group": 1},
            {"id": "WTC", "desc": "Single Peril: Tropical Cyclone", "peril_correlation_group": 1},
            {"id": "WW1", "desc": "Group Peril: Windstorm with storm surge"},
            {"id": "WW2", "desc": "Group Peril: Windstorm w/o storm surge"}
        ]
    },
    "correlation_settings": [
    {"peril_correlation_group":  1, "damage_correlation_value":  "0.7", "hazard_correlation_value":  "0.3"}
    ],

|

Example of an invalid model settings that raises a ``ValueError``:

.. code-block:: json

    "lookup_settings":{
        "supported_perils":[
            {"id": "WSS", "desc": "Single Peril: Storm Surge", "peril_correlation_group": 1},
            {"id": "WTC", "desc": "Single Peril: Tropical Cyclone", "peril_correlation_group": 1},
            {"id": "WW1", "desc": "Group Peril: Windstorm with storm surge"},
            {"id": "WW2", "desc": "Group Peril: Windstorm w/o storm surge"}
        ]
    },
    "correlation_settings": [
    {"peril_correlation_group":  1}
    ],

|

Correlations files updated schema for csv <-> binary conversion tools
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

The correlations.csv and .bin files are modified as they now contain two additional columns: ``hazard_group_id`` and 
``hazard_correlation_value``. They also feature a renamed column from ``correlation_value`` to ``damage_correlation_value``.

The ``oasislmf`` package ships conversion tools for the correlations files: ``correlationtobin`` to convert a correlations file 
from csv to bin:

.. code-block:: bash

    correlationtobin correlations.csv -o correlations.bin

and ``correlationtocsv`` to convert a ``correlations.bin`` file to ``csv``. If ``-o <filename>`` is specified, it writes the csv 
table to file:

.. code-block:: bash

    correlationtocsv correlations.bin -o correlations.csv

|

If no ``-o <filename>`` is specified, it prints the csv table to stdout:

.. code-block:: bash

    correlationtocsv correlations.bin 
    item_id,peril_correlation_group,damage_correlation_value,hazard_correlation_value
    1,1,0.4,0.0
    2,1,0.4,0.0
    3,1,0.4,0.0
    4,1,0.4,0.0
    5,1,0.4,0.0
    6,1,0.4,0.0
    7,1,0.4,0.0
    8,1,0.4,0.0
    9,1,0.4,0.0
    10,2,0.7,0.9
    11,2,0.7,0.9
    12,2,0.7,0.9
    13,2,0.7,0.9
    14,2,0.7,0.9
    15,2,0.7,0.9
    16,2,0.7,0.9
    17,2,0.7,0.9
    18,2,0.7,0.9
    19,2,0.7,0.9
    20,2,0.7,0.9

|

``gulmc`` supports *stochastic disaggregation* for items and fm files
#####################################################################

Use ``NumberOfBuildings`` from location file to generate expanded items file

Use ``IsAggregate`` flag value from location file to generate fm files.

Each disaggregated location has the same areaperil / vulnerability attributes as the parent coverage.

A new field is needed in gul_summary_map and fm_summary_map to link disaggregated locations to original location (disagg_id)

TIV, deductibles and limits are split equally.

The definition of site for the application of site terms depends on the value of IsAggregate.

where ``IsAggregate`` = 1, site is the disaggregated location
where ``IsAggregate`` = 0, site is the non-disaggregated location


``gulmc`` supports *absolute damage (vulnerability) functions* 
##############################################################

In its current implementation, the damage bin dicts file containing the definition of the damage bins for an entire model can 
contain both relative and absolute damage bins, e.g.:

.. code-block:: csv

    "bin_index","bin_from","bin_to","interpolation"
    1,0.000000,0.000000,0.000000
    2,0.000000,0.100000,0.050000
    3,0.100000,0.200000,0.150000
    4,0.200000,0.300000,0.250000
    5,0.300000,0.400000,0.350000
    6,0.400000,0.500000,0.450000
    7,0.500000,0.600000,0.550000
    8,0.600000,0.700000,0.650000
    9,0.700000,0.800000,0.750000
    10,0.800000,0.900000,0.850000
    11,0.900000,1.000000,0.950000
    12,1.000000,1.000000,1.000000
    13,1.000000,2.000000,1.500000
    14,2.000000,3.000000,2.500000
    15,3.000000,30.00000,16.50000

where bins 1 to 12 represent a relative damage, and bins 13 to 15 represent an absolute damage.

For random losses falling in absolute damage bins that have a non-zero width (e.g., bins 13, 14, and 15), the loss is 
interpolated using the same linear or parabolic interpolation algorithm already used for the relative damage bins.

**IMPORTANT**: vulnerability functions are required to be **either entirely absolute or entirely relative**. *Mixed* 
vulnerability functions defined by a mixture of absolute and relative vulnerability function are not supported. Currently there 
is no automatic pre-run check that verifies that all vulnerability functions comply with this requirement; the user must check 
this manually.