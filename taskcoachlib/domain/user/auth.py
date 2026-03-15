# -*- coding: utf-8 -*-

"""
Task Coach - Your friendly task manager
Copyright (C) 2004-2024 Task Coach developers <developers@taskcoach.org>

Task Coach is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Task Coach is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Password hashing utilities for user authentication.
"""

import hashlib
import secrets
import base64


class PasswordHasher:
    """
    密码哈希工具类。
    
    使用PBKDF2算法进行密码哈希，支持盐值和迭代次数配置。
    """
    
    ALGORITHM = 'pbkdf2_sha256'
    ITERATIONS = 100000
    SALT_LENGTH = 16
    HASH_LENGTH = 32
    
    def hash(self, password):
        """
        对密码进行哈希处理。
        
        Args:
            password: 明文密码
            
        Returns:
            格式化的哈希字符串 (algorithm$iterations$salt$hash)
        """
        salt = secrets.token_hex(self.SALT_LENGTH)
        hash_value = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            self.ITERATIONS,
            self.HASH_LENGTH
        )
        hash_b64 = base64.b64encode(hash_value).decode('utf-8')
        return f'{self.ALGORITHM}${self.ITERATIONS}${salt}${hash_b64}'
    
    def verify(self, password, hashed_password):
        """
        验证密码是否正确。
        
        Args:
            password: 明文密码
            hashed_password: 哈希后的密码
            
        Returns:
            bool: 密码是否正确
        """
        if not hashed_password:
            return False
        
        try:
            algorithm, iterations, salt, hash_b64 = hashed_password.split('$')
        except ValueError:
            return False
        
        if algorithm != self.ALGORITHM:
            return False
        
        try:
            iterations = int(iterations)
        except ValueError:
            return False
        
        stored_hash = base64.b64decode(hash_b64)
        computed_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            iterations,
            len(stored_hash)
        )
        
        return secrets.compare_digest(stored_hash, computed_hash)
    
    def needs_update(self, hashed_password):
        """
        检查哈希是否需要更新（例如迭代次数增加）。
        
        Args:
            hashed_password: 哈希后的密码
            
        Returns:
            bool: 是否需要更新
        """
        try:
            algorithm, iterations, salt, hash_b64 = hashed_password.split('$')
            return int(iterations) < self.ITERATIONS
        except (ValueError, TypeError):
            return True


class SimplePasswordHasher:
    """
    简单密码哈希工具类。
    
    用于不需要高安全性的场景，仅使用SHA256哈希。
    """
    
    @staticmethod
    def hash(password):
        """
        对密码进行简单哈希处理。
        
        Args:
            password: 明文密码
            
        Returns:
            哈希字符串
        """
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    @staticmethod
    def verify(password, hashed_password):
        """
        验证密码是否正确。
        
        Args:
            password: 明文密码
            hashed_password: 哈希后的密码
            
        Returns:
            bool: 密码是否正确
        """
        return SimplePasswordHasher.hash(password) == hashed_password


def validate_password_strength(password):
    """
    验证密码强度。
    
    Args:
        password: 明文密码
        
    Returns:
        tuple: (是否有效, 错误消息列表)
    """
    errors = []
    
    if len(password) < 8:
        errors.append('密码长度至少为8个字符')
    
    if len(password) > 128:
        errors.append('密码长度不能超过128个字符')
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password)
    
    if not (has_upper and has_lower):
        errors.append('密码应包含大小写字母')
    
    if not has_digit:
        errors.append('密码应包含数字')
    
    if not has_special:
        errors.append('密码应包含特殊字符')
    
    return len(errors) == 0, errors
