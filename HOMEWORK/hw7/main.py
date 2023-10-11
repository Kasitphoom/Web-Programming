import ZODB, ZODB.FileStorage
import persistent
import transaction
import BTrees.OOBTree
from class_module import *

storage = ZODB.FileStorage.FileStorage('mydata.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root

root.courses = BTrees.OOBTree.BTree()
root.courses[101] = Course(101, "Computer Programming", 4)
root.courses[201] = Course(201, "Web Programming", 4)
root.courses[202] = Course(202, "Software Engineering Principles", 5)
root.courses[301] = Course(301, "Artificial Intelligent", 3)

root.students = BTrees.OOBTree.BTree()
root.students[1101] = Student([], 1101, "Mr. For Example")
root.students[1101].enrolls = [Enrollment(root.courses[101], 75.0, root.students[1101]), Enrollment(root.courses[201], 81.0, root.students[1101]), Enrollment(root.courses[202], 81.0, root.students[1101]),Enrollment(root.courses[301], 57.0, root.students[1101])]

newGradingScheme = [
    {"Grade": "A", "Min": 85, "Max": 100},
    {"Grade": "B", "Min": 75, "Max": 84},
    {"Grade": "C", "Min": 55, "Max": 74},
    {"Grade": "D", "Min": 50, "Max": 54},
    {"Grade": "F", "Min": 0, "Max": 49}
]

if root.students[1101].enrolls[2].course.setGradeScheme(newGradingScheme):
    print("Success")
else:
    print("Fail")
    
if root.students[1101].enrolls[3].course.setGradeScheme(newGradingScheme):
    print("Success")
else:
    print("Fail")

transaction.commit()
db.close()