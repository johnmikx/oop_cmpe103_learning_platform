"""
Factory Pattern Implementation
Demonstrates object creation patterns with OOP
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging

# Import user models
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inheritance.user_models import Student, Teacher, Admin, GraduateStudent, Professor
from abstraction.notification_service import EmailNotificationService, SMSNotificationService, PushNotificationService

class UserFactory:
    """
    FACTORY PATTERN for creating different user types
    
    Demonstrates how to create objects without specifying exact classes
    Encapsulates object creation logic
    """
    
    # ⬅️ FACTORY PATTERN: Registry of user types
    _user_types = {
        'student': Student,
        'graduate_student': GraduateStudent,
        'teacher': Teacher,
        'professor': Professor,
        'admin': Admin
    }
    
    @classmethod
    def create_user(cls, user_type: str, username: str, email: str, full_name: str, extra: str) -> Any:
        """
        Factory method to create users based on type
        
        ⬅️ FACTORY PATTERN: Single method to create different object types
        Hides the complexity of object creation from client code
        """
        if user_type not in cls._user_types:
            raise ValueError(f"Unknown user type: {user_type}")
        
        user_class = cls._user_types[user_type]
        
        try:
            # Create user with appropriate parameters based on type
            if user_type in ['student', 'graduate_student']:
                # Students need course/research area
                user = user_class(username, email, full_name, extra)
            elif user_type in ['teacher', 'professor']:
                # Teachers need department
                user = user_class(username, email, full_name, extra)
            elif user_type == 'admin':
                # Admins need access level
                user = user_class(username, email, full_name, extra)
            else:
                # Fallback
                user = user_class(username, email, full_name, extra)
            
            logging.info(f"Created {user_type}: {full_name}")
            return user
            
        except Exception as e:
            logging.error(f"Failed to create user {username}: {e}")
            raise
    
    @classmethod
    def get_available_types(cls) -> list:
        """Get list of available user types"""
        return list(cls._user_types.keys())
    
    @classmethod
    def register_user_type(cls, type_name: str, user_class: type) -> None:
        """
        ⬅️ FACTORY PATTERN: Dynamic registration of new user types
        Allows extending the factory without modifying existing code
        """
        cls._user_types[type_name] = user_class
        logging.info(f"Registered new user type: {type_name}")

class NotificationFactory:
    """
    FACTORY PATTERN for creating different notification services
    
    Demonstrates polymorphic object creation
    """
    
    # ⬅️ FACTORY PATTERN: Registry of notification types
    _notification_types = {
        'email': EmailNotificationService,
        'sms': SMSNotificationService,
        'push': PushNotificationService
    }
    
    @classmethod
    def create_notification_service(cls, service_type: str, config: Optional[Dict] = None) -> Any:
        """
        Factory method to create notification services
        
        ⬅️ FACTORY PATTERN: Creates different notification services
        All returned objects implement the same interface (polymorphism)
        """
        if service_type not in cls._notification_types:
            raise ValueError(f"Unknown notification service: {service_type}")
        
        service_class = cls._notification_types[service_type]
        
        try:
            if config:
                service = service_class(config)
            else:
                service = service_class()
            
            logging.info(f"Created notification service: {service_type}")
            return service
            
        except Exception as e:
            logging.error(f"Failed to create notification service {service_type}: {e}")
            raise
    
    @classmethod
    def create_multi_channel_service(cls, channels: list) -> 'MultiChannelNotificationService':
        """
        ⬅️ FACTORY PATTERN: Creates composite notification service
        Demonstrates creating complex objects using the factory
        """
        services = []
        for channel in channels:
            service = cls.create_notification_service(channel)
            services.append(service)
        
        return MultiChannelNotificationService(services)
    
    @classmethod
    def get_available_services(cls) -> list:
        """Get list of available notification services"""
        return list(cls._notification_types.keys())

class MultiChannelNotificationService:
    """
    Composite notification service that uses multiple channels
    Demonstrates composition with factory-created objects
    """
    
    def __init__(self, services: list):
        self._services = services
    
    def send_notification(self, recipient: str, message: str, subject: str = None) -> Dict:
        """Send notification through all channels"""
        results = {}
        
        for service in self._services:
            try:
                service_name = type(service).__name__
                result = service.send_notification(recipient, message, subject)
                results[service_name] = result
            except Exception as e:
                results[service_name] = {'success': False, 'error': str(e)}
        
        return results

class AbstractFactory(ABC):
    """
    ABSTRACT FACTORY PATTERN
    
    Demonstrates creating families of related objects
    """
    
    @abstractmethod
    def create_user_service(self) -> Any:
        """Create user management service"""
        pass
    
    @abstractmethod
    def create_notification_service(self) -> Any:
        """Create notification service"""
        pass
    
    @abstractmethod
    def create_payment_service(self) -> Any:
        """Create payment service"""
        pass

class StudentSystemFactory(AbstractFactory):
    """
    Concrete factory for student management system
    
    ⬅️ ABSTRACT FACTORY: Creates family of related objects for students
    """
    
    def create_user_service(self):
        from abstraction.data_service import StudentDataService
        return StudentDataService()
    
    def create_notification_service(self):
        return NotificationFactory.create_notification_service('email')
    
    def create_payment_service(self):
        from polymorphism.payment_processors import CreditCardProcessor
        return CreditCardProcessor()

class TeacherSystemFactory(AbstractFactory):
    """
    Concrete factory for teacher management system
    
    ⬅️ ABSTRACT FACTORY: Creates family of related objects for teachers
    """
    
    def create_user_service(self):
        from abstraction.data_service import TeacherDataService
        return TeacherDataService()
    
    def create_notification_service(self):
        return NotificationFactory.create_multi_channel_service(['email', 'sms'])
    
    def create_payment_service(self):
        from polymorphism.payment_processors import BankTransferProcessor
        return BankTransferProcessor()

# Example usage demonstrating factory patterns
if __name__ == "__main__":
    print("=== FACTORY PATTERN DEMONSTRATION ===\n")
    
    # ⬅️ FACTORY PATTERN: Creating different user types
    print("1. User Factory:")
    try:
        student = UserFactory.create_user('student', 'john_doe', 'john@email.com', 'John Doe', 'Computer Science')
        teacher = UserFactory.create_user('teacher', 'prof_smith', 'smith@email.com', 'Dr. Smith', 'Mathematics')
        
        print(f"Created: {student.get_name()} ({student.get_role()})")
        print(f"Created: {teacher.get_name()} ({teacher.get_role()})")
    except Exception as e:
        print(f"Error: {e}")
    
    print(f"Available user types: {UserFactory.get_available_types()}\n")
    
    # ⬅️ FACTORY PATTERN: Creating notification services
    print("2. Notification Factory:")
    try:
        email_service = NotificationFactory.create_notification_service('email')
        multi_service = NotificationFactory.create_multi_channel_service(['email', 'sms'])
        
        print(f"Created email service: {type(email_service).__name__}")
        print(f"Created multi-channel service with {len(multi_service._services)} channels")
    except Exception as e:
        print(f"Error: {e}")
    
    print(f"Available services: {NotificationFactory.get_available_services()}\n")
    
    # ⬅️ ABSTRACT FACTORY: Creating system components
    print("3. Abstract Factory:")
    student_factory = StudentSystemFactory()
    teacher_factory = TeacherSystemFactory()
    
    student_system = {
        'user_service': student_factory.create_user_service(),
        'notification_service': student_factory.create_notification_service(),
        'payment_service': student_factory.create_payment_service()
    }
    
    print("Student system components created:")
    for component, service in student_system.items():
        print(f"  {component}: {type(service).__name__}")
