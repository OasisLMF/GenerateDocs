OasisLMF Changelog
==================

.. start_latest_release

`2.5.4`_
---------
* `#1940 <https://github.com/OasisLMF/OasisLMF/pull/1940>`_ - enhancement/profile check script
* `#1942 <https://github.com/OasisLMF/OasisLMF/pull/1942>`_ - Fix brittle PolNumber backfill in IL input preparation
* `#1947 <https://github.com/OasisLMF/OasisLMF/pull/1947>`_ - enhancement/conversion_tool_speed
* `#1955 <https://github.com/OasisLMF/OasisLMF/pull/1955>`_ - Improved quadratic interpolation for robustness
* `#1957 <https://github.com/OasisLMF/OasisLMF/pull/1957>`_ - Stochastic hazard dynamic footprint
* `#1963 <https://github.com/OasisLMF/OasisLMF/pull/1963>`_ - Update API client for OIDC M2M
* `#1964 <https://github.com/OasisLMF/OasisLMF/pull/1964>`_ - perf(gulmc): replace numba dicts with precomputed array-backed structures
* `#1967 <https://github.com/OasisLMF/OasisLMF/pull/1967>`_ - Fix for stalled runs on V2 workers
* `#1968 <https://github.com/OasisLMF/OasisLMF/pull/1968>`_ - Improve numerical stability in variance calculations
* `#1969 <https://github.com/OasisLMF/OasisLMF/pull/1969>`_ - Improved bash error detection
* `#1971 <https://github.com/OasisLMF/OasisLMF/pull/1971>`_ - Fix IL merge failure when layers sharing a CondTag mix %-TIV and flat terms
* `#1973 <https://github.com/OasisLMF/OasisLMF/pull/1973>`_ - Add portfolio complexity metrics to oasislmf exposure run
* `#1974 <https://github.com/OasisLMF/OasisLMF/pull/1974>`_ - Improve rtree builtin
* `#1979 <https://github.com/OasisLMF/OasisLMF/pull/1979>`_ - Feature/hazard selection dynamic
* `#1987 <https://github.com/OasisLMF/OasisLMF/pull/1987>`_ - fix/pytools-empty-inputs
* `#1992 <https://github.com/OasisLMF/OasisLMF/pull/1992>`_ - Speed up summarypy read_buffer
* `#1999 <https://github.com/OasisLMF/OasisLMF/pull/1999>`_ - fix/input_gen_status

.. end_latest_release

.. _`2.5.4`: https://github.com/OasisLMF/OasisLMF/compare/2.5.3...2.5.4

`2.5.3`_
---------
* `#1903 <https://github.com/OasisLMF/OasisLMF/pull/1903>`_ - Remove pd from summarypy to save on memory usage
* `#1920 <https://github.com/OasisLMF/OasisLMF/pull/1920>`_ - enhancement/lecpy_speed
* `#1935 <https://github.com/OasisLMF/OasisLMF/pull/1935>`_ - enhancement/peril info from OEDSpec
* `#1941 <https://github.com/OasisLMF/OasisLMF/pull/1941>`_ - Fix correct UTC timestamps in get_utctimestamp
* `#1945 <https://github.com/OasisLMF/OasisLMF/pull/1945>`_ - Fix resource monitor for V2 worker runs
* `#1948 <https://github.com/OasisLMF/OasisLMF/pull/1948>`_ - fix/nonzero default fm profile
* `#1951 <https://github.com/OasisLMF/OasisLMF/pull/1951>`_ - fix/join-summary-info-bugs
* `#1956 <https://github.com/OasisLMF/OasisLMF/pull/1956>`_ - fix: reduce memory usage in FootprintBin and skip footprint load when data_server active
* `#1959 <https://github.com/OasisLMF/OasisLMF/pull/1959>`_ - API client: added option for disabled auth
* `#1960 <https://github.com/OasisLMF/OasisLMF/pull/1960>`_ - Directly send port to gulmc gulpy and socket server

.. _`2.5.3`: https://github.com/OasisLMF/OasisLMF/compare/2.5.2...2.5.3

`2.5.2`_
---------
* `#1873 <https://github.com/OasisLMF/OasisLMF/pull/1873>`_ - Add docstrings and documentation to bash.py
* `#1878 <https://github.com/OasisLMF/OasisLMF/pull/1878>`_ - Fix error handling and replaced row wise apply in loss computation
* `#1898 <https://github.com/OasisLMF/OasisLMF/pull/1898>`_ - Add resource monitor for pytools processes
* `#1899 <https://github.com/OasisLMF/OasisLMF/pull/1899>`_ - Add Numba JIT cache warmup to eliminate cold-start overhead
* `#1902 <https://github.com/OasisLMF/OasisLMF/pull/1902>`_ - Add option to set analyses chunk size for API client
* `#1913 <https://github.com/OasisLMF/OasisLMF/pull/1913>`_ - feat: Native Apple Silicon (macOS arm64) installation support
* `#1919 <https://github.com/OasisLMF/OasisLMF/pull/1919>`_ - Optimize FootprintParquetDynamic for partitioned parquet
* `#1923 <https://github.com/OasisLMF/OasisLMF/pull/1923>`_ - Add H3 hexagonal grid lookup to builtin keys server
* `#1924 <https://github.com/OasisLMF/OasisLMF/pull/1924>`_ - fix: remove necessity for dummy layer with multiple cond peril
* `#1930 <https://github.com/OasisLMF/OasisLMF/pull/1930>`_ - Set CRS to WGS84 on location coordinates

.. _`2.5.2`: https://github.com/OasisLMF/OasisLMF/compare/2.5.1...2.5.2

`2.5.1`_
---------
* `#1869 <https://github.com/OasisLMF/OasisLMF/pull/1869>`_ - perf: Optimize GULMC performance - 4.5% faster standard, 76% faster dynamic footprint
* `#1876 <https://github.com/OasisLMF/OasisLMF/pull/1876>`_ - Write binary files directly, bypass CSV intermediary
* `#1879 <https://github.com/OasisLMF/OasisLMF/pull/1879>`_ - fix/oidc_header_fix
* `#1885 <https://github.com/OasisLMF/OasisLMF/pull/1889>`_ - Race condition fix with join-summary-info in generated bash script

.. _`2.5.1`: https://github.com/OasisLMF/OasisLMF/compare/2.5.0...2.5.1

`2.5.0`_
---------
* `#1811 <https://github.com/OasisLMF/OasisLMF/pull/1811>`_ - Add environment variables and coerce into integers
* `#1813 <https://github.com/OasisLMF/OasisLMF/pull/1813>`_ - Fixed merging analyses computation_settings on the platform
* `#1836 <https://github.com/OasisLMF/OasisLMF/pull/1836>`_ - Dynamic footprint initial implementation
* `#1842 <https://github.com/OasisLMF/OasisLMF/pull/1842>`_ - GULMC: support for effective damageability and Full Monte Carlo modes
* `#1848 <https://github.com/OasisLMF/OasisLMF/pull/1848>`_ - Add support for parquet keys files
* `#1855 <https://github.com/OasisLMF/OasisLMF/pull/1855>`_ - Add OED schema version selection (--oed-schema-info)
* `#1860 <https://github.com/OasisLMF/OasisLMF/pull/1860>`_ - Post-analysis hook support (run-postanalysis command)

.. _`2.5.0`: https://github.com/OasisLMF/OasisLMF/compare/2.4.9...2.5.0
