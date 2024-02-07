import pandas as pd
import pandasql as psql


def get_coordinates(lineage_object_id):

    # Replace 'your_file.csv' with the path to your CSV file
    csv_file_path = r'data/result.csv'

    # Define the variable
    lineage_object_id_value = lineage_object_id

    # Read the CSV file into a DataFrame
    src_df = pd.read_csv(csv_file_path)

    # to fetch job details
    job_file_path = r'data/DBTjobs.csv'
    jobs = pd.read_csv(job_file_path)

    # to fetch report details
    report_file_path = r'data/reports.csv'
    report = pd.read_csv(report_file_path)

    # Define the SQL query
    sql_query = f"""
        with final_all as (
            select * from src_df 
            where lineage_object_id='{lineage_object_id_value}'
        ),
        graph as (
            select DISTINCT 
            lineage_object_id,
            source_schema as model_schema,
            source_table_id as model_name,
            node_type,
            loaded_through,
            max(level_num) as LEVEL
            from final_all where level_num<0
            group by 1,2,3,4,5

            union ALL

            select DISTINCT 
            lineage_object_id,
            target_schema as model_schema,
            target_table_id as model_name,
            node_type,
            loaded_through,
            max(level_num) as LEVEL
            from final_all where level_num>=0
            group by 1,2,3,4,5

            order by level,model_schema,model_name
        ),
        GRAPH_2 AS (
            SELECT *,COUNT(*) OVER (PARTITION BY LEVEL) CNT,
            ROW_NUMBER() OVER (PARTITION BY LEVEL ORDER BY model_name) RN,
            TRUNC(COUNT(*) OVER (PARTITION BY LEVEL)/2) as INDEX_ALIAS
            FROM GRAPH ORDER BY LEVEL,RN
        ),
        COORDINATES AS (
            SELECT 
            MODEL_NAME as MODEL_NAME,
            (MODEL_SCHEMA||'.'||MODEL_NAME) AS OBJECT,LEVEL AS X,
            CASE WHEN mod(CNT,2)=0 THEN INDEX_ALIAS+0.5-RN ELSE INDEX_ALIAS+1-RN END AS Y
            FROM GRAPH_2
            ORDER BY LEVEL,Y
        )
        select * from COORDINATES order by x,y;
    """

    sql_query_job = f"""
        select distinct case when DBT_JOB_NAME is null then DBT_CLOUD_JOB_ID else DBT_JOB_NAME end as JOB_NAME, CASE WHEN NEXT_RUN IS NULL THEN DBT_CLOUD_RUN_REASON ELSE 'Triggered via DBT' END AS RunTrigger,
        datetime(LATEST_RUN_STARTED_AT) as Last_run_at,STATUS as Last_Run_Status,CASE WHEN NEXT_RUN IS NULL THEN 'NA' ELSE CRON_HUMANIZED END AS Schedule
        from jobs
        where (TRIGGERS_SCHEDULE=1 OR TRIGGERS_SCHEDULE IS NULL) AND MODEL_NAME='{lineage_object_id_value}'  
        order by LATEST_RUN_STARTED_AT desc;
    """

    sql_query_report = f"""
        select distinct target_schema AS SCHEMA,table_name AS OBJECT,report from (
        SELECT distinct case when trim(DASHBOARD_NAME)<>trim(WORKBOOK_NAME) then upper(DASHBOARD_NAME || '^' || WORKBOOK_NAME) else upper(DASHBOARD_NAME || '^' || WORKBOOK_NAME) end as Report,table_name,target_schema,project_name  
        FROM report b
        left join src_df a on a.target_table_id = b.table_name)
        where lower(project_name) not like 'personal%' and table_name='{lineage_object_id_value}' and target_schema is not null
        order by object,LENGTH(report);
    """    


    # Execute the SQL query on the DataFrame
    coordinate_df = psql.sqldf(sql_query, locals())

    jobs_df = psql.sqldf(sql_query_job, locals())

    reports_df = psql.sqldf(sql_query_report, locals())

    # Display the result DataFrame
    return [coordinate_df, jobs_df, reports_df]