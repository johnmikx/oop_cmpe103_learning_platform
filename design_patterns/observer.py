"""
Observer Pattern Implementation
Demonstrates event notification and loose coupling
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime
import logging

class Observer(ABC):
    """
    OBSERVER PATTERN: Abstract observer interface
    
    Defines the interface that all observers must implement
    """
    
    @abstractmethod
    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        """Called when the subject notifies observers of changes"""
        pass

class Subject(ABC):
    """
    OBSERVER PATTERN: Abstract subject interface
    
    Defines the interface for objects that can be observed
    """
    
    def __init__(self):
        self._observers: List[Observer] = []
    
    def subscribe(self, observer: Observer) -> None:
        """Add an observer to the notification list"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def unsubscribe(self, observer: Observer) -> None:
        """Remove an observer from the notification list"""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, event_type: str, data: Dict[str, Any]) -> None:
        """Notify all observers of an event"""
        for observer in self._observers:
            try:
                observer.update(event_type, data)
            except Exception as e:
                logging.error(f"Error notifying observer: {e}")

class GradeNotificationSystem(Subject):
    """
    OBSERVER PATTERN: Concrete subject for grade notifications
    
    Manages grade-related events and notifies interested parties
    """
    
    def __init__(self):
        super().__init__()
        self._grade_history: List[Dict] = []
        self._notification_queue: List[Dict] = []
        self.logger = logging.getLogger(__name__)
    
    def notify_grade_assigned(self, student_username: str, subject: str, grade: float, final_grade: float) -> None:
        """
        ⬅️ OBSERVER PATTERN: Notify observers when a grade is assigned
        Demonstrates how subjects notify observers of state changes
        """
        event_data = {
            'student_username': student_username,
            'subject': subject,
            'grade': grade,
            'final_grade': final_grade,
            'timestamp': datetime.now().isoformat(),
            'event_id': len(self._grade_history) + 1
        }
        
        # Store in history
        self._grade_history.append(event_data)
        
        # Add to notification queue
        self._notification_queue.append(event_data)
        
        # Notify all observers
        self.notify('grade_assigned', event_data)
        
        self.logger.info(f"Grade assigned notification sent: {student_username} - {subject}: {grade}")
    
    def notify_grade_updated(self, student_username: str, subject: str, old_grade: float, new_grade: float) -> None:
        """Notify observers when a grade is updated"""
        event_data = {
            'student_username': student_username,
            'subject': subject,
            'old_grade': old_grade,
            'new_grade': new_grade,
            'timestamp': datetime.now().isoformat(),
            'event_id': len(self._grade_history) + 1
        }
        
        self._grade_history.append(event_data)
        self._notification_queue.append(event_data)
        
        self.notify('grade_updated', event_data)
        
        self.logger.info(f"Grade update notification sent: {student_username} - {subject}: {old_grade} -> {new_grade}")
    
    def get_subscriber_count(self) -> int:
        """Get the number of active subscribers"""
        return len(self._observers)
    
    def get_queue_size(self) -> int:
        """Get the size of the notification queue"""
        return len(self._notification_queue)
    
    def process_notification_queue(self) -> List[Dict]:
        """Process and clear the notification queue"""
        processed = self._notification_queue.copy()
        self._notification_queue.clear()
        return processed
    
    def get_grade_history(self, limit: int = 10) -> List[Dict]:
        """Get recent grade history"""
        return self._grade_history[-limit:] if self._grade_history else []

class StudentGradeObserver(Observer):
    """
    OBSERVER PATTERN: Concrete observer for students
    
    Students receive notifications about their own grades
    """
    
    def __init__(self, student_username: str):
        self.student_username = student_username
        self.received_notifications: List[Dict] = []
        self.logger = logging.getLogger(__name__)
    
    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        """
        ⬅️ OBSERVER PATTERN: Handle notifications from the subject
        Only processes notifications relevant to this student
        """
        if data.get('student_username') == self.student_username:
            notification = {
                'event_type': event_type,
                'data': data,
                'received_at': datetime.now().isoformat()
            }
            
            self.received_notifications.append(notification)
            
            # Process the notification
            if event_type == 'grade_assigned':
                self._handle_grade_assigned(data)
            elif event_type == 'grade_updated':
                self._handle_grade_updated(data)
            
            self.logger.info(f"Student {self.student_username} received {event_type} notification")
    
    def _handle_grade_assigned(self, data: Dict[str, Any]) -> None:
        """Handle new grade assignment"""
        subject = data['subject']
        grade = data['grade']
        print(f"📧 {self.student_username}: New grade in {subject}: {grade}")
    
    def _handle_grade_updated(self, data: Dict[str, Any]) -> None:
        """Handle grade update"""
        subject = data['subject']
        old_grade = data['old_grade']
        new_grade = data['new_grade']
        print(f"📧 {self.student_username}: Grade updated in {subject}: {old_grade} → {new_grade}")
    
    def get_notifications(self) -> List[Dict]:
        """Get all received notifications"""
        return self.received_notifications.copy()

class TeacherGradeObserver(Observer):
    """
    OBSERVER PATTERN: Concrete observer for teachers
    
    Teachers receive notifications about all grade activities
    """
    
    def __init__(self, teacher_username: str):
        self.teacher_username = teacher_username
        self.grade_statistics: Dict[str, int] = {'assigned': 0, 'updated': 0}
        self.recent_activities: List[Dict] = []
        self.logger = logging.getLogger(__name__)
    
    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        """
        ⬅️ OBSERVER PATTERN: Handle all grade notifications
        Teachers see all grade activities for monitoring
        """
        activity = {
            'event_type': event_type,
            'data': data,
            'processed_at': datetime.now().isoformat()
        }
        
        self.recent_activities.append(activity)
        
        # Update statistics
        if event_type == 'grade_assigned':
            self.grade_statistics['assigned'] += 1
            self._handle_grade_assigned(data)
        elif event_type == 'grade_updated':
            self.grade_statistics['updated'] += 1
            self._handle_grade_updated(data)
        
        # Keep only recent activities (last 50)
        if len(self.recent_activities) > 50:
            self.recent_activities = self.recent_activities[-50:]
        
        self.logger.info(f"Teacher {self.teacher_username} processed {event_type} notification")
    
    def _handle_grade_assigned(self, data: Dict[str, Any]) -> None:
        """Handle grade assignment notification"""
        student = data['student_username']
        subject = data['subject']
        grade = data['grade']
        print(f"👨‍🏫 {self.teacher_username}: Grade assigned to {student} in {subject}: {grade}")
    
    def _handle_grade_updated(self, data: Dict[str, Any]) -> None:
        """Handle grade update notification"""
        student = data['student_username']
        subject = data['subject']
        old_grade = data['old_grade']
        new_grade = data['new_grade']
        print(f"👨‍🏫 {self.teacher_username}: Grade updated for {student} in {subject}: {old_grade} → {new_grade}")
    
    def get_statistics(self) -> Dict[str, int]:
        """Get grade activity statistics"""
        return self.grade_statistics.copy()
    
    def get_recent_activities(self, limit: int = 10) -> List[Dict]:
        """Get recent grade activities"""
        return self.recent_activities[-limit:] if self.recent_activities else []

class AdminGradeObserver(Observer):
    """
    OBSERVER PATTERN: Concrete observer for administrators
    
    Administrators receive comprehensive notifications and maintain system metrics
    """
    
    def __init__(self, admin_username: str):
        self.admin_username = admin_username
        self.system_metrics: Dict[str, Any] = {
            'total_grades_assigned': 0,
            'total_grades_updated': 0,
            'active_students': set(),
            'active_subjects': set(),
            'daily_activity': {}
        }
        self.alerts: List[Dict] = []
        self.logger = logging.getLogger(__name__)
    
    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        """
        ⬅️ OBSERVER PATTERN: Handle all notifications for system monitoring
        Administrators track system-wide metrics and generate alerts
        """
        # Update metrics
        if event_type == 'grade_assigned':
            self.system_metrics['total_grades_assigned'] += 1
            self._update_daily_activity(data['timestamp'])
        elif event_type == 'grade_updated':
            self.system_metrics['total_grades_updated'] += 1
        
        # Track active entities
        self.system_metrics['active_students'].add(data['student_username'])
        self.system_metrics['active_subjects'].add(data['subject'])
        
        # Check for alerts
        self._check_for_alerts(event_type, data)
        
        self.logger.info(f"Admin {self.admin_username} updated system metrics for {event_type}")
    
    def _update_daily_activity(self, timestamp: str) -> None:
        """Update daily activity metrics"""
        date = timestamp.split('T')[0]  # Extract date part
        if date not in self.system_metrics['daily_activity']:
            self.system_metrics['daily_activity'][date] = 0
        self.system_metrics['daily_activity'][date] += 1
    
    def _check_for_alerts(self, event_type: str, data: Dict[str, Any]) -> None:
        """Check for system alerts"""
        # Example: Alert if too many grade updates for one student
        if event_type == 'grade_updated':
            student = data['student_username']
            recent_updates = sum(1 for alert in self.alerts 
                               if alert.get('student_username') == student 
                               and alert.get('event_type') == 'grade_updated')
            
            if recent_updates >= 3:  # Threshold for alert
                alert = {
                    'type': 'excessive_grade_updates',
                    'student_username': student,
                    'subject': data['subject'],
                    'timestamp': datetime.now().isoformat(),
                    'message': f"Student {student} has had multiple grade updates"
                }
                self.alerts.append(alert)
                print(f"🚨 ALERT: {alert['message']}")
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get comprehensive system metrics"""
        metrics = self.system_metrics.copy()
        metrics['active_students'] = len(metrics['active_students'])
        metrics['active_subjects'] = len(metrics['active_subjects'])
        return metrics
    
    def get_alerts(self) -> List[Dict]:
        """Get system alerts"""
        return self.alerts.copy()

# Example usage demonstrating observer pattern
if __name__ == "__main__":
    print("=== OBSERVER PATTERN DEMONSTRATION ===\n")
    
    # ⬅️ OBSERVER PATTERN: Create the subject (notification system)
    grade_system = GradeNotificationSystem()
    
    # ⬅️ OBSERVER PATTERN: Create different types of observers
    student_observer = StudentGradeObserver('john_doe')
    teacher_observer = TeacherGradeObserver('prof_smith')
    admin_observer = AdminGradeObserver('admin')
    
    # ⬅️ OBSERVER PATTERN: Subscribe observers to the subject
    grade_system.subscribe(student_observer)
    grade_system.subscribe(teacher_observer)
    grade_system.subscribe(admin_observer)
    
    print(f"Subscribers: {grade_system.get_subscriber_count()}\n")
    
    # ⬅️ OBSERVER PATTERN: Trigger events that notify all observers
    print("1. Assigning grades:")
    grade_system.notify_grade_assigned('john_doe', 'Mathematics', 85.0, 85.0)
    grade_system.notify_grade_assigned('john_doe', 'Physics', 92.0, 92.0)
    
    print("\n2. Updating grades:")
    grade_system.notify_grade_updated('john_doe', 'Mathematics', 85.0, 88.0)
    
    print(f"\n3. System Statistics:")
    print(f"Student notifications: {len(student_observer.get_notifications())}")
    print(f"Teacher statistics: {teacher_observer.get_statistics()}")
    print(f"Admin metrics: {admin_observer.get_system_metrics()}")
    print(f"Admin alerts: {len(admin_observer.get_alerts())}")
