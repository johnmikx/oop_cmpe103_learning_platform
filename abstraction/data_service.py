"""
Abstraction Example: Data Service Classes
Demonstrates abstract base classes and hiding implementation complexity
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Any

class DataService(ABC):
    """
    Demonstrates ABSTRACTION - the second pillar of OOP
    
    Abstract base class that defines the interface for data services
    Hides implementation details and provides a common contract
    """
    
    def __init__(self):
        # ⬅️ ABSTRACTION: Internal data structure hidden from users
        self._data_store: List[Any] = []
    
    # ⬅️ ABSTRACTION: Abstract methods define interface without implementation
    @abstractmethod
    def add_user(self, user: Any) -> bool:
        """Abstract method - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def get_user_by_username(self, username: str) -> Optional[Any]:
        """Abstract method - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def validate_user_data(self, user: Any) -> bool:
        """Abstract method - each service validates differently"""
        pass
    
    # ⬅️ ABSTRACTION: Concrete methods that use abstract methods
    def get_user_count(self) -> int:
        """Concrete method available to all subclasses"""
        return len(self._data_store)
    
    def get_all_users(self) -> List[Any]:
        """Concrete method that returns copy of data (abstraction of internal storage)"""
        return self._data_store.copy()
    
    def remove_user(self, username: str) -> bool:
        """
        Concrete method that uses abstract method internally
        Demonstrates how abstraction builds on abstract methods
        """
        user = self.get_user_by_username(username)
        if user:
            self._data_store.remove(user)
            return True
        return False

class StudentDataService(DataService):
    """
    Concrete implementation of DataService for Students
    Demonstrates ABSTRACTION by implementing abstract methods with specific logic
    """
    
    def __init__(self):
        super().__init__()
        # ⬅️ ABSTRACTION: Additional internal state hidden from users
        self._student_courses = {}
    
    # ⬅️ ABSTRACTION: Implementing abstract method with student-specific logic
    def add_user(self, student) -> bool:
        """Student-specific implementation of add_user"""
        if not self.validate_user_data(student):
            return False
        
        # Check for duplicate usernames
        if self.get_user_by_username(student.get_username()):
            return False
        
        self._data_store.append(student)
        # ⬅️ ABSTRACTION: Internal tracking of student courses (hidden complexity)
        self._student_courses[student.get_username()] = student.get_course()
        return True
    
    # ⬅️ ABSTRACTION: Student-specific implementation
    def get_user_by_username(self, username: str):
        """Find student by username - hides search implementation"""
        for student in self._data_store:
            if student.get_username() == username:
                return student
        return None
    
    # ⬅️ ABSTRACTION: Student-specific validation logic
    def validate_user_data(self, student) -> bool:
        """Validate student data - hides validation complexity"""
        try:
            # Check required attributes exist
            return (hasattr(student, '_username') and 
                   hasattr(student, '_email') and 
                   hasattr(student, '_course') and
                   student.get_username() and 
                   student.get_email() and
                   '@' in student.get_email())
        except:
            return False
    
    # ⬅️ ABSTRACTION: Additional method specific to student service
    def get_students_by_course(self, course: str) -> List:
        """Student-specific method - abstracts course filtering logic"""
        return [student for student in self._data_store 
                if hasattr(student, '_course') and student.get_course() == course]

class TeacherDataService(DataService):
    """
    Different concrete implementation of DataService for Teachers
    Demonstrates ABSTRACTION with different internal logic but same interface
    """
    
    def __init__(self):
        super().__init__()
        # ⬅️ ABSTRACTION: Different internal state for teachers
        self._teacher_departments = {}
    
    # ⬅️ ABSTRACTION: Teacher-specific implementation of same abstract method
    def add_user(self, teacher) -> bool:
        """Teacher-specific implementation with different validation"""
        if not self.validate_user_data(teacher):
            return False
        
        if self.get_user_by_username(teacher.get_username()):
            return False
        
        self._data_store.append(teacher)
        # ⬅️ ABSTRACTION: Different internal tracking for teachers
        self._teacher_departments[teacher.get_username()] = teacher.get_department()
        return True
    
    def get_user_by_username(self, username: str):
        """Teacher-specific search implementation"""
        for teacher in self._data_store:
            if teacher.get_username() == username:
                return teacher
        return None
    
    # ⬅️ ABSTRACTION: Different validation rules for teachers
    def validate_user_data(self, teacher) -> bool:
        """Teacher-specific validation - different rules than students"""
        try:
            return (hasattr(teacher, '_username') and 
                   hasattr(teacher, '_email') and 
                   hasattr(teacher, '_department') and
                   teacher.get_username() and 
                   teacher.get_email() and
                   '@' in teacher.get_email() and
                   teacher.get_department())
        except:
            return False
    
    # ⬅️ ABSTRACTION: Teacher-specific method
    def get_teachers_by_department(self, department: str) -> List:
        """Teacher-specific method - abstracts department filtering"""
        return [teacher for teacher in self._data_store 
                if hasattr(teacher, '_department') and teacher.get_department() == department]

# Example usage demonstrating abstraction
if __name__ == "__main__":
    # ⬅️ ABSTRACTION: Users work with the same interface regardless of implementation
    
    # Both services provide the same interface but different implementations
    student_service = StudentDataService()
    teacher_service = TeacherDataService()
    
    # Same method calls work on both services (abstraction in action)
    print(f"Student count: {student_service.get_user_count()}")
    print(f"Teacher count: {teacher_service.get_user_count()}")
    
    # Implementation details are hidden - users don't need to know how data is stored
