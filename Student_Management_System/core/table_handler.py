#Downtiser
'''The main module to map tables between mysql
and the Project
'''
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Enum, Table
from sqlalchemy.orm import relationship
from Student_Management_System.core import db_handler
engine_info = db_handler.db_engine()
engine = create_engine(engine_info, encoding='utf-8')

def bind_grade_table(grade_name, Base):
    '''
    To map grade table in mysql through table name
    :param grade_name:
    :param Base:
    :return:
    '''
    class Grade(Base):
        __tablename__ = grade_name + '_grade'
        id = Column(Integer, primary_key=True)
        stu_id = Column(Integer, ForeignKey('student_info.stu_id'),unique=True, nullable=False)
        name = Column(String(32), nullable=False)
    return Grade

def bind_record_table(grade_name, Base):
    '''
    To map record table in mysql through table name
    :param grade_name:
    :param Base:
    :return:
    '''
    class Record(Base):
        __tablename__ = grade_name + '_record'

        id = Column(Integer, primary_key=True)
        day = Column(Integer, ForeignKey(grade_name + '_period.day'), nullable=False)
        stu_id = Column(Integer, ForeignKey(grade_name + '_grade.stu_id'), nullable=False)
        statue = Column(String(32), nullable=False, default='/')
        commit = Column(String(32), nullable=False, default='/')
        score = Column(Integer, nullable=False, default=0)
        grade_info = relationship('Grade', backref='record')

    return  Record

def bind_period_table(grade_name, Base):
    '''
    To map period table in mysql through table name
    :param grade_name:
    :param Base:
    :return:
    '''
    class Period(Base):
        __tablename__ = grade_name + '_period'

        id = Column(Integer, primary_key=True)
        day = Column(Integer, unique=True, nullable=False)
        content = Column(String(128))
    return Period

def bind_student_info_table(Base, student_2_grade):
    '''
    To map global student information table in mysql and
    create many to many foreign key between this table and
    GradesTable
    :param Base:
    :param student_2_grade:
    :return:
    '''
    class StudentInfo(Base):
        __tablename__ = 'student_info'
        id = Column(Integer, primary_key=True)
        stu_id = Column(Integer, unique=True, nullable=False)
        name = Column(String(32), nullable=False)
        gender = Column(Enum("Male","Female","MF"))
        address = Column(String(64),default='/')
        phone = Column(String(32),default='/')
        grades = relationship('GradesTable', secondary=student_2_grade, backref='students')
    return StudentInfo
def bind_grades(Base):
    '''
    Map the GradesTable
    :param Base:
    :return:
    '''
    class GradesTable(Base):
        __tablename__ = 'grade_info'
        id = Column(Integer, primary_key=True)
        grade_id = Column(Integer, unique=True, nullable=False)
        grade_name = Column(String(64), nullable=False)
        grade_price = Column(Integer, nullable=False)
    return GradesTable
def bind_student_m2m_grade(Base):
    '''
    Map the secondary table
    :param Base:
    :return:
    '''
    student_2_grade = Table('student_2_grade', Base.metadata,
                            Column('stu_id', Integer, ForeignKey('student_info.stu_id')),
                            Column('grade_id', Integer, ForeignKey('grade_info.grade_id'))

    )
    return student_2_grade


def Grades_table(Base):
    class GradesTable(Base):
        __tablename__ = 'grade_info'
        id = Column(Integer, primary_key=True)
        grade_id = Column(Integer, unique=True, nullable=False)
        grade_name = Column(String(64), nullable=False)
        grade_price = Column(Integer, nullable=False)
    return GradesTable

def StudentRegistration(Base):
    class StudentInfo(Base):
        __tablename__ = 'student_info'
        id = Column(Integer, primary_key=True)
        stu_id = Column(Integer, unique=True, nullable=False)
        name = Column(String(32), nullable=False)
        gender = Column(Enum("Male","Female","MF"))
        address = Column(String(64), default='/')
        phone = Column(String(32), default='/')
    return StudentInfo

