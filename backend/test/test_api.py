from fastapi.testclient import TestClient
import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
from main import app
from app.db.database import Base, get_db
from app.hashing import Hash

# Base de datos de prueba
db_path = os.path.join(os.path.dirname(__file__), "test.db")
db_uri = "sqlite:///{}".format(db_path)
SQLALCHEMY_DATABASE_URL = db_uri
engine_test = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(bind=engine_test, autocommit=False, autoflush=False)
Base.metadata.create_all(bind=engine_test)

client = TestClient(app)


def insert_test_user():
    password_hash = Hash.hash_password("testpassword")
    with engine_test.connect() as conn:
        conn.execute(
            text("INSERT INTO users (username, email, password, created_at) VALUES (:username, :email, :password, :created_at)"),
            {"username": "testuser", "email": "test@example.com", "password": password_hash, "created_at" :"2025-06-18 15:33:50.652323"}
        )
        conn.commit()


insert_test_user()


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def test_create_user():
    usuario = {
        "username": "andres1",
        "password": "awesomepassword",
        "email": "an@gmail.com",
    }
    # Create user
    response = client.post("/v1/users/", json=usuario)
    assert response.status_code == 201

    usuario_login = {"username": "testuser", "password": "testpassword"}

    # Login with the test user
    response_token = client.post("/v1/login/", data=usuario_login)
    assert response_token.status_code == 200
    assert response_token.json()["token_type"] == "bearer"


def test_delete_database():
    engine_test.dispose()
    db_path = os.path.join(os.path.dirname(__file__), "test.db")
    os.remove(db_path)