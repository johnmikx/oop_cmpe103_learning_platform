"""
Inheritance Example: User Model Classes
Demonstrates base classes, inheritance, and method overriding
"""

from typing import Optional
from datetime import datetime

class BaseUser:
    """
    Demonstrates INHERITANCE - the third pillar of OOP
    
    Base class that defines common attributes and methods for all users
    Child classes inherit and extend this functionality
    """
    
    def __init__(self, username: str, email: str, full_name: str):
        # ⬅️ INHERITANCE: Protected attributes (accessible to child classes)
        self._username = username
        self._email = email
        self._full_name = full_name
        self._created_at = datetime.now()
        self._is_active = True
        self._login_count = 0
    
    # ⬅️ INHERITANCE: Base methods that all child classes inherit
    def get_username(self) -> str:
        """Common method inherited by all user types"""
        return self._username
    
    def get_email(self) -> str:
        """Common method inherited by all user types"""
        return self._email
    
    def get_name(self) -> str:
        """Common method inherited by all user types"""
        return self._full_name
    
    def get_created_at(self) -> datetime:
        """Common method inherited by all user types"""
        return self._created_at
    
    def login(self) -> bool:
        """Common login functionality for all users"""
        if self._is_active:
            self._login_count += 1
            return True
        return False
    
    def deactivate(self) -> None:
        """Common deactivation functionality"""
        self._is_active = False
    
    # ⬅️ INHERITANCE: Virtual method to be overridden by child classes
    def get_role(self) -> str:
        """Base implementation - child classes should override this"""
        return "User"
    
    def get_user_details(self) -> str:
        """Base implementation - child classes can override for specific details"""
        return f"User: {self._full_name} ({self._username})"
    
    def __str__(self) -> str:
        """String representation for all user types"""
        return f"{self.get_role()}: {self._full_name}"

class Student(BaseUser):
    """
    Demonstrates INHERITANCE by extending BaseUser
    Inherits all base functionality and adds student-specific features
    """
    
    def __init__(self, username: str, email: str, full_name: str, course: str):
        # ⬅️ INHERITANCE: Call parent constructor
        super().__init__(username, email, full_name)
        
        # ⬅️ INHERITANCE: Add student-specific attributes
        self._course = course
        self._grades = {}
        self._assignments = []
        self._gpa = 0.0
        self._bank_account = None  # For encapsulation demo
    
    # ⬅️ INHERITANCE: Override parent method with student-specific implementation
    def get_role(self) -> str:
        """Override base method - polymorphism in action"""
        return "Student"
    
    def get_user_details(self) -> str:
        """Override base method with student-specific details"""
        return f"Student: {self._full_name} - Course: {self._course} (GPA: {self._gpa})"
    
    # ⬅️ INHERITANCE: Student-specific methods (extending base functionality)
    def get_course(self) -> str:
        """Student-specific method"""
        return self._course
    
    def add_grade(self, subject: str, grade: float) -> None:
        """Student-specific functionality"""
        self._grades[subject] = grade
        self._calculate_gpa()
    
    def get_grades(self) -> dict:
        """Student-specific functionality"""
        return self._grades.copy()
    
    def get_gpa(self) -> float:
        """Student-specific functionality"""
        return self._gpa
    
    def set_bank_account(self, bank_account) -> None:
        """Link to bank account for encapsulation demo"""
        self._bank_account = bank_account
    
    def _calculate_gpa(self) -> None:
        """Private method to calculate GPA"""
        if self._grades:
            self._gpa = sum(self._grades.values()) / len(self._grades)

class Teacher(BaseUser):
    """
    Another INHERITANCE example - different specialization of BaseUser
    Shows how different child classes can extend the same base class differently
    """
    
    def __init__(self, username: str, email: str, full_name: str, department: str):
        # ⬅️ INHERITANCE: Call parent constructor
        super().__init__(username, email, full_name)
        
        # ⬅️ INHERITANCE: Add teacher-specific attributes
        self._department = department
        self._courses_taught = []
        self._students = []
        self._salary = 0.0
    
    # ⬅️ INHERITANCE: Override parent method with teacher-specific implementation
    def get_role(self) -> str:
        """Override base method - different implementation than Student"""
        return "Teacher"
    
    def get_user_details(self) -> str:
        """Override base method with teacher-specific details"""
        courses_count = len(self._courses_taught)
        return f"Teacher: {self._full_name} - Dept: {self._department} ({courses_count} courses)"
    
    # ⬅️ INHERITANCE: Teacher-specific methods
    def get_department(self) -> str:
        """Teacher-specific method"""
        return self._department
    
    def add_course(self, course: str) -> None:
        """Teacher-specific functionality"""
        if course not in self._courses_taught:
            self._courses_taught.append(course)
    
    def get_courses(self) -> list:
        """Teacher-specific functionality"""
        return self._courses_taught.copy()
    
    def assign_grade(self, student_username: str, subject: str, grade: float) -> bool:
        """Teacher-specific functionality - grading students"""
        # In a real app, this would interact with student objects
        print(f"Teacher {self._full_name} assigned grade {grade} to {student_username} in {subject}")
        return True

class Admin(BaseUser):
    """
    Third INHERITANCE example - administrative user with elevated privileges
    Demonstrates how inheritance can create specialized user types
    """
    
    def __init__(self, username: str, email: str, full_name: str, access_level: str):
        # ⬅️ INHERITANCE: Call parent constructor
        super().__init__(username, email, full_name)
        
        # ⬅️ INHERITANCE: Add admin-specific attributes
        self._access_level = access_level
        self._permissions = ["read", "write", "delete", "manage_users"]
        self._managed_systems = []
    
    # ⬅️ INHERITANCE: Override parent method with admin-specific implementation
    def get_role(self) -> str:
        """Override base method - admin-specific implementation"""
        return "Administrator"
    
    def get_user_details(self) -> str:
        """Override base method with admin-specific details"""
        return f"Admin: {self._full_name} - Access Level: {self._access_level}"
    
    # ⬅️ INHERITANCE: Admin-specific methods
    def get_access_level(self) -> str:
        """Admin-specific method"""
        return self._access_level
    
    def has_permission(self, permission: str) -> bool:
        """Admin-specific functionality"""
        return permission in self._permissions
    
    def manage_user(self, user: BaseUser, action: str) -> bool:
        """
        Admin-specific functionality - can manage any user type
        Demonstrates inheritance - accepts any BaseUser or its children
        """
        if not self.has_permission("manage_users"):
            return False
        
        if action == "deactivate":
            user.deactivate()
            print(f"Admin {self._full_name} deactivated user {user.get_username()}")
            return True
        
        return False

# Example usage demonstrating inheritance
if __name__ == "__main__":
    # ⬅️ INHERITANCE: Create instances of different user types
    student = Student("john_doe", "john@email.com", "John Doe", "Computer Science")
    teacher = Teacher("prof_smith", "smith@email.com", "Dr. Smith", "Mathematics")
    admin = Admin("admin", "admin@email.com", "System Admin", "super")
    
    # ⬅️ INHERITANCE: All objects share common interface from BaseUser
    users = [student, teacher, admin]
    
    for user in users:
        print(f"Username: {user.get_username()}")  # Inherited method
        print(f"Role: {user.get_role()}")          # Overridden method
        print(f"Details: {user.get_user_details()}")  # Overridden method
        print(f"Login successful: {user.login()}")    # Inherited method
        print("---")
    
    # ⬅️ INHERITANCE: Child-specific methods
    student.add_grade("Math", 85.0)
    teacher.add_course("Calculus 101")
    admin.manage_user(student, "deactivate")
