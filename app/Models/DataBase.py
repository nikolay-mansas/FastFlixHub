from app.Models.DataBaseSQL import create_table_sql, search_user_by_ID, search_user_by_email
import asyncpg
from passlib.context import CryptContext
from time import time
# from typing import Optional


class DataBase:
    async def _create_table(self) -> None:
        await self.connection.execute(create_table_sql)

        return None

    def __init__(self, db_name: str, db_user: str, db_password: str, db_url: str) -> None:
        self.db_name: str = db_name
        self.db_user: str = db_user
        self.db_password: str = db_password
        self.db_url: str = db_url
        # self.connection: Optional[asyncpg.connect] = None
        self.connection: None | asyncpg.Connection = None
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        return

    async def connect(self) -> None:
        self.connection = await asyncpg.connect(database=self.db_name,
                                                user=self.db_user,
                                                password=self.db_password,
                                                host=self.db_url)
        await self._create_table()

        return None

    async def close(self) -> None:
        await self.connection.close()

        return None

    async def new_user(self, email: str, password: str):
        pwd_hash = self.pwd_context.hash(password)
        await self.connection.execute(create_table_sql)

    async def delete_user(self, login: str):
        ...

    async def search_user(self, _id: int | None = None, email: str | None = None) -> dict:
        if email is not None:
            if ("'" in email) or ('"' in email) or ('`' in email) or ('’' in email) or ('”' in email):
                return {"status": False, "message": "Error email"}
            else:
                sql = (search_user_by_email, (email,))
        elif _id is not None:
            if (type(_id) is not int) or (_id < 0):
                return {"status": False, "message": "Error id"}
            else:
                sql = (search_user_by_ID, (_id,))
        else:
            return {"status": False, "message": "Id and email is None"}
        print(sql)

        rows = await self.connection.fetch(sql[0], sql[1])

        return {"status": True, "message": rows}
