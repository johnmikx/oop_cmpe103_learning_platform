"""
Enhanced Encapsulation: Security Manager
Demonstrates advanced encapsulation with security features
"""

import hashlib
import secrets
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

class SecurityManager:
    """
    Advanced ENCAPSULATION example with security features
    
    Private attributes for security data:
    - __login_attempts (private)
    - __security_logs (private)
    - __session_tokens (private)
    - __rate_limits (private)
    """
    
    def __init__(self):
        # ⬅️ ENCAPSULATION: Private security data
        self.__login_attempts: Dict[str, List[datetime]] = {}
        self.__security_logs: List[Dict] = []
        self.__session_tokens: Dict[str, Dict] = {}
        self.__rate_limits: Dict[str, List[float]] = {}
        self.__security_config = {
            'max_login_attempts': 5,
            'lockout_duration': 300,  # 5 minutes
            'rate_limit_window': 60,  # 1 minute
            'max_requests_per_window': 100
        }
        self.__incident_count = 0
        
        self.logger = logging.getLogger(__name__)
    
    # ⬅️ ENCAPSULATION: Controlled access to security validation
    def validate_login_attempt(self, username: str, ip_address: str) -> bool:
        """
        Public method to validate login attempts
        Hides internal security logic and rate limiting
        """
        current_time = datetime.now()
        
        # Check if user is locked out
        if self.__is_user_locked_out(username):
            self.__log_security_event('login_blocked', username, ip_address, 'User locked out')
            return False
        
        # Check rate limiting
        if not self.__check_rate_limit(ip_address):
            self.__log_security_event('rate_limit_exceeded', username, ip_address, 'Too many requests')
            return False
        
        return True
    
    # ⬅️ ENCAPSULATION: Private method for internal security logic
    def __is_user_locked_out(self, username: str) -> bool:
        """Private method - internal security implementation"""
        if username not in self.__login_attempts:
            return False
        
        recent_attempts = self.__get_recent_attempts(username)
        max_attempts = self.__security_config['max_login_attempts']
        
        if len(recent_attempts) >= max_attempts:
            last_attempt = recent_attempts[-1]
            lockout_duration = timedelta(seconds=self.__security_config['lockout_duration'])
            
            if datetime.now() - last_attempt < lockout_duration:
                return True
        
        return False
    
    def __get_recent_attempts(self, username: str) -> List[datetime]:
        """Private method to get recent login attempts"""
        if username not in self.__login_attempts:
            return []
        
        cutoff_time = datetime.now() - timedelta(seconds=self.__security_config['lockout_duration'])
        return [attempt for attempt in self.__login_attempts[username] if attempt > cutoff_time]
    
    def __check_rate_limit(self, ip_address: str) -> bool:
        """Private method for rate limiting logic"""
        current_time = time.time()
        window_size = self.__security_config['rate_limit_window']
        max_requests = self.__security_config['max_requests_per_window']
        
        if ip_address not in self.__rate_limits:
            self.__rate_limits[ip_address] = []
        
        # Remove old requests outside the window
        self.__rate_limits[ip_address] = [
            req_time for req_time in self.__rate_limits[ip_address]
            if current_time - req_time < window_size
        ]
        
        # Check if under limit
        if len(self.__rate_limits[ip_address]) >= max_requests:
            return False
        
        # Add current request
        self.__rate_limits[ip_address].append(current_time)
        return True
    
    # ⬅️ ENCAPSULATION: Public interface for password operations
    def hash_password(self, password: str) -> str:
        """Public method for password hashing - hides implementation"""
        salt = secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return f"{salt}:{password_hash.hex()}"
    
    def verify_password(self, password: str, stored_hash: str) -> bool:
        """Public method for password verification"""
        try:
            salt, hash_hex = stored_hash.split(':')
            password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
            return password_hash.hex() == hash_hex
        except:
            return False
    
    # ⬅️ ENCAPSULATION: Controlled logging interface
    def log_login_success(self, username: str, ip_address: str) -> None:
        """Public method to log successful login"""
        self.__clear_login_attempts(username)
        self.__log_security_event('login_success', username, ip_address, 'Successful login')
    
    def log_login_failure(self, username: str, ip_address: str) -> None:
        """Public method to log failed login"""
        self.__record_login_attempt(username)
        self.__log_security_event('login_failure', username, ip_address, 'Failed login attempt')
        self.__incident_count += 1
    
    def log_logout(self, username: str, ip_address: str) -> None:
        """Public method to log logout"""
        self.__log_security_event('logout', username, ip_address, 'User logout')
    
    def __record_login_attempt(self, username: str) -> None:
        """Private method to record login attempt"""
        if username not in self.__login_attempts:
            self.__login_attempts[username] = []
        
        self.__login_attempts[username].append(datetime.now())
    
    def __clear_login_attempts(self, username: str) -> None:
        """Private method to clear login attempts after success"""
        if username in self.__login_attempts:
            del self.__login_attempts[username]
    
    def __log_security_event(self, event_type: str, username: str, ip_address: str, details: str) -> None:
        """Private method for internal security logging"""
        event = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'username': username,
            'ip_address': ip_address,
            'details': details
        }
        self.__security_logs.append(event)
        self.logger.info(f"Security event: {event}")
    
    # ⬅️ ENCAPSULATION: Public interface for security status
    def get_security_status(self) -> Dict:
        """Public method to get security status without exposing internal data"""
        return {
            'total_events': len(self.__security_logs),
            'incident_count': self.__incident_count,
            'active_lockouts': len([u for u in self.__login_attempts.keys() if self.__is_user_locked_out(u)]),
            'rate_limited_ips': len(self.__rate_limits),
            'last_event_time': self.__security_logs[-1]['timestamp'] if self.__security_logs else None
        }
    
    def get_incident_count(self) -> int:
        """Public getter for incident count"""
        return self.__incident_count
    
    def apply_security_headers(self) -> None:
        """Public method to apply security headers"""
        # In a real application, this would set HTTP security headers
        pass
    
    # ⬅️ ENCAPSULATION: Controlled access to security logs
    def get_recent_security_events(self, limit: int = 10) -> List[Dict]:
        """Public method to get recent security events (sanitized)"""
        recent_events = self.__security_logs[-limit:] if self.__security_logs else []
        
        # Return sanitized version (hide sensitive details)
        sanitized_events = []
        for event in recent_events:
            sanitized_event = {
                'timestamp': event['timestamp'],
                'event_type': event['event_type'],
                'username': event['username'][:3] + '***' if len(event['username']) > 3 else '***',
                'ip_address': event['ip_address'].split('.')[0] + '.***.***.***'
            }
            sanitized_events.append(sanitized_event)
        
        return sanitized_events

# Example usage demonstrating encapsulation
if __name__ == "__main__":
    security_manager = SecurityManager()
    
    # ✅ Correct usage - through public interface
    print("Testing security manager...")
    
    # Test password hashing
    password = "secure_password_123"
    hashed = security_manager.hash_password(password)
    print(f"Password hashed: {hashed[:20]}...")
    
    # Test password verification
    is_valid = security_manager.verify_password(password, hashed)
    print(f"Password verification: {is_valid}")
    
    # Test login validation
    can_login = security_manager.validate_login_attempt("test_user", "192.168.1.1")
    print(f"Can login: {can_login}")
    
    # ❌ Cannot access private attributes directly
    # print(security_manager.__login_attempts)  # This would cause AttributeError
    
    # ✅ Access through public interface
    status = security_manager.get_security_status()
    print(f"Security status: {status}")
