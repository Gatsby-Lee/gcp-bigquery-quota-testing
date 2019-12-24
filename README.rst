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
    python load_job_to_standard_table.py create-table \
        --project [project-name] \
        --dataset [dataset-name]


Run load jobs with threads
--------------------------

.. code-block:: bash

    # run load jobs with threads
    python load_job_to_standard_table.py loadjob-with-thread \
        --project [project-name] \
        --dataset [dataset-name] \
        --num-thread 1


Results
-------

* With more than one thread, it encounters `rateLimitExceeded`

.. code-block:: python

    [{'reason': 'rateLimitExceeded', 'location': 'table.write',
    'message': 'Exceeded rate limits: too many table update operations for this table. For more information, see https://cloud.google.com/bigquery/troubleshooting-errors'}]
