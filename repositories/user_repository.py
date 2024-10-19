from typing import Optional
import mysql.connector
from mysql.connector import Error
from services.auth_service import settings
from ..models.user import User
from core import app_settings


class UserRepository:
    def __init__(self):
        self.db_connection = self.create_db_connection()

    def create_db_connection(self):
        settings = app_settings.get_settings()
        try:
            connection = mysql.connector.connect(
                host=settings.MYSQL_DB_HOST,
                user=settings.MYSQL_DB_USERNAME,
                password=settings.MYSQL_DB_PASSWORD,
                database=settings.MYSQL_DB_NAME
            )
            if connection.is_connected():
                return connection
        except Error as e:
            return None

    def find_by_user_name(self, user_name: str) -> Optional[User]:
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT id, user_name, password FROM users WHERE email = ?', (user_name,))
        row = cursor.fetchone()
        if row:
            return User(id=row[0], email=row[1], password=row[2])
        return None

    def create_user(self, user: User) -> User:
        cursor = self.db_connection.cursor()
        cursor.execute('INSERT INTO users (user_name, password) VALUES (?, ?)', (user.user_name, user.password))
        user.id = cursor.lastrowid
        self.db_connection.commit()
        return user

    def is_founder_in_club(self, user_id: int, club_id: int) -> bool:
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT id_rol FROM participant_role_club WHERE user_id = ? AND club_id = ?', (user_id, club_id))
        row = cursor.fetchone()
        if row and row[0] == 1: # 1 is the id of the founder role
            return True
        return False

