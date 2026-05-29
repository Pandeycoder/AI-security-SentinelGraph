from enum import str, Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    SECURITY_ANALYST = "security_analyst"
    USER = "user"
    AUDITOR = "auditor"
