Platform architecture
=====================

A schematic of the Oasis Platform architecture is shown in the diagram below, and the components are descibed in the following table:

.. figure:: /images/oasis_architecture_tiers.jpg
    :alt: Oasis UI and Platform architecture
   
.. csv-table::
    :header: "Component", "Description", "Technology"

    "Oasis UI", "Browser-based application that provides simple modelling workflows.", "ShinyProxy"
    "Oasis UI API", "Services for running models and interacting with exposure and output data.", "Flask"
    "Oasis UI Database", "Storage for exposure data, workflow configurations and system data.", "SQL Server"
    "Oasis API", "Services for uploading Oasis files, running analyses and retrieving outputs.", "Flask, Celery"
    "Message Queue", "Queues for managing workload across multiple calculation back ends.", "Rabbit MQ"
    "Data store", "Storage for transient analysis data.", "File share"
    "Keys Server", "Model specific services for generating area peril and vulnerability keys for a particular set of exposures.", "Flask, Python"
    "Analysis Worker", "Executes a model.", "Celery, running as daemon, ktools, model data"

All of the components, apart from SQL server, are packaged as Docker images.
Docker-compose is used to deploy the system on one or more physical servers.
Scalability can be achieved by provisioning more calculation servers and deploying more Analysis Worker images.
We intend to investigate container-based orchestrators, such as Kubernetes or AWS Container Service, for running catastrophe models at scale in a cost effective manner.