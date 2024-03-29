Ktools
======

On this package
---------------

* :ref:`intro_ktools`
* :ref:`background_ktools`
* :ref:`architecture_ktools`
* :ref:`language_ktools`
* :ref:`components_ktools`
* :ref:`usage_ktools`
* :ref:`links_ktools`

|

.. _intro_ktools:

Introduction
************

----

The in-memory solution for the Oasis Kernel is called the kernel tools or “ktools”. ktools is an independent “specification” 
of a set of processes which means that it defines the processing architecture and data structures. The framework is 
implemented as a set of components called the “reference model” which can then be adapted for particular model or business 
needs.

The code can be compiled in Linux, POSIX-compliant Windows and native Windows. The installation instructions can be found 
`here <https://github.com/OasisLMF/ktools/blob/develop/README.md>`_.

|

.. _background_ktools:

Background
**********

----

The Kernel performs the core Oasis calculations of computing effective damageability distributions, Monte-Carlo sampling of 
ground up loss, the financial module calculations, which apply insurance policy terms and conditions to the sampled losses, 
and finally some common catastrophe model outputs.

The early releases of Oasis used a SQL-compliant database to perform all calculations. Release 1.3 included the first 
“in-memory” version of the Oasis Kernel written in C++ and C to provide streamed calculation at high computational 
performance, as an alternative to the database calculation. The scope of the in-memory calculation was for the most 
intensive Kernel calculations of ground up loss sampling and the financial module. This in-memory variant was first 
delivered as a stand-alone toolkit "ktools" with R1.4.

With R1.5, a Linux-based in-memory calculation back-end was released, using the reference model components of ktools. The 
range of functionality of ktools was still limited to ground up loss sampling, the financial module and single output 
workflows, with effective damage distributions and output calculations still being performed in a SQL-compliant database.

In 2016 the functionality of ktools was extended to include the full range of Kernel calculations, including effective 
damageability distribution calculations and a wider range of financial module and output calculations. The data stream 
structures and input data formats were also substantially revised to handle multi-peril models, user-definable summary 
levels for outputs, and multiple output workflows.

In 2018 the Financial Module was extended to perform net loss calculations for per occurrence forms of reinsurance, 
including facultative reinsurance, quota share, surplus share, per risk and catastrophe excess of loss treaties.

|

.. _architecture_ktools:

Architecture
************

----

The Kernel is provided as a toolkit of components (“ktools”) which can be invoked at the command line. Each component is a 
separately compiled executable with a binary data stream of inputs and/or outputs.

The principle is to stream data through the calculations in memory, starting with generating the damage distributions and 
ending with calculating the user's required result, before writing the output to disk. This is done on an event-by-event 
basis, which means at any one time the compute server only has to hold the model data for a single event in its memory, per 
process. The user can run the calculation across multiple processes in parallel, specifiying the analysis workfkow and 
number of processes in a script file appropriate to the operating system.

|

.. _language_ktools:

Language
********

----

The components can be written in any language as long as the data structures of the binary streams are adhered to. The 
current set of components have been written in POSIX-compliant C++. This means that they can be compiled in Linux and 
Windows using the latest GNU compiler toolchain.

|

.. _components_ktools:

Components
**********

----

The components in the Reference Model can be summarized as follows:

* `Core components <https://github.com/OasisLMF/ktools/blob/develop/docs/md/CoreComponents.md>`_ perform the core kernel 
  calculations and are used in the main analysis workflow.

* `Output components <https://github.com/OasisLMF/ktools/blob/develop/docs/md/OutputComponents.md>`_ perform specific 
  output calculations at the end of the analysis workflow. Essentially, they produce various statistical summaries of the 
  sampled losses from the core calculation.

* `Data conversion components <https://github.com/OasisLMF/ktools/blob/develop/docs/md/InputConversionComponents.md>`_ are 
  provided to enable users to convert model and exposure data into the required binary formats.

* `Stream conversion components <https://github.com/OasisLMF/ktools/blob/develop/docs/md/StreamConversionComponents.md>`_ 
  are provided to inspect the data streams flowing between the core components, for more detailed analysis or debugging 
  purposes.

|

.. _usage_ktools:

Usage
*****

----

Standard piping syntax can be used to invoke the components at the command line. It is the same syntax in Windows DOS, 
Linux terminal or Cygwin (a Linux emulator for Windows). For example the following command invokes eve, getmodel, gulcalc, 
fmcalc, summarycalc and eltcalc, and exports an event loss table output to a csv file.

.. code-block:: sh

    $ eve 1 1 | getmodel | gulcalc -r –S100 -a1 –i - | fmcalc | summarycalc -f -1 - | eltcalc > elt.csv
|

Example python scripts are provided along with a binary data package in the /examples folder to demonstrate usage of the 
toolkit. For more guidance on how to use the toolkit, see `Workflows <https://github.com/OasisLMF/ktools/blob/develop/docs/
md/Workflows.md>`_.

|

.. _links_ktools:

Links for more information
**************************

----

More information on ktools can be found in the `ktools GitHub repository <https://github.com/OasisLMF/ktools/tree/develop#readme>`_ 
on:

1. `Introduction <https://github.com/OasisLMF/ktools/blob/develop/docs/md/Introduction.md>`_

2. `Data streaming architecture overview <https://github.com/OasisLMF/ktools/blob/develop/docs/md/Overview.md>`_

3. `Specification <https://github.com/OasisLMF/ktools/blob/develop/docs/md/Specification.md>`_

4. `Reference model <https://github.com/OasisLMF/ktools/blob/develop/docs/md/ReferenceModelOverview.md>`_

4.1 `Core Components section <https://github.com/OasisLMF/ktools/blob/develop/docs/md/CoreComponents.md>`_

4.2 `Output components <https://github.com/OasisLMF/ktools/blob/develop/docs/md/OutputComponents.md>`_

4.3 `ORD output components <https://github.com/OasisLMF/ktools/blob/develop/docs/md/ORDOutputComponents.md>`_

4.4 `Data conversion components <https://github.com/OasisLMF/ktools/blob/develop/docs/md/DataConversionComponents.md>`_

4.5 `Stream conversion components <https://github.com/OasisLMF/ktools/blob/develop/docs/md/StreamConversionComponents.md>`_

4.6 `Validation components <https://github.com/OasisLMF/ktools/blob/develop/docs/md/ValidationComponents.md>`_

5. `Financial Module <https://github.com/OasisLMF/ktools/blob/develop/docs/md/FinancialModule.md>`_

6. `Workflows <https://github.com/OasisLMF/ktools/blob/develop/docs/md/Workflows.md>`_