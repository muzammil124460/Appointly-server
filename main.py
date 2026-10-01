from fastapi import FastAPI
from src.routes.auth import auth_router
from src.routes.chat import chat_route
from src.routes.admin import admin_route
from fastapi.middleware.cors import CORSMiddleware
from src.model.user import User 
from src.db.DataBase import Base,DB,get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from src.model.ai_operation import ai_Database
app = FastAPI(title="MyApp")

origins = [
    "https://appointly-frontend.onrender.com",  
    "http://localhost:5173"         
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# join routes

Base.metadata.create_all(bind=DB)
app.include_router(auth_router)
app.include_router(chat_route)
app.include_router(admin_route)



@app.get("/")
def health_check(db: Session = Depends(get_db)):
    try:
        data = db.query(ai_Database).limit(1).all()

        if len(data) == 0:
            return "database is connected but table is empty"

        return "server and database are working"

    except Exception as e:
        return f"error: {e}"



