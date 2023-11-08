import ZODB, ZODB.FileStorage
import persistent
import transaction
import BTrees.OOBTree

class Course(persistent.Persistent):
    def __init__(self, id, name, credit = 3):
        self.credit = credit
        self.id = id
        self.name = name
        self.gradeScheme = [
            {"Grade": "A", "Min": 80, "Max": 100},
            {"Grade": "B", "Min": 70, "Max": 79},
            {"Grade": "C", "Min": 60, "Max": 69},
            {"Grade": "D", "Min": 50, "Max": 59},
            {"Grade": "F", "Min": 0, "Max": 49}
        ]
        
    def __str__(self):
        return "Course ID: {}, Course Name: {}, Course Credit: {}".format(self.id, self.name, self.credit)
    
    def getCredit(self):
        return self.credit
    
    def setName(self, name):
        self.name = name
    
    def scoreGrading(self, score):
        for grade in self.gradeScheme:
            if score >= grade["Min"] and score <= grade["Max"]:
                return grade["Grade"]
        return "F"
    
    def setGradeScheme(self, scheme):
        # Check for correct format
        if len(scheme) != 5:
            return False
        for grade in scheme:
            if "Grade" not in grade or "Min" not in grade or "Max" not in grade:
                return False
        # Check for overlapping
        for i in range(len(scheme)):
            for j in range(i + 1, len(scheme)):
                if scheme[i]["Min"] <= scheme[j]["Max"] and scheme[i]["Max"] >= scheme[j]["Min"]:
                    return False
        self.gradeScheme = scheme
        return True
    
    def printDetail(self):
        print(self.__str__())

class Enrollment(persistent.Persistent):
    def __init__(self, course, score, student):
        self.course = course
        self.student = student
        self.score = score
        
    def __str__(self):
        return "Course: {}, Score: {}, Grade: {}".format(self.course.name, self.score, self.course.scoreGrading(self.score))
    
    def getCourse(self):
        return self.course
    
    def getGrade(self):
        return self.course.scoreGrading(self.score)
    
    def getScore(self):
        return self.score
    
    def setScore(self, score):
        self.score = score
        
    def printDetail(self):
        print(self.__str__())
    
class Student(persistent.Persistent):
    def __init__(self, enrolls, id, name, password):
        self.enrolls = enrolls
        self.id = id
        self.name = name
        self.password = password
        
    def __str__(self):
        courses = ""
        courses += "================= Transcripts =================\n"
        courses += "Student ID: {}, Student Name: {}\n".format(self.id, self.name)
        for enroll in self.enrolls:
            courses += "Course: {}, Credit: {}, Score: {}, Grade: {}\n".format(enroll.getCourse().name, enroll.getCourse().credit, enroll.getScore(), enroll.getGrade())
        courses += "GPA: {:.3}\n".format(self.getGPA())
        courses += "==============================================="
        return courses
        
    def GradeLetterToNumber(self, grade):
        LetterToNumber = {
            "A": 4,
            "B": 3,
            "C": 2,
            "D": 1,
            "F": 0
        }
        return LetterToNumber[grade]
    
    def getGPA(self):
        totalpoint = 0
        totalcredit = 0
        
        for enroll in self.enrolls:
            totalpoint += enroll.getCourse().credit * self.GradeLetterToNumber(enroll.getGrade())
            totalcredit += enroll.getCourse().credit
        return totalpoint / totalcredit
    
    def enrollCourse(self, course):
        enrollobj = Enrollment(course, None, self)
        self.enrolls.append(enrollobj)
        return enrollobj
    
    def getEnrollment(self, course):
        for enroll in self.enrolls:
            if enroll.getCourse() == course:
                return enroll
        return None
    
    def login(self, id, password):
        if self.id == id and self.password == password:
            return True
        return False
    
    def printTranscript(self):
        print(self.__str__())
    
    def setName(self, name):
        self.name = name