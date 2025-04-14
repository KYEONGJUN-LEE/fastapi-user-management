from fastapi import FastAPI, HTTPException, Depends
from db import engine, SessionLocal, Base
from pydantic import BaseModel
from models import User
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserCreate(BaseModel):
    username: str
    password: str
    name: str
    email: str


class UserUpdate(BaseModel):
    name: str
    email: str


@app.get("/")
def root():
    return {"message": "FastAPI 앱이 정상 작동중입니다."}


# 유저 생성(CREATE)
@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_data = User(
        username=user.username, 
        password=user.password,
        name=user.name, 
        email=user.email
    )
    try:
        db.add(user_data)
        db.commit()
        return {"message": "사용자 등록이 완료되었습니다."}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# 유저조회(READ)
@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    try:
        result = db.query(User).all()
        return result

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# 유저 정보 업데이트(UPDATE)
@app.put("/users/{username}")
def update_user(username: str, user: UserUpdate, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.username == username).first()
        db_user.name = user.name
        db_user.email = user.email
        db.commit()

        return {"message": "사용자 정보 수정이 완료되었습니다."}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# 유저 삭제(DELETE)
@app.delete("/users/{username}")
def delete_user(username: str, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.username == username).first()
        db.delete(db_user)
        db.commit()
        return {"message": "사용자 삭제가 완료되었습니다."}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))