""" Importing necessary libraries for the functions we need to use """
from pyspark.sql.functions import *
from pyspark.sql.types import *

'''
    This function will take four arguments: 
    columns: this is an array of all the column names for which one has Data quality check (e.g. [id, name])
    dq: this is an array of all the Data quality SQL Logic for bad records (e.g. [id is null, name like 'wrong%']) 
    comment: this is an array of all the Data quality comments of good records (e.g. [id shouln't be null, name should should not start with 'wrong'])
    df: this is the dataframe that needs to be flagged, i.e. the dataframe where one wishes to add flagging column

    returns: this function returns a dataframe with flagging columns for each record
'''
def flagging(columns, dq, comment, df):
    df_dq = df
    flag_columns = list()
    try: 
        for i, j, k in zip(columns, dq, comment):  
            # creating flagging columns for each record
            df_dq = df_dq.withColumn(f'flag_violation_{i}', expr(f"case when {j} then '{i}: {k}' else Null end"))
            flag_columns.append(f'flag_violation_{i}')
    except Exception as e:
        return f'got error while creating flag columns, error: {e}'
    # combining flagging columns
    try: 
        df_with_combined = (df_dq.withColumn('flag_violation', concat_ws(", ", expr(f"filter(array({', '.join(flag_columns)}), x -> x IS NOT NULL)")))
                                    .withColumn('flag_violation', when(col("flag_violation").isNotNull(), concat(lit("{"), col("flag_violation"), lit("}"))))
                                    .withColumn('flag_violation', when(col("flag_violation") == "{}", None).otherwise(col("flag_violation")))
                                    .drop(*flag_columns))
    except Exception as e:
        return f'got error while combining flag columns, error: {e}'
    return df_with_combined 


'''
    This function will take four arguments: 
    dq_good: this is an array of all the Data quality SQL Logic for good records (e.g. 'id is not null and name in ('f', 'm'))
    dq_bad: this is an array of all the Data quality SQL Logic for bad records (e.g. 'id is null or name not in ('f', 'm')) 
    df: this is the dataframe, that will used for creating quarantine and good dataframes

    returns: this function returns two dataframes df_good and df_bad
'''
def quarantine(dq_good, dq_bad, df):
    try: 
        df_good = df.filter(expr(dq_good))
        df_bad = df.filter(expr(dq_bad))
    except Exception as e:
        return f'Error while creating good and bad dataframes, error: {e}'
    return df_good, df_bad 
