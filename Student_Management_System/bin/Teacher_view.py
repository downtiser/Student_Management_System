#Downtiser
'''The entrance of the teacher view'''
from Student_Management_System.core import teacher_main

if __name__ == '__main__':
    print("\033[34;1mWelcome to Downtiser's Student Management system!\033[0m")
    while True:
        teacher = teacher_main.TeacherView()
        user_choice = input('Input q to quit or any other values to continue>>>')
        if user_choice == 'q':
            break
        else:
            teacher.run()