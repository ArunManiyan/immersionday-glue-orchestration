import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME','BUCKET_NAME','SRC_PREFIX','TRG_PREFIX'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

##constructing the source and target folders
src_path = "s3://"+ args['BUCKET_NAME']+"/"+args['SRC_PREFIX'] +"/"
trg_path = "s3://"+ args['BUCKET_NAME']+"/"+args['TRG_PREFIX']+"/"

print ("source file path:", src_path)

##creating source dataframe from raw table

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

## Dropping columns with NULL values from the source dynamic frame
dropnullfields3 = DropNullFields.apply(frame = srcDyF, transformation_ctx = "dropnullfields3")

##writing to target s3 location
datasink4 = glueContext.write_dynamic_frame.from_options(frame = dropnullfields3, connection_type = "s3", connection_options = {"path": trg_path }, format = "parquet")


job.commit()
