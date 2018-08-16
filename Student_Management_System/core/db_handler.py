#Downtiser
'''To handle the database'''
from Student_Management_System.conf import SETTINGS
import json


def db_engine():
    '''
    Get the MySQL engine information from settings
    :return: The engine's URL
    '''
    db_type = SETTINGS.db_config['db_type']
    db_driver = SETTINGS.db_config['db_driver']
    db_manager = SETTINGS.db_config['db_manager']
    db_password = SETTINGS.db_config['db_password']
    db_host = SETTINGS.db_config['db_host']
    db_name = SETTINGS.db_config['db_name']
    engine = '%s+%s://%s:%s@%s/%s?charset=utf8'%(db_type,
                                                 db_driver,
                                                 db_manager,
                                                 db_password,
                                                 db_host,
                                                 db_name)
    return engine

def update_grade_list(name):
    '''
    To save time, store the new grade name in local
    FileStorage
    :param name: The grade's name
    :return:
    '''
    path = SETTINGS.local_db_info['path'] + '/grade_list.json'
    f = open(path, 'r', encoding='utf-8')
    grade_list = json.loads(f.read())
    f.close()
    grade_list.append(name)
    f = open(path, 'w', encoding='utf-8')
    f.write(json.dumps(grade_list))
    f.close()
def update_score_list(name):
    '''
    Similar to `update_grade_list()`
    :param name:
    :return:
    '''
    path = SETTINGS.local_db_info['path'] + '/score_list.json'
    f = open(path, 'r', encoding='utf-8')
    score_list = json.loads(f.read())
    f.close()
    score_list.append(name)
    f = open(path, 'w', encoding='utf-8')
    f.write(json.dumps(score_list))
    f.close()
def load_grade_list():
    '''
    Load grade's name from local storage
    :return: A list contain existed grade's name
    '''
    path = SETTINGS.local_db_info['path'] + '/grade_list.json'
    f = open(path, 'r', encoding='utf-8')
    grade_list = json.loads(f.read())
    f.close()
    return grade_list

def load_score_list():
    '''
    Similar to `load_grade_list()`
    :return:
    '''
    path = SETTINGS.local_db_info['path'] + '/score_list.json'
    f = open(path, 'r', encoding='utf-8')
    score_list = json.loads(f.read())
    f.close()
    return score_list