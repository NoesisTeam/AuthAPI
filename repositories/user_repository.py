from typing import Optional
from fastapi import HTTPException, Depends
from sqlalchemy import and_
from sqlalchemy.orm import Session
from core.database import get_table, get_db
from models.user import User, UserCreate


class UserRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.users_table = get_table('users')  # Obtiene la tabla de usuarios
        self.club_table = get_table('clubs')  # Obtiene la tabla de clubs

    def _get_db(self) -> Session:
        db = next(get_db())  # Obtiene la sesión usando el generador
        return db

    def find_by_user_name(self, user_name: str) -> Optional[User]:
        db = self._get_db()  # Obtiene la sesión
        try:
            query = db.query(self.users_table).filter(
                and_(self.users_table.c.user_name == user_name)
            )
            row = query.first()  # Obtiene el primer resultado
            if row:
                return User(id=row.id_user, user_name=row.user_name, user_password=row.user_password)
            return None
        finally:
            db.close()


    def create_user(self, user: UserCreate) -> UserCreate:
        db = self._get_db()
        try:
            new_user = self.users_table.insert().values(
                user_name=user.user_name,
                user_password=user.user_password
            )
            db.execute(new_user)
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()  # Asegúrate de hacer rollback en caso de error
            raise HTTPException(status_code=500, detail="Internal error in db")
        finally:
            db.close()
        return user

    def is_club_status_active(self, club_id: int):
        db = self._get_db()
        try:
            query = db.query(self.club_table).filter(
                and_(self.club_table.c.id_club == club_id)
            )
            row = query.first()
            return row.club_status == 'A' if row else False
        finally:
            db.close()

    # Obtiene el rol de un usuario en un club
    def get_role_id_in_club(self, user_id: int, club_id: int):
        db = self._get_db()  # Obtiene la sesión
        if self.is_club_status_active(club_id):
            try:
                roles_table = get_table('participant_role_club')  # Obtiene la tabla de roles
                query = db.query(roles_table).filter(
                    and_(
                        roles_table.c.id_user == user_id,
                        roles_table.c.id_club == club_id
                    )
                )
                row = query.first()
                return row.id_role if row else None
            finally:
                db.close()
        else:
            raise HTTPException(status_code=400, detail="Club does not exist or is not active")

    def get_role_name_in_club(self, user_id: int, club_id: int):
        db = self._get_db()
        roles_table = get_table('roles')
        role_id = self.get_role_id_in_club(user_id, club_id)
        query = db.query(roles_table).filter(and_(roles_table.c.id_role == role_id))
        row = query.first()
        return row.role_name if row else None

