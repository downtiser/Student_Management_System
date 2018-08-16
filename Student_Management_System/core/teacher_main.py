#Downtiser
'''The main logical module to do interact job with
mysql
'''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from Student_Management_System.core import db_handler, table_creator, table_handler
import warnings
#warnings.filterwarnings('ignore')
class TeacherView(object):
    '''
    The main class to build a teacher view
    environment through instantiating a object
    with several attributes
    '''
    def __init__(self):
        '''
        Do some prepares to connect to mysql and
        some command
        '''
        self.manage_operation_dict = {
            '1':self.manage_grade,
            '2':self.create_grade,
            '3':self.upload_student_info
        }
        self.modify_operation_dict = {
            '1':self.modify_record,
            '2':self.add_member,
            '3':self.query_student_record,
            '4':self.add_period
        }
        self.engine = create_engine(db_handler.db_engine(), encoding = 'utf-8')
        self.Session_class = sessionmaker()
        self.session = self.Session_class(bind=self.engine)



    def run(self):
        '''
        Start deal with the user' request
        :return:
        '''
        while True:
            print('\033[32;1m----Manage List----\033[0m')
            print('1 manage your grade')
            print('2 create a grade')
            print('3 student registration')

            user_choice = input('Please choose an operation or input q to quit>>>').strip()
            if user_choice in self.manage_operation_dict:
                self.manage_operation_dict[user_choice]()
            elif user_choice == 'q':
                exit('Quit successfully!')
            else:
                print('invalid input!')
                continue

    def upload_student_info(self):
        '''
        To do registration work for new student
        :return:
        '''
        Base = declarative_base()
        student_2_grade = table_handler.bind_student_m2m_grade(Base)
        StudentRegistration = table_handler.StudentRegistration(Base)
        stu_obj_list = []
        while True:
            stu_id = input('please input the student id or q to quit>>>').strip()
            if stu_id == 'q':
                break
            elif not stu_id.isdigit() or '.' in stu_id:
                print('\033[31;1mInvalid student id!\033[0m')
                continue
            stu_id = int(stu_id)
            if len(self.session.query(StudentRegistration).filter(StudentRegistration.stu_id == stu_id).all()) != 0:
                print('\033[31;1mThe student already exist!\033[0m')
                continue
            name = input('please input the student name>>>')
            gender = input("please input the student's gender(Male/Female/MF)>>>")
            address = input("please input the student's address>>>")
            phone = input("please input the student's phone number>>>")
            stu_obj = StudentRegistration(stu_id=stu_id, name=name, gender=gender, address=address, phone=phone)
            stu_obj_list.append(stu_obj)
            print("Added student's amount:[%s]"%len(stu_obj_list))
        self.session.add_all(stu_obj_list)
        self.session.commit()
        print('\033[32;1mDone!\033[0m')

    def manage_grade(self):
        '''
        Start to manage a specific grade
        :return:
        '''
        while True:
            self.Base = declarative_base()
            self.GradesTable = table_handler.bind_grades(self.Base)
            self.grade_list = self.session.query(self.GradesTable).all()
            print('\033[32;1m----Grade list----\033[0m')
            for i, item in enumerate(self.grade_list):
                print(i+1, 'Grade ID:[%s] Grade Name:[%s]'%(item.grade_id, item.grade_name))
            user_choice = input('Please choose a grade or input q to quit>>>').strip()
            if user_choice.isdigit() and int(user_choice) > 0 and int(user_choice) <= len(self.grade_list):
                #self.Base.metadata.drop_all(self.engine)
                self.grade = self.grade_list[int(user_choice) - 1].grade_name
                self.grade_id = self.grade_list[int(user_choice) - 1].grade_id
                self.Grade = table_handler.bind_grade_table(self.grade, self.Base)
                self.Record = table_handler.bind_record_table(self.grade, self.Base)
                self.Period = table_handler.bind_period_table(self.grade, self.Base)
                self.Student_2_grade = table_handler.bind_student_m2m_grade(self.Base)
                self.StudentInfo = table_handler.bind_student_info_table(self.Base, self.Student_2_grade)
                while True:
                    print('\033[32;1m----Operation List----\033[0m')
                    print('1 modify student record')
                    print('2 add new member')
                    print('3 query student record')
                    print('4 add course period')
                    user_choice2 = input('please choose an operation or input q to quit>>>').strip()
                    if user_choice2 in self.modify_operation_dict:
                        self.modify_operation_dict[user_choice2]()
                    elif user_choice2 == 'q':
                        break
                    else:
                        print('invalid input!')
                        continue
            elif user_choice == 'q':
                break
            else:
                print('invalid input!')
                continue
    def create_grade(self):
        '''
        To create a new grade as well as creating
        relative tables in mysql.
        :return:
        '''
        Base = declarative_base()
        GradesTable = table_handler.Grades_table(Base)
        self.grade_list = db_handler.load_grade_list()
        while True:
            grade_name = input('please input the grade name or q to quit>>>')
            if grade_name == 'q':
                break
            grade_id = input('please input the grade id>>>')
            if grade_name == 'q':
                break
            if not grade_id.isdigit() or '.' in grade_id:
                print('\033[31;1minvalid grade id!\033[0m')
                continue
            grade_id = int(grade_id)
            if len(self.session.query(GradesTable).filter(GradesTable.grade_id == grade_id).all()) != 0:
                print('\033[31;1mThe Grade id already exist, please change to another one!\033[0m')
                continue
            if grade_name in self.grade_list:
                print('\033[31;1mThe grade name already exist!\033[0m')
                continue
            else:
                grade_price = input('please input the grade price>>>')
                if not grade_price.isdigit():
                    print('\033[31;1mInvalid price!\033[0m')
                    continue
                grade_price = float(grade_price)
                table_creator.create_grade(grade_name)
                grade_obj = GradesTable(grade_id=grade_id, grade_name=grade_name, grade_price=grade_price)
                self.session.add(grade_obj)
                self.session.commit()
                print('Done!')

    def add_period(self):
        '''
        To add course outlines
        :return:
        '''
        while True:
            day_period_list = self.session.query(self.Period).all()
            for item in day_period_list:
                print('Day:[%s]  Content:[%s]'%(item.day, item.content))
            day = input('please input the day you want to add or q to quit>>>')
            if day == 'q':
                break
            elif not day.isdigit() or '.' in day:
                print('invalid input!')
                continue
            day = int(day)
            if len(self.session.query(self.Period).filter(self.Period.day == day).all()) != 0:
                print("The day's period already exist!")
                continue
            else:
                content = input('Please input the content>>>')
                period_obj = self.Period(day=day, content=content)
                self.session.add(period_obj)
                self.session.commit()

    def query_student_record(self):
        '''
        To query student's record in mysql
        :return:
        '''
        while True:
            user_choice = input('Input full to query the whole record or q to quit or any other value to specify a day record>>>')
            if user_choice == 'q':
                break
            if user_choice == 'full':
                record_list = self.session.query(self.Record).all()
                for item in record_list:
                    print('Day:[%s] Student ID:[%s] Student Name:[%s] Statue:[%s] Commit:[%s] Score:[%s]'%(item.day,
                                                                                                  item.stu_id,
                                                                                                  item.grade_info.name,
                                                                                                  item.statue,
                                                                                                  item.commit,
                                                                                                  item.score
                                                                                                  ))
            else:
                while True:
                    day = input('please choose a day, or q to quit>>>')
                    if day == 'q':
                        break
                    elif not day.isdigit() or '.' in day:
                        print('invalid input!')
                        continue
                    day = int(day)
                    record_list = self.session.query(self.Record).filter(self.Record.day == day).all()
                    if len(record_list) == 0:
                        print("The day's record not found, dump the day's records first!")
                        continue
                    else:
                        for item in record_list:
                            print('Day:[%s] Student ID:[%s] Student Name:[%s] Statue:[%s] Commit:[%s] Score:[%s]'%(item.day,
                                                                                                            item.stu_id,
                                                                                                            item.grade_info.name,
                                                                                                            item.statue,
                                                                                                            item.commit,
                                                                                                            item.score
                                                                                                            ))

    def modify_record(self):
        '''
        To start modify the record table
        :return:
        '''
        operation_dict = {
            '1':self.add_study_record,
            '2':self.add_score
        }
        while True:
            print('1 add study record')
            print('2 add score')
            user_choice = input('please choose a operation or q to quit>>>')
            if user_choice in operation_dict:
                operation_dict[user_choice]()
            elif user_choice == 'q':
                break
            else:
                print('invalid input!')
                continue

    def add_study_record(self):
        '''
        To add student's study record
        :return:
        '''
        while True:
            day = input('please choose a day, or q to quit>>>')
            if day == 'q':
                break
            elif not day.isdigit() or '.' in day:
                print('invalid input!')
                continue
            day = int(day)
            if len(self.session.query(self.Period).filter(self.Period.day == day).all()) == 0:
                print("The day's period not found, please add the day's period first!")
                continue
            record_obj_list = []
            stu_obj_list = self.session.query(self.Grade).all()
            for i, stu in enumerate(stu_obj_list):
                print(i+1,'Student ID:[%s]'%stu.stu_id,'Student Name:[%s]'%stu.name)
                statue = input("please input the student's statue(yes/no)>>>")
                record_obj = self.Record(day=day, stu_id=stu.stu_id, statue=statue)
                record_obj_list.append(record_obj)
            self.session.add_all(record_obj_list)
            self.session.commit()
            print('Done!')

    def add_score(self):
        '''
        To give student's home work a score
        :return:
        '''
        while True:
            day = input('please choose a day, or q to quit>>>')
            if day == 'q':
                break
            elif not day.isdigit() or '.' in day:
                print('invalid input!')
                continue
            day = int(day)
            if len(self.session.query(self.Period).filter(self.Period.day == day).all()) == 0:
                print("The day's period not found, please add the day's period first!")
                continue
            record_obj_list = self.session.query(self.Record).filter(self.Record.day==day).filter(self.Record.score==0).all()
            if not record_obj_list:
                print('You need to add the day record first!')
                continue
            for i, item in enumerate(record_obj_list):
                print(i+1, 'Student ID:[%s] Name:[%s] Commit:[%s]'%(item.grade_info.stu_id, item.grade_info.name, item.commit))
                if item.commit == '/':
                    commit = input("The student have not commit yet, Please input the student's commit statue manually>>>")
                    item.commit = commit
                score = input("please input the student's score>>>").strip()
                if not score.isdigit():
                    print('Invalid input value!')
                    self.session.rollback()
                    continue
                item.score = float(score)

            self.session.commit()
            print('Done!')


    def add_member(self):
        '''
        To add new member into a grade.
        :return:
        '''
        grade_obj = self.session.query(self.GradesTable).filter(self.GradesTable.grade_id == self.grade_id).first()
        stu_obj_list =[]
        while True:
            stu_id = input('please input the student id or q to quit>>>').strip()
            if stu_id == 'q':
                break
            elif not stu_id.isdigit() or '.' in stu_id:
                print('Invalid student id!')
                continue
            stu_id = int(stu_id)
            if len(self.session.query(self.StudentInfo).filter(self.StudentInfo.stu_id == stu_id).all()) == 0:
                print('The student have not registered yet! Please make student registration first!')
                continue
            if len(self.session.query(self.Grade).filter(self.Grade.stu_id == stu_id).all()) != 0:
                print('The student already exist!')
                continue
            info_obj = self.session.query(self.StudentInfo).filter(self.StudentInfo.stu_id == stu_id).first()
            name = info_obj.name
            info_obj.grades.append(grade_obj)
            stu_obj = self.Grade(stu_id=stu_id, name=name)
            stu_obj_list.append(stu_obj)
            print('Student [%s] has been added to the grade! Added Student amount:[%s]'%(name, len(stu_obj_list)))
        self.session.add_all(stu_obj_list)
        self.session.commit()
        print('Done!')




