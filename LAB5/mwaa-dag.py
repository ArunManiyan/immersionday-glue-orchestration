from datetime import timedelta  
import airflow  
from airflow import DAG  
from airflow.providers.amazon.aws.sensors.s3_prefix import S3PrefixSensor
from airflow.providers.amazon.aws.operators.glue import AwsGlueJobOperator
from airflow.providers.amazon.aws.operators.glue_crawler import AwsGlueCrawlerOperator

## Setting S3 bucket name
S3_BUCKET_NAME = 'glueworkshop-changeme-us-east-1' #enter your S3 bucketname here  

##Configuring DAG 
default_args = {  
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(1),
    'retries': 0,
    'retry_delay': timedelta(minutes=2),
    'provide_context': True,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False
}

dag = DAG(  
    'glue_mwaa_scheduler',
    default_args=default_args,
    dagrun_timeout=timedelta(hours=2),
    schedule_interval='0 3 * * *'
)

##Task to wait for a file to be dropped

s3_sensor = S3PrefixSensor(  
  task_id='s3_sensor',  
  bucket_name=S3_BUCKET_NAME,  
  prefix='data/raw/mwaa-green',  
  dag=dag  
)

##Task to start a glue job
glue_task = AwsGlueJobOperator(  
    task_id="glue_task",  
    job_name='ny-taxi-transformed-console-jb',  
    iam_role_name='AWSGlueServiceRole-default',  
    script_args={'--BUCKET_NAME': S3_BUCKET_NAME,
                 '--JOB_NAME': 'glue-job-mwaa',
                 '--SRC_PREFIX': 'data/raw/mwaa-green',
                 '--TRG_PREFIX': 'target/mwaa-transformed'},
    dag=dag) 



s3_sensor >> glue_task

