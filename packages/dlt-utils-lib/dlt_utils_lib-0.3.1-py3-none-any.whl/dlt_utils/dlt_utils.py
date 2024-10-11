from pyspark.sql.functions import col, expr
import dlt

def create_bronze_table_definition(table_name, files_path, file_format, schema_exclude_columns):
    @dlt.table(
        name=f"bronze_{table_name}",
        comment="This is the bronze table.",
        temporary=False
    )
    def transform_cdc_to_bronze():
        df = spark.read.format(file_format).load(files_path)
        fields = [field for field in df.schema.fields if field.name not in schema_exclude_columns]
        schema_string = ', '.join([f"{field.name} {field.dataType.simpleString()}" for field in fields])
        return spark \
            .readStream \
            .format('cloudFiles') \
            .option("cloudFiles.format", file_format) \
            .option("cloudFiles.schemaHints", schema_string) \
            .load(files_path) \
            .withColumn('cdc_timestamp', col('cdc_timestamp').cast('timestamp'))

    return transform_cdc_to_bronze

def silver_streaming_process(table_name, keys, partition_col, exclude_columns):
    dlt.create_streaming_table(
        name=table_name,
        table_properties={
            "delta.autoOptimize.optimizeWrite": "true",
            "delta.autoOptimize.autoCompact": "true"
        },
        comment="This is the silver table with source in",
        partition_cols=partition_col if partition_col else None
    )

    dlt.apply_changes(
        target=table_name,
        source=f"bronze_{table_name}",
        keys=keys,
        sequence_by=col("cdc_timestamp"),
        apply_as_deletes=expr("Op = 'D'"),
        apply_as_truncates=expr("Op = 'T'"),
        except_column_list=["Op", "_rescued_data"] + exclude_columns,
        stored_as_scd_type=1
    )