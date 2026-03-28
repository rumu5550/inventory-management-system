from src.models.user import User
from src.storage.json_store import JsonStore

class AuthService:
    """Manages authentication and access control logic."""
    def __init__(self):
        self.store = JsonStore("users")
        self.users = {u['username']: User.from_dict(u) for u in self.store.load()}
        # Initial admin if no users exist
        if not self.users:
            admin = User("admin", "admin123", "Admin")
            self.users[admin.username] = admin
            self.save_users()

    def register(self, username, password, role="Staff", email=None):
        if username in self.users:
            return False, "User already exists"
        user = User(username, password, role, email)
        self.users[username] = user
        self.save_users()
        return True, "User registered"

    def login(self, username, password):
        user = self.users.get(username)
        if user and user.password == password:
            return True, user
        return False, "Invalid credentials"

    def reset_password(self, username, new_password):
        if username in self.users:
            self.users[username].password = new_password
            self.save_users()
            return True, "Password reset"
        return False, "User not found"

    def save_users(self):
        self.store.save([u.to_dict() for u in self.users.values()])
