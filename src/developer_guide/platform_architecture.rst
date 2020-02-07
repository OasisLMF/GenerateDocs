Platform architecture
=====================

A schematic of the Oasis Platform architecture is shown in the diagram below, and the components are descibed in the following table:

.. figure:: /images/oasis_containers.png
    :alt: Oasis UI and Platform architecture
   
.. csv-table::
    :header: "Component", "Description", "Technology"

    "ShinyProxy", "Provides multi-user support and enterprise integration features on top of a Shiny app.", "ShinyProxy"
    "OasisUI", "The application server for the Oasis user interface, a web app.", "Shiny App"
    "OasisAPI", "The application server for the Oasis API.", "Django Application Server"
    "OasisAPI DB", "The database for the Oasis API. Stores the system meta-data, but not the detailed model data, exposure data or results.", "MySql (or other RDBMS)"
    "Worker monitor", "Monitors the model worker and updates the Oasis API database with the status of tasks.", "Custom Python code"
    "Celery - Message Queue", "Message queue for the celery job management framework.", "Rabbit MQ (other options)"
    "Celery – Backing Store", "Backing store for the celery job management framework.", "MySQL (other options)"
    "Datastore", "File based datastore for exposure data, analysis results and model data.", "Docker volume"
    "Model Worker", "Celery worker that can run a lookup or model execution task for a particular model version. The model data is attached to the container from the datastore at startup.", "Custom Python and C++ code"

All of the components are packaged as Docker images.
Docker-compose can be used to deploy the system on one or more physical servers.
Scalability can be achieved by provisioning more calculation servers and deploying more Analysis Worker images.