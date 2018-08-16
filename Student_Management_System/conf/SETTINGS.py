#Downtiser
'''Store the database config information'''
import os
db_config = {
    'db_type':'mysql',
    'db_driver':'mysqlconnector',
    'db_manager':'root',
    'db_password':'gu996080',
    'db_host':'localhost',
    'db_name':'ManagementSystem'
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
local_db_info = {
    'path':BASE_DIR + '/data',
    'type':'FileStorage'

}