# ==================== #
#                      #
#        imports       #
#                      #
# ==================== #

from pathlib import Path
import dlt
import dagster as dg

from dagster_dlt import DagsterDltResource, dlt_assets
from dagster_dbt import DbtCliResource, DbtProject, dbt_assets
from data_extract.extract_data_update import nobil_source
from pathlib import Path


# path to duckdb
# db_path = str(Path(__file__).parents[1] / "data_warehouse/data.duckdb")

# This create a Dagster resource
dlt_resource = DagsterDltResource()





# ==================== #
#                      #
#     dlt assets       #
#                      #
# ==================== #

# This is the same idea for when you run dlt seperently. But here it create a Dagster asset for every dlt.resource
# It's the bridge between dlt and Dagster
@dlt_assets(
    dlt_source=nobil_source(),
    dlt_pipeline=dlt.pipeline(
        pipeline_name="nobil_pipeline",
        dataset_name="staging",
        destination="snowflake",
    ),
)
def dlt_load(context: dg.AssetExecutionContext,dlt: DagsterDltResource):
    yield from dlt.run(context=context)





# ==================== #
#                      #
#      dbt assets      #
#                      #
# ==================== #

dbt_project_dir = Path(__file__).parents[1] / "data_transform"
profiles_dir = Path.home() / ".dbt"

dbt_project = DbtProject(
    project_dir=dbt_project_dir,
    profiles_dir=profiles_dir,
)

dbt_resource = DbtCliResource(project_dir=dbt_project)

# This important for Dagster to understand the dbt linage
dbt_project.prepare_if_dev()


@dbt_assets(manifest=dbt_project.manifest_path)
def dbt_models(context: dg.AssetExecutionContext, dbt: DbtCliResource,):
    yield from dbt.cli(["build"], context=context).stream()





# ==================== #
#                      #
#         jobs         #
#                      #
# ==================== #

# Run ALL dlt-assets from nobil_source
job_dlt = dg.define_asset_job(
    name="job_dlt",
    selection=dg.AssetSelection.keys(
        dg.AssetKey("dlt_nobil_source_csmd_data"),
        dg.AssetKey("dlt_nobil_source_status_online_data"),
        dg.AssetKey("dlt_nobil_source_connector_data"),
    )
)

# This will run all of the dbt-modells
job_dbt = dg.define_asset_job(
    name="job_dbt",
    selection=dg.AssetSelection.key_prefixes("warehouse", "marts")
    | dg.AssetSelection.keys("municipality_lan")
)




# ==================== #
#                      #
#       schedule       #
#                      #
# ==================== #

schedule_dlt = dg.ScheduleDefinition(
    job=job_dlt,
    cron_schedule="0 02 * * *",  # 02:00 UTC
)





# ==================== #
#                      #
#        sensor        #
#                      #
# ==================== #

# A sensor that will trigger when dlt job is materialized
@dg.run_status_sensor(
    run_status=dg.DagsterRunStatus.SUCCESS,
    monitored_jobs=[job_dlt],
    request_job=job_dbt,
)
def dlt_success_trigger(context):
    yield dg.RunRequest(run_key=context.dagster_run.run_id)




# ==================== #
#                      #
#     definitions      #
#                      #
# ==================== #

# Dagster object that contains the dbt assets and resource
defs = dg.Definitions(
    assets=[dlt_load, dbt_models],
    resources={ "dlt": dlt_resource, "dbt": dbt_resource},
    jobs=[job_dlt, job_dbt],
    schedules=[schedule_dlt],
    sensors=[dlt_success_trigger]
)
