#Downtiser
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from Student_Management_System.core import db_handler

engine_info = db_handler.db_engine()
engine = create_engine(engine_info, encoding='utf-8')
def create_grade(grade_name):
    '''
    when teacher create a new grade, the function
    will be called, and according to the parameter
    grade_name to create specific tables in mysql
    :param grade_name:
    :return:
    '''
    Base = declarative_base()
    class Grade(Base):
        __tablename__ = grade_name + '_grade'
        id = Column(Integer, primary_key=True)
        stu_id = Column(Integer, unique=True, nullable=False)
        name = Column(String(32), nullable=False)
    db_handler.update_grade_list(grade_name)

    class Period(Base):
        __tablename__ = grade_name + '_period'
        id = Column(Integer, primary_key=True)
        day = Column(Integer, unique=True, nullable=False)
        content = Column(String(128))

    class Record(Base):
        __tablename__ = grade_name + '_record'
        id = Column(Integer, primary_key=True)
        day = Column(Integer, ForeignKey(Period.__tablename__), nullable=False)
        stu_id = Column(Integer, ForeignKey(Grade.__tablename__), nullable=False)
        statue = Column(String(32), nullable=False, default='/')
        commit = Column(String(32), nullable=False, default='/')
        score = Column(Integer, nullable=False, default=0)
    db_handler.update_score_list(Record.__tablename__)
    Base.metadata.create_all(engine)




