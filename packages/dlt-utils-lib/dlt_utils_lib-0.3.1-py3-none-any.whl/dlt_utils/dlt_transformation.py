def apply_partitions(df: DataFrame, partitions: dict):
    # apply partitioning to the dataframe
    if partitions:
        for col_name, expression in partitions.items():
            if expression.replace(" ", "") != '':
                df = df.withColumn(col_name, expr(expression))
    return df
    
def update_cdc_timestamp(df: DataFrame) -> DataFrame:
    # if cdc_timestamp is null or time difference is greater than threshold, set it to the max timestamp in the row
    time_diff_threshold = 5 # 5 days
    timestamp_cols = [col.name for col in df.schema.fields if isinstance(col.dataType, (TimestampType, DateType)) and col.name != 'cdc_timestamp']
    if timestamp_cols:
        max_timestamp_per_row = greatest(*[col(col_name) for col_name in timestamp_cols])
        df = df.withColumn(
            'cdc_timestamp',
            when(
                col('cdc_timestamp').isNull() | 
                (spark_abs(datediff(max_timestamp_per_row, col('cdc_timestamp'))) > time_diff_threshold), 
                max_timestamp_per_row
            ).otherwise(col('cdc_timestamp'))
        )
    return df