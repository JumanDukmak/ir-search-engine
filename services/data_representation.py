import pymysql
import mysql.connector
from mysql.connector import Error


# configuration
host = "localhost"
user = "root"
dbname = "datasets_ir"

# Establish a database connection
connection = pymysql.connect(host=host, user=user, db=dbname)


def get_corpus(dataset:str)->dict[int,str]:

    #print("IN Data Representation Service")
    cursor = connection.cursor()
    
    sql_query = f"SELECT * FROM {dataset}"

    try:
        # execute the SQL query
        cursor.execute(sql_query)
        
        # get all the rows
        rows = cursor.fetchall()

        # row_count = cursor.rowcount
        result_dict = {row[1]: row[2] for row in rows}

        return result_dict

    except Exception as e:
        return {"error": str(e)}

    finally:
        cursor.close()
        #connection.close()

#----------------------------------------------------------------------------------#
def get_documents(dataset:str,docs_ids:list):

    cursor = connection.cursor()

    #values_list = ['11']

    placeholders = ",".join(["%s"] * len(docs_ids))

    if dataset == "lotte":
        query = f"SELECT id_number , text FROM {dataset} WHERE id_number IN ({placeholders})"
    else:
        query = f"SELECT id_right , text_right FROM {dataset} WHERE id_right IN ({placeholders})"

    placeholders = tuple(docs_ids)

    cursor.execute(query, placeholders)

    # Fetch and process the results
    records = cursor.fetchall()

    return records

# Example usage
# table_name = "wikir_corpus"
# m=get_corpus(table_name)
# print(m)
# #records_dict = store_in_dict(rows)

# Print the records stored in the dictionary
# for record in records_dict:
#     print(record)

# Close the connection when done

#connection.close()