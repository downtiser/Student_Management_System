#Downtiser
from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from Student_Management_System.core import db_handler, table_handler
class StudentView(object):
    '''The main class to create a object can interact
    with mysql as a student view
    '''
    def __init__(self):
        '''Do some initialization job for
        some command
        '''
        self.operation_dict = {
            '1':self.submit_homework,
            '2':self.query_score,
            '3':self.query_rank

        }
        self.engine = create_engine(db_handler.db_engine(), encoding='utf-8')
        self.Session_class = sessionmaker()
        self.session = self.Session_class(bind=self.engine)

    def run(self):
        '''
        Contact with MySQL and map the table in database
        :return:
        '''
        Base = declarative_base()
        student_2_grade = table_handler.bind_student_m2m_grade(Base)
        StudentInfo = table_handler.bind_student_info_table(Base, student_2_grade)
        GradesTable = table_handler.bind_grades(Base)
        while True:
            stu_id = input('Please input your student id or q to quit>>>')
            if stu_id == 'q':
                exit('Quit successfully!')
            if not stu_id.isdigit() or '.' in stu_id:
                print('Invalid student id!')
                continue
            stu_id = int(stu_id)
            if len(self.session.query(StudentInfo).filter(StudentInfo.stu_id == stu_id).all()) == 0:
                print('The id does not exist, please check your input!')
                continue
            self.stu_obj = self.session.query(StudentInfo).filter(StudentInfo.stu_id == stu_id).first()
            print('\033[32;1mWelcome! %s!\033[0m'%self.stu_obj.name)
            print('----Your Grade----')
            Grade_obj_list = self.stu_obj.grades
            while True:
                for i, obj in enumerate(Grade_obj_list):
                    print(i+1, 'Grade ID:[%s] Grade Name:[%s]'%(obj.grade_id, obj.grade_name))
                user_choice = input('Please choose a grade or q to quit>>>')
                if user_choice.isdigit() and int(user_choice) > 0 and int(user_choice) <= len(Grade_obj_list):
                    self.Base = declarative_base()
                    self.grade_obj = Grade_obj_list[int(user_choice) - 1]
                    self.Grade = table_handler.bind_grade_table(self.grade_obj.grade_name, self.Base)
                    self.Record = table_handler.bind_record_table(self.grade_obj.grade_name, self.Base)
                    self.Period = table_handler.bind_period_table(self.grade_obj.grade_name, self.Base)
                    self.student_2_grade = table_handler.bind_student_m2m_grade(self.Base)
                    self.StudentInfo = table_handler.bind_student_info_table(self.Base, self.student_2_grade)
                    self.GradesTable = table_handler.bind_grades(self.Base)
                    while True:
                        print('----Operation List----')
                        print('1 submit your home work')
                        print('2 query your score')
                        print('3 query your rank')
                        user_choice2 = input('Please choose a operation or q to quit>>>')
                        if user_choice2 in self.operation_dict:
                            self.operation_dict[user_choice2]()
                        elif user_choice2 == 'q':
                            break
                        else:
                            print('Invalid input!')
                            continue
                elif user_choice == 'q':
                    break
                else:
                    print('Invalid input!')
                    continue

    def submit_homework(self):
        '''
        For student to submit their homework
        :return:
        '''
        while True:
            record_list = self.session.query(self.Record).filter(self.Record.stu_id == self.stu_obj.stu_id).all()
            for i, item in enumerate(record_list):
                print(i+1,'Day:[%s] commit:[%s]'%(item.day, item.commit))
            user_choice = input('Please choose a day to submit or q to quit>>>')
            if user_choice.isdigit() and int(user_choice) > 0 and int(user_choice) <= len(record_list):
                record_obj = record_list[int(user_choice) - 1]
                if record_obj.commit == 'no':
                    print('Ops! The deadline has passed!')
                    continue
                else:
                    record_obj.commit = 'yes'
                    self.session.commit()
                    print('Done!')
            elif user_choice == 'q':
                break
            else:
                print('invalid input!')
                continue


    def query_score(self):
        '''
        For student to query their score
        :return:
        '''
        record_list = self.session.query(self.Record).filter(self.Record.stu_id == self.stu_obj.stu_id).all()
        for i, item in enumerate(record_list):
            print(i + 1, 'Day:[%s] commit:[%s] score:[%s]' % (item.day, item.commit, item.score))
        input('input any value to quit>>>')

    def query_rank(self):
        '''
        For student to query their rank in their
        grade
        :return:
        '''
        record_list = self.session.query(self.Record.stu_id, func.sum(self.Record.score)).group_by(self.Record.stu_id).order_by(func.sum(self.Record.score).desc()).all()
        rank = 0
        total_score = 0
        for i, item in enumerate(record_list):
            if item[0] == self.stu_obj.stu_id:
                rank = i + 1
                total_score = item[1]
                break
        print('Your total score :[%s] Your Rank:[%s] The amount of student:[%s]'%(total_score,rank, len(record_list)))
        input('input any value to quit>>>')
