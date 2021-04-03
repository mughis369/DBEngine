from db_engine import DBEngine


if __name__=="__main__":
    engine = DBEngine()

	# insert query
    flag = DBEngine._engine.insert(
        [
            {
                'id': 1, 
                'desc': 'desc of item', 
                'status': 'not updated'
            },
            {
                'id': 2, 
                'desc': 'desc of item', 
                'status': 'not updated'
            },
            {
                'id': 3, 
                'desc': 'desc of item', 
                'status': 'not updated'
            }
        ], 
        'tsettable'
    )
    
    #delete query    
    DBEngine._engine.delete(
        {
            'tablename': 'tsettable',
            'query': 'DELETE from tsettable where id=1'
        }
    )

    #update query
    DBEngine._engine.set(
        {
            'tablename': 'name',
            'cond': 'OR',
            'new_values':{
                'colname0': 'new_value0',
                'colname1': 'new_value1',
                'colname3': 'new_value3',
                'colname2': 'new_value2'
            },
            'where':{
                'colname1': 'value22',
                'colname2': 'value33',
                'colname3': 'value44'
            }
        }
    )

    #select query
    data = DBEngine._engine.select(
        {
            'tablename': 'tsettable',
            'query': 'select * from tsettable'
        }
    )
