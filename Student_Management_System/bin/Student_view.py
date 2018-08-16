#Downtiser
'''The entrance of student view'''
from Student_Management_System.core import student_main

if __name__ == '__main__':
    print("\033[34;1mWelcome to Downtiser's Student Management system!\033[0m")
    while True:
        student = student_main.StudentView()
        user_choice = input('Input q to quit or any other values to continue>>>')
        if user_choice == 'q':
            break
        else:
            student.run()