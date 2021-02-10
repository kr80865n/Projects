import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

job.init(args['JOB_NAME'], args)

location = f'.sparkStaging/{sc.applicationId}/areas.json'
print("TEST - Loading areas.json from HDFS into a Spark DataFrame")
print("========================================")
df = spark.read.format("json").load(location)
df.printSchema()
print("========================================")
df.show()
print("========================================")

job.commit()
