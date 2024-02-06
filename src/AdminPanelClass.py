from config import admin_id
from src.Database.DatabaseClass import db




class AdminPanel:
    def __init__(self):
        self._admin_id = admin_id
        self.db = db

    def get_admin_id(self):
        return self._admin_id

    def get_users_number(self):
        return self.db.get_users_amount()

admin_panel = AdminPanel()
