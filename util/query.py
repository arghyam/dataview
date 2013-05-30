from models import * 

def getTables(query_json):
    table_alias_dict = {}
    for row in query_json:
        for key in row.iterkeys():
            if key.startswith("datatable_id"):
                data_table_id = row[key]
                #table = DataTable.query.filter_by(data_table_id=data_table_id).first()
                table_alias = "values_data_table_"+str(data_table_id)
                table_alias_dict[table_alias]=table_alias
    return table_alias_dict

def getWhereClause(query_json):
    operations = {"equals":"=","greater":">","lesser":"<"}
    where_query = ""
    for row in query_json:
        table1 = " values_data_table_"+str(row["datatable_id1"])
        column1_id = row["datatable_column1"]
        data_column1 = DataColumn.query.filter_by(data_column_id=int(column1_id)).first()
        where_query = where_query+" "+table1+"."+data_column1.data_column_short_name+" "
        
        operation = row["operation"]
        where_query = where_query+" "+operations[operation]+" "


        table2 = " values_data_table_"+str(row["datatable_id2"])

        column2_id = row["datatable_column2"]
        data_column2 = DataColumn.query.filter_by(data_column_id=int(column2_id)).first()
        where_query = where_query+" "+table2+"."+data_column2.data_column_short_name+" "

        where_query = where_query+"  and "

    where_query = where_query[:-4]
        

    return where_query    