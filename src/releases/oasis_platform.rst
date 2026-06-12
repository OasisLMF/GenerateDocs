OasisPlatform Changelog
=======================

.. start_latest_release

`2.5.4`_
---------
* `#1389 <https://github.com/OasisLMF/OasisPlatform/pull/1389>`_ - Tidy up related file serializers
* `#1395 <https://github.com/OasisLMF/OasisPlatform/pull/1395>`_ - Remove storage of raw output and SQL endpoints
* `#1396 <https://github.com/OasisLMF/OasisPlatform/pull/1396>`_ - Updated Package Requirements: urllib3==2.7.0 twisted==26.*
* `#1398 <https://github.com/OasisLMF/OasisPlatform/pull/1398>`_ - Bake numba JIT cache into model-worker
* `#1400 <https://github.com/OasisLMF/OasisPlatform/pull/1400>`_ - fix/input_gen_status

.. end_latest_release

.. _`2.5.4`: https://github.com/OasisLMF/OasisPlatform/compare/2.5.3...2.5.4

`2.5.3`_
---------
* `#1379 <https://github.com/OasisLMF/OasisPlatform/pull/1379>`_ - fix: chainmap import
* `#1380 <https://github.com/OasisLMF/OasisPlatform/pull/1380>`_ - Ktools options renamed to kernel options
* `#1381 <https://github.com/OasisLMF/OasisPlatform/pull/1381>`_ - enhancement/perils from OED
* `#1383 <https://github.com/OasisLMF/OasisPlatform/pull/1383>`_ - Fix resource monitor for V2 worker runs
* `#1387 <https://github.com/OasisLMF/OasisPlatform/pull/1387>`_ - Added option to disable API authorization (API_AUTH_TYPE=disabled)
* `#1388 <https://github.com/OasisLMF/OasisPlatform/pull/1388>`_ - Fix swagger file picker
* `#1392 <https://github.com/OasisLMF/OasisPlatform/pull/1392>`_ - Fix for 403 when calling analysis-task-statuses with no auth

.. _`2.5.3`: https://github.com/OasisLMF/OasisPlatform/compare/2.5.2...2.5.3

`2.5.2`_
---------
* `#1340 <https://github.com/OasisLMF/OasisPlatform/pull/1340>`_ - Move from drf-yasg to drf-spectacular
* `#1346 <https://github.com/OasisLMF/OasisPlatform/pull/1346>`_ - Added Numba JIT warm-up to worker startup
* `#1347 <https://github.com/OasisLMF/OasisPlatform/pull/1347>`_ - Fixed limiting cores on V2 workers
* `#1355 <https://github.com/OasisLMF/OasisPlatform/pull/1355>`_ - Remove validate option when uploading exposure file
* `#1361 <https://github.com/OasisLMF/OasisPlatform/pull/1361>`_ - Set logger based on oasislmf log level
* `#1363 <https://github.com/OasisLMF/OasisPlatform/pull/1363>`_ - Feature/celery ssl support (OASIS_CELERY_BROKER_SSL_* options)

.. _`2.5.2`: https://github.com/OasisLMF/OasisPlatform/compare/2.5.1...2.5.2

`2.5.1`_
---------
* `#1325 <https://github.com/OasisLMF/OasisPlatform/pull/1325>`_ - Add platform interface for ORD combining tool
* `#1334 <https://github.com/OasisLMF/OasisPlatform/pull/1334>`_ - Update Oasis Data Manager
* `#1344 <https://github.com/OasisLMF/OasisPlatform/pull/1344>`_ - Revert removal of ``latest`` docker image tag
* `#1342 <https://github.com/OasisLMF/OasisPlatform/pull/1342>`_ - fix/oidc_token_scopes

.. _`2.5.1`: https://github.com/OasisLMF/OasisPlatform/compare/2.5.0...2.5.1

`2.5.0`_
---------
* `#1248 <https://github.com/OasisLMF/OasisPlatform/pull/1248>`_ - Feature/generic OIDC authentication
* `#1312 <https://github.com/OasisLMF/OasisPlatform/pull/1312>`_ - RoE (Return on Equity) functionality in Platform
* `#1316 <https://github.com/OasisLMF/OasisPlatform/pull/1316>`_ - Fix/current platform errors
* `#1317 <https://github.com/OasisLMF/OasisPlatform/pull/1317>`_ - Use updated setting handlers from ods-tools

.. _`2.5.0`: https://github.com/OasisLMF/OasisPlatform/compare/2.4.10...2.5.0
