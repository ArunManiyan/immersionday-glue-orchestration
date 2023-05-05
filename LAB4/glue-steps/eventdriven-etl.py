import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME','bucketName','key'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
job.commit()
src_path = "s3://"+args['bucketName']+'/'+args['key']
trg_path = "s3://"+args['bucketName']+'/target/eventdriven/'
print("FileName:",src_path)


srcDyF  = glueContext.create_dynamic_frame.from_options(
    format_options={"quoteChar": '"', "withHeader": True, "separator": ","},
    connection_type="s3",
    format="csv",
    connection_options={
        "paths": [src_path],
        "recurse": True,
    },
  
)

srcDyF.show(10)

datasink4 = glueContext.write_dynamic_frame.from_options(frame = srcDyF, connection_type = "s3", connection_options = {"path": trg_path }, format = "parquet")
