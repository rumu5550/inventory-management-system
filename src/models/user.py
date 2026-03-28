class User:
    """Represents a user in the system with access control roles."""
    def __init__(self, username, password, role="Staff", email=None):
        self.username = username
        self.password = password
        self.role = role  # Admin, Manager, Staff
        self.email = email

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "role": self.role,
            "email": self.email
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            username=data.get("username"),
            password=data.get("password"),
            role=data.get("role", "Staff"),
            email=data.get("email")
        )
