Container Configuration
======================

.. _container_configuration:

:doc:`overview` | :doc:`platform_architecture` | :doc:`container_configuration` | :doc:`rest_api` | :doc:`distributed_execution` | :doc:`appendices`

There are two methods for setting configuration options on an oasis container. (1) by setting a shell environment variable on the container. (2) by adjusting a conf.ini file within the container.

Environment Variable Overrides
------------------------------

Configuration for OASIS Docker containers is primarily managed via a conf.ini file, which establishes default values. However, the **preferred and highest-precedence method for dynamic configuration is through shell environment variables.**

Naming Convention
^^^^^^^^^^^^^^^^^

To ensure an environment variable is recognized and applied, it must be prefixed with **OASIS_**. Any environment variable lacking this prefix will be ignored by the OASIS applications.

* **Example:** Setting OASIS_DEBUG=True will override the default DEBUG=False value found in the conf.ini file.

conf.ini Location and Loading
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The canonical conf.ini file is located at OasisLMF/OasisPlatform/conf.ini within the OasisPlatform repository. This file provides the base configuration, but its effective path and how it's consumed differs based on the container type:

* **Model Worker Images:**
  
  * **Container Path:** /home/worker/conf.ini
  * **Integration:** Values from this conf.ini are loaded and directly influence the configuration within Celery's task processing files.

* **Server Images (Django):**
  
  * **Container Path:** /var/www/oasis/conf.ini
  * **Integration:** Values from this conf.ini are loaded into Django's settings.py configuration file, forming the application's core settings.

Precedence Hierarchy
^^^^^^^^^^^^^^^^^^^^

When an OASIS container starts, configuration values are applied in the following order of precedence, with later steps overriding earlier ones:

1. **conf.ini Defaults:** Values read from the conf.ini file ([default], [server], [worker], [celery] sections, respecting section-specific overrides).
2. **OASIS_ Prefixed Environment Variables:** Any environment variable set with the OASIS_ prefix (e.g., OASIS_DEBUG) will *always* override a corresponding setting derived from the conf.ini file.

This ensures that you can define sensible defaults within your image, while maintaining the flexibility to adjust specific parameters at deployment time using environment variables, without needing to rebuild or modify the container image itself.

Understanding conf.ini Structure and Precedence
-----------------------------------------------

The conf.ini file employs a standard INI file format, organized into sections, each containing key-value pairs. The sections define the scope of the configuration:

* **[default]**: This section contains settings that apply universally to all container types (servers and workers).
* **[server]**: Settings in this section are specific to server (e.g., Django) containers. Any key-value pair defined here will override a similarly named key in the [default] section when accessed by a server.
* **[worker]**: Similar to [server], this section holds configurations unique to worker containers. Settings here will override [default] settings for workers.
* **[celery]**: This section is dedicated to Celery-specific configuration options and applies to *both* server and worker container types, assuming both might interact with Celery.

Precedence Rules
^^^^^^^^^^^^^^^

1. **Environment Variables (Highest Precedence):** An environment variable OASIS_SETTING_NAME_TO_GET=<value> will always override any setting, regardless of the conf.ini file. This provides the most dynamic and immediate way to adjust configurations without modifying the file itself.
2. **Specific Section Overrides Default:** For server containers, values in [server] take precedence over [default]. For worker containers, values in [worker] take precedence over [default].
3. **[celery] Section:** Settings within [celery] are additive and specifically for Celery. They don't directly override [default], [server], or [worker] in the same way, but rather provide a dedicated namespace for Celery configurations that both server and worker processes can utilize.

Server Container Configuration Options
--------------------------------------

These options are specifically applicable to the **coreoasis/api_server** containers and can be set via environment variables (prefixed with OASIS_, OASIS_{ini sections}_{variable}) or within the conf.ini file's [server] or [default] sections.

For example OASIS_DB_PASS=<value> or OASIS_SERVER_DB_PASS=<value> will both work.

Django Core Options
^^^^^^^^^^^^^^^^^^^

.. csv-table::
   :header: "Option Name", "Type", "Default", "Description"
   :widths: 20, 10, 15, 55

   "MEDIA_ROOT", "String", "(Django default)", "The absolute filesystem path to the directory that will hold user-uploaded media files."
   "SECRET_KEY", "String", "(Django required)", "A secret key used for cryptographic signing, crucial for security (e.g., sessions, password resets)."
   "ALLOWED_HOSTS", "List/String", "[]", "A list of strings representing the host/domain names that this Django site can serve. Protects against HTTP Host header attacks."
   "STARTUP_RUN_MIGRATIONS", "Boolean", "True", "If set to True, Django database migrations will be automatically applied when the container starts."
   "OASIS_ADMIN_USER", "String", "None", "If set, a default Django superuser will be created with this username. Requires OASIS_ADMIN_PASS."
   "OASIS_ADMIN_PASS", "String", "None", "The password for the default admin user specified by OASIS_ADMIN_USER. Requires OASIS_ADMIN_USER."

Debug Options
^^^^^^^^^^^^

.. csv-table::
   :header: "Option Name", "Type", "Default", "Description"
   :widths: 20, 10, 15, 55

   "DEBUG", "Boolean", "False", "Controls Django's debug mode. If True, enables verbose logging, error pages, and other development features. **Should be False in production.**"
   "DEBUG_TOOLBAR", "Boolean", "False", "If True, enables the Django Debug Toolbar, typically accessible in the Swagger UI for development and debugging purposes."
   "URL_SUB_PATH", "Boolean", "False", "If True, all REST API routes will be nested under a /api/ sub-path (e.g., https://<site-domain>/api/). Otherwise, routes are directly under the domain (e.g., https://<site-domain>/)."
   "DISABLE_V2_API", "Boolean", "False", "If True, disables the V2 API routes, primarily for backward compatibility with older client integrations."

Storage Related Options
^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table::
   :header: "Option Name", "Type", "Default", "Description"
   :widths: 20, 10, 15, 55

   "PORTFOLIO_PARQUET_STORAGE", "Boolean", "False", "If True, all portfolio CSV files uploaded will be automatically compressed and stored in Parquet format."
   "STORAGE_TYPE", "String", "shared-fs", "Defines the backend storage solution. Valid values are 'S3' (AWS S3), 'AZURE' (Azure Blob Storage), or 'shared-fs' (a common file system accessible by containers)."

**If STORAGE_TYPE is 'S3'**:

See :ref:`appendix_s3_options` for the complete list of AWS S3 configuration options.

**If STORAGE_TYPE is 'AZURE'**:

See :ref:`appendix_azure_options` for the complete list of Azure Blob Storage configuration options.

Server Database (DB) Options
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table::
   :header: "Option Name", "Type", "Default", "Description"
   :widths: 20, 10, 15, 55

   "DB_ENGINE", "String", "django.db.backends.postgresql_psycopg2", "The database backend engine (e.g., django.db.backends.postgresql_psycopg2, django.db.backends.mysql)."
   "DB_HOST", "String", "localhost", "The hostname or IP address of the database server."
   "DB_PASS", "String", "None", "The password for the database user."
   "DB_USER", "String", "None", "The username for connecting to the database."
   "DB_NAME", "String", "oasis", "The name of the database to connect to."
   "DB_PORT", "Integer", "5432", "The port number on which the database server is listening. (e.g., 5432 for PostgreSQL, 3306 for MySQL)."
   "CHANNEL_LAYER_HOST", "String", "channel-layer", "The hostname or IP address of the server hosting the Django Channels layer (e.g., Redis or RabbitMQ)."

Authentication Options
^^^^^^^^^^^^^^^^^^^^^

.. csv-table::
   :header: "Option Name", "Type", "Default", "Description"
   :widths: 20, 10, 15, 55

   "API_AUTH_TYPE", "String", "simple_jwt", "Defines the API authentication mechanism. Valid values are 'keycloak' or 'simple_jwt'."

**If API_AUTH_TYPE is 'keycloak'**:

See :ref:`appendix_keycloak_options` for the complete list of Keycloak configuration options.

**If API_AUTH_TYPE is 'simple_jwt'**:

See :ref:`appendix_simplejwt_options` for the complete list of Simple JWT configuration options.

Worker Container Configuration Options
--------------------------------------

These options are specifically applicable to the worker (Celery) container, which processes tasks dispatched from the API.

Celery Queue Naming
^^^^^^^^^^^^^^^^^^^

These three variables are crucial for the worker to correctly identify and connect to its designated Celery task queue. They **must match** the corresponding values used by the API's models endpoint when dispatching tasks.

.. csv-table::
   :header: "Option Name", "Type", "Default", "Description"
   :widths: 20, 10, 15, 55

   "MODEL_SUPPLIER_ID", "String", "None", "Identifier for the model supplier, forming part of the Celery queue name."
   "MODEL_ID", "String", "None", "Identifier for the specific model, forming part of the Celery queue name."
   "MODEL_VERSION_ID", "String", "None", "Identifier for the model version, forming part of the Celery queue name."

Workflow Run Mode
^^^^^^^^^^^^^^^^

.. csv-table::
   :header: "Option Name", "Type", "Default", "Description"
   :widths: 20, 10, 15, 55

   "RUN_MODE", "String", "None", "Determines the worker's operational mode. - 'v1': Selects a single-server, legacy workflow. - 'v2': Selects distributed, modern workflow based on the OASIS platform."

Worker Paths
^^^^^^^^^^^^

These options define file locations within the worker container for models, configuration, and run data.

See :ref:`appendix_worker_paths` for the complete list of worker path configuration options.

Debug Options
^^^^^^^^^^^^

These options control various debugging behaviors and features within the worker.

.. csv-table::
   :header: "Option Name", "Type", "Default", "Description"
   :widths: 20, 10, 15, 55

   "DEBUG", "Boolean", "False", "If True, enables increased and more verbose logging for worker operations, useful for debugging."
   "DISABLE_WORKER_REG", "Boolean", "False", "If True, disables the worker's automatic self-registration process with the API server's 'models' endpoint upon connection."

V2 Mode Only Options
^^^^^^^^^^^^^^^^^^^^

These options are only relevant and applied when RUN_MODE is set to 'v2'.

See :ref:`appendix_v2_options` for the complete list of V2 mode configuration options.

V1 Mode Only Options
^^^^^^^^^^^^^^^^^^^^

These options are only relevant and applied when RUN_MODE is set to 'v1'.

See :ref:`appendix_v1_options` for the complete list of V1 mode configuration options.

Storage Related Options
^^^^^^^^^^^^^^^^^^^^^^^

These options configure the worker's ability to interact with various storage backends for input/output data.

.. csv-table::
   :header: "Option Name", "Type", "Default", "Description"
   :widths: 20, 10, 15, 55

   "STORAGE_TYPE", "String", "shared-fs", "Defines the backend storage solution. Valid values are 'S3' (AWS S3), 'AZURE' (Azure Blob Storage), or 'shared-fs' (a common file system accessible by containers)."

For detailed S3 and Azure configuration options, see :ref:`appendix_s3_options` and :ref:`appendix_azure_options` respectively.

Celery Configuration Options
----------------------------

The following options apply to both server and worker containers, any container connected to celery. But can vary by oasis version.

Celery Broker: Image Versions 1.28.x or Older
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table::
   :header: "Option Name", "Type", "Default", "Description"
   :widths: 20, 10, 15, 55

   "OASIS_RABBIT_HOST", "String", "broker", "Hostname of the RabbitMQ broker for Celery workers."
   "OASIS_RABBIT_PORT", "Integer", "5672", "Port of the RabbitMQ broker for Celery workers."
   "OASIS_RABBIT_USER", "String", "rabbit", "Username for connecting to the RabbitMQ broker for Celery workers."
   "OASIS_RABBIT_PASS", "String", "rabbit", "Password for connecting to the RabbitMQ broker for Celery workers."

Celery Broker: Image Versions 2.3.x or Newer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table::
   :header: "Option Name", "Type", "Default", "Description"
   :widths: 20, 10, 15, 55

   "OASIS_CELERY_BROKER_URL", "String", "amqp://rabbit:rabbit@broker:5672", "Full connection URL for the Celery broker."

Celery Results DB connection Values: Applies to All Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table::
   :header: "Option Name", "Type", "Default", "Description"
   :widths: 20, 10, 15, 55

   "CELERY_DB_ENGINE", "String", "db+postgresql+psycopg2", "Specifies the database engine for Celery's results backend."
   "CELERY_DB_HOST", "String", "celery-db", "Hostname for the database used as Celery's results backend."
   "CELERY_DB_PASS", "String", "password", "Password for accessing the database used as Celery's results backend."
   "CELERY_DB_USER", "String", "celery", "Username for accessing the database used as Celery's results backend."
   "CELERY_DB_NAME", "String", "celery", "Name of the database used as Celery's results backend."
   "CELERY_DB_PORT", "Integer", "5432", "Port for connecting to the database used as Celery's results backend."

Celery concurrency and custom arguments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Following apply only to the worker images, and are not configurable from the conf.ini file

.. csv-table::
   :header: "Option Name", "Type", "Default", "Description"
   :widths: 20, 10, 15, 55

   "OASIS_CELERY_CONCURRENCY", "Integer", "Number of available cores", "Sets the concurrency argument for Celery workers. By default, it equals the number of available cores, but can be set lower to mitigate out-of-memory errors."
   "OASIS_CELERY_EXTRA_ARGS", "String", "None", "Allows passing custom Celery arguments directly into the worker's startup command. Refer to the Celery CLI documentation for available options."
