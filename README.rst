GCP BigQuery Quota Testing
##########################

Setup
=====

.. code-block:: bash

    pip install -r requirements.txt
    # export GCP service account credential path if necessary
    # GOOGLE_APPLICATION_CREDENTIALS


LoadJob to Standard Table
=========================

Create Table
------------

.. code-block:: bash

    # create table in BigQuery dataset
    python load_job_to_table.py create-table \
        --project [project_name] \
        --dataset [dataset_name]
        --table [table_name]

    # In case, you want to drop the table
    python load_job_to_table.py drop-table \
        --project [project_name] \
        --dataset [dataset_name]
        --table [table_name]


Run load jobs with threads
--------------------------

.. code-block:: bash

    # run load jobs with threads
    python load_job_to_standard_table.py loadjob-with-thread \
        --project [project-name] \
        --dataset [dataset-name] \
        --table [table_name]
        --num-thread 1


Results
-------

* ref: https://cloud.google.com/bigquery/quotas#table_limits

rateLimitExceeded
>>>>>>>>>>>>>>>>>

* Maximum rate of table metadata update operations: 5 operations every 10 seconds per table

.. code-block:: python

    [{'reason': 'rateLimitExceeded', 'location': 'table.write',
    'message': 'Exceeded rate limits: too many table update operations for this table. For more information, see https://cloud.google.com/bigquery/troubleshooting-errors'}]


quotaExceeded
>>>>>>>>>>>>>

* Maximum number of table operations per day — 1,000

.. code-block:: python

      [{'reason': 'quotaExceeded', 'location': 'load_job_per_table.long',
      'message': 'Quota exceeded: Your table exceeded quota for imports or query appends per table. For more information, see https://cloud.google.com/bigquery/troubleshooting-errors'}]



LoadJob to Column Partitioned Table
===================================

Create Table
------------

.. code-block:: bash

    # create table in BigQuery dataset
    python load_job_to_table.py create-table \
        --project [project_name] \
        --dataset [dataset_name]
        --table [table_name]
        --partitioned


Run load jobs with threads
--------------------------

.. code-block:: bash

    # run load jobs with threads
    python load_job_to_table.py loadjob-with-thread \
        --project [project-name] \
        --dataset [dataset-name] \
        --table [table_name]
        --num-thread 4



Results
-------

* ref: https://cloud.google.com/bigquery/quotas#table_limits

rateLimitExceeded
>>>>>>>>>>>>>>>>>

* Maximum rate of partition operations: 50 partition operations every 10 seconds

.. code-block:: python

    [{'reason': 'rateLimitExceeded', 'location': 'table.write',
    'message': 'Exceeded rate limits: too many table update operations for this table. For more information, see https://cloud.google.com/bigquery/troubleshooting-errors'}]


quotaExceeded
>>>>>>>>>>>>>

* Maximum number of partition modifications per ingestion time partitioned table: 5,000
* Maximum number of partition modifications per column partitioned table: 30,000

.. code-block:: python

      [{'reason': 'quotaExceeded', 'location': 'load_job_per_table.long',
      'message': 'Quota exceeded: Your table exceeded quota for imports or query appends per table. For more information, see https://cloud.google.com/bigquery/troubleshooting-errors'}]
