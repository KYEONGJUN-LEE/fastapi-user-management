from fastapi import FastAPI, HTTPException
from mysql.connector import Error
from db import create_conn
from pydantic import BaseModel

app = FastAPI()

class UserCreate(BaseModel):
    username : str
    password : str
    name : str
    email : str

class UserUpdate(BaseModel):
    name : str
    email : str

@app.get("/")
def root():
    return {"message : " "FastAPI 앱이 정상 작동중입니다."}

@app.post("/users")
def create_user(user: UserCreate):
    conn, cursor = create_conn()
    
    if not conn or not cursor:
        raise HTTPException(status_code=500, detail="DB 연결 실패")

    try:
        sql = """
        INSERT INTO users (username, password, name, email)
        VALUES (%s, %s, %s, %s)
        """
        user_data = (user.username, user.password, user.name, user.email)
        cursor.execute(sql, user_data)
        conn.commit()
        return {"message": f"사용자 '{user.username}' 추가 완료!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"사용자 추가 실패: {str(e)}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("연결 종료됨")


@app.get("/users")
def get_users():
    conn, cursor = create_conn()
    if not conn or not cursor:
        raise HTTPException(status_code=500, detail="DB 연결 실패")

    try:
        cursor.execute("SELECT user_id, username, name, email, created_at FROM users")
        result = cursor.fetchall()
        users = [
            {
                "user_id": row[0],
                "username": row[1],
                "name": row[2],
                "email": row[3],
                "created_at": row[4]
            }
            for row in result
        ]
        return users
    except Error as e:
        raise HTTPException(status_code=500, detail=f"조회 실패: {str(e)}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
# get_user()

@app.put("/users/{username}")
def update_user(username: str, user: UserUpdate):
    conn, cursor = create_conn()

    if not conn or not cursor:
        raise HTTPException(status_code=500, detail="DB 연결 실패")

    try:
        sql = "UPDATE users SET name = %s, email = %s WHERE username = %s"
        values = (user.name, user.email, username)
        cursor.execute(sql, values)
        conn.commit()

        return {"message": f"사용자 '{username}' 정보가 수정되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"수정 실패: {str(e)}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
# update_user()

# DELETE문
@app.delete("/users/{username}")
def delete_user(username: str):
    conn, cursor = create_conn()
    
    if not conn or not cursor:
        raise HTTPException(status_code=500, detail="DB 연결 실패")

    try:
        sql = "DELETE FROM users WHERE username = %s"
        cursor.execute(sql, (username,))
        conn.commit()

        if cursor.rowcount > 0:
            return {"message": f"사용자 '{username}' 삭제 완료"}
        else:
            raise HTTPException(status_code=404, detail=f"사용자 '{username}'를 찾을 수 없습니다.")
    except Error as e:
        raise HTTPException(status_code=500, detail=f"삭제 실패: {str(e)}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
# delete_user()