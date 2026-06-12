from airflow import DAG
import pendulum
from datetime import timedelta, datetime
from api.video_stats import get_playlist_id, get_video_ids, extract_video_data, save_to_json
from datawarehouse.dwh import staging_table, core_table
from dataquality.soda import yt_elt_data_quality

#Define the local timezone
local_tz = pendulum.timezone("Europe/Riga")

#Default Args
default_args = {
    "owner": "dataengineers",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "email":"hello@raivis.it",
    # "retries": 1,
    # "retry_delay": timedelta(minutes=5),
    "max_active_runs": 1,
    "dagrun_timeout": timedelta(minutes=60),
    "start_date": datetime(2026, 5, 27, tzinfo=local_tz),
    # "end_date": datetime(2024, 6, 30, tzinfo=local_tz)
}

# Variables
staging_schema = "staging"
core_schema = "core"

with DAG(
     dag_id="produce_json",
     default_args=default_args,
     description="A DAG to extract video stats from YouTube API and save it as JSON",
     schedule="0 14 * * *", # Run daily at 14:00 (2 PM) local time
     catchup=False
) as dag:
    
    # Define the tasks
    playlist_id = get_playlist_id()
    video_ids = get_video_ids(playlist_id)
    extracted_data = extract_video_data(video_ids)
    save_to_json_task = save_to_json(extracted_data)

    # Define dependencies
    playlist_id >> video_ids >> extracted_data >> save_to_json_task
    
with DAG(
     dag_id="update_db",
     default_args=default_args,
     description="DAG to process JSON file and insert data into the staging and core schemas",
     schedule="0 15 * * *", # Run daily at 15:00 (3 PM) local time
     catchup=False
) as dag:
    
    # Define the tasks
    update_staging = staging_table()
    update_core = core_table()

    # Define dependencies
    update_staging >> update_core

with DAG(
     dag_id="data_quality",
     default_args=default_args,
     description="DAG to check the data quality on both layers in the db",
     schedule="0 16 * * *", # Run daily at 16:00 (4 PM) local time
     catchup=False
) as dag:
    
    # Define the tasks
    soda_validate_staging = yt_elt_data_quality(staging_schema)
    soda_validate_core = yt_elt_data_quality(core_schema)

    # Define dependencies
    soda_validate_staging >> soda_validate_core