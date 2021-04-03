from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import logger

Base = declarative_base()

class Modals:
    '''Contains the Data Modals upon which DB tables will be generated'''

    class TestTable(Base):
        '''
        Base structure for the table
        '''
        __tablename__ = "testtable"

        id = Column('id', Integer, primary_key=True)
        desc = Column('desc', String)
        status = Column('status', Integer) 
        

class DBEngine:
    
    class _Engine:
        """ Establishes connections and create a global scoped_session """
        def __init__(self):
            
            self.engine = create_engine(
                'sqlite:///demo.db', 
                connect_args={'check_same_thread': False}
            )

            Base.metadata.create_all(bind=self.engine)
            
            self.db_session = scoped_session(
                sessionmaker(
                    autocommit=False, 
                    autoflush=False, 
                    bind=self.engine
                )
            )

            self.modals = {
                'testtable': Modals.TestTable
            }
        
        def insert(self, data, tablename):
            rtn_status = False
            session = self.db_session()

            try:
                for row in data:
                    modal_obj = self.modals[tablename]()
                    for key, value in row.items():
                        setattr(modal_obj, key, value)

                    session.add(modal_obj)

                session.commit()
                logger.log(f"{len(data)} row added to TABLE[{tablename}] in local DB", 'info')
                rtn_status = True
            
            except Exception as ex:
                logger.log(f'Insertion in Table[{tablename}] failed: {ex.__cause__}', 'error')
                rtn_status = False
                session.rollback()        
            finally:
                session.close()
                self.db_session.remove()
                return rtn_status

        def select(self, query):

            session = self.db_session()
            results = None
            try:
                results = session.execute(query['query']).fetchall()
                logger.log(f"{len(results)} row selected from TABLE[{query['tablename']}]", 'info')
            except Exception as ex:
                logger.log(f"No rows selected from {query['tablename']}: {ex.__cause__}", 'error')
            finally:
                session.close()
                self.db_session.remove()
                if results is not None:
                    return [dict(row) for row in results]
                
                return None

        def delete(self, query):
            session = self.db_session()
            try:
                session.execute(query['query'])
                session.commit()
                logger.log(f"data deleted from TABLE[{query['tablename']}]", 'info')
            except Exception as ex:
                logger.log(f"No rows deleted from {query['tablename']}: {ex.__cause__}", 'error')
                session.rollback()
            finally:
                session.close()
                self.db_session.remove()

        def set(self, query):
            session = self.db_session()
            try:
                session.execute(self.construct_query(query))
                session.commit()
                logger.log(f"row updated from TABLE[{query['tablename']}]", 'info')
            except Exception as ex:
                logger.log(f"No row updated from TABLE[{query['tablename']}]: {ex.__cause__}", 'error')
                session.rollback()
            finally:
                session.close()
                self.db_session.remove()
        
        def construct_query(self, query):
            q = ''
            i = 0
            for key, value in query['new_values'].items():
                if i != 0:
                    q += ','    
                q += f' {key}={value} '
                i += 1
                
            i = 0
            q += ' WHERE '
            for key, value in query['where'].items():
                if i != 0:
                    q += f' {query["cond"]} '    
                q += f' {key}={value} '
                i += 1
            
            return f'UPDATE {query["tablename"]} SET ' + q

    _engine = _Engine()
    
 