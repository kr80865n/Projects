import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job

glueContext = GlueContext(SparkContext.getOrCreate())
spark = glueContext.spark_session
job = Job(glueContext)
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

job.init(args['JOB_NAME'], args)

### CODE STARTS HERE ###



# Create an empty dictionary and use it to load the contents of the JSON file taken from "Referenced files path":
filejson = {}
with open('areas.json', 'r') as inputfile:
   filejson = eval(inputfile.read())

# Create a Spark DataFrame with data from the JSON file:
df = glueContext.createDataFrame(
    [
        (filejson[0]["id"], filejson[0]["name"]),
        (filejson[1]["id"], filejson[1]["name"]),
        (filejson[2]["id"], filejson[2]["name"]),
        (filejson[3]["id"], filejson[3]["name"]),
        (filejson[4]["id"], filejson[4]["name"]),
        (filejson[5]["id"], filejson[5]["name"]),
        (filejson[6]["id"], filejson[6]["name"]),
        (filejson[7]["id"], filejson[7]["name"]),
        (filejson[8]["id"], filejson[8]["name"]),
        (filejson[9]["id"], filejson[9]["name"])
    ],
    ['id', 'name']
)

# Check 'df' contents:
df.printSchema()
df.show()

# Convert 'df' to Glue DynamicFrame:
dyf = DynamicFrame.fromDF(df, glueContext, "dftodyf")

# Repartition to 12 to achieve maximum parallelization based on my DPUs config:
dyf_rep = dyf.repartition(12)

# Write the outut into S3 in JSON format:
datasink = glueContext.write_dynamic_frame.from_options(frame = dyf_rep, connection_type = "s3", connection_options = {"path": my_output_s3Path}, format = "json", transformation_ctx = "datasink")

### CODE ENDS HERE ###

job.commit()