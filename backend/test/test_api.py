from pydoc import cli
from fastapi.testclient import TestClient
import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
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
            text(
                "INSERT INTO users (username, email, password, created_at) VALUES (:username, :email, :password, :created_at)"
            ),
            {
                "username": "testuser",
                "email": "test@email.com",
                "password": password_hash,
                "created_at": "2025-06-18 15:33:50.652323",
            },
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

    usuario_login = {"username": "andres1", "password": "awesomepassword"}

    # Login with the test user
    response_token = client.post("/v1/login/", data=usuario_login)
    assert response_token.status_code == 200
    assert response_token.json()["token_type"] == "bearer"


def test_get_all_users():
    response_token = client.post(
        "/v1/login/", data={"username": "testuser", "password": "testpassword"}
    )
    assert response_token.status_code == 200
    headers = {"Authorization": f"Bearer {response_token.json()['access_token']}"}
    response = client.get("/v1/users/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


def test_get_user():
    response = client.get("/v1/users/1")
    assert response.json()["username"] == "testuser"


def test_update_user():
    response_token = client.post(
        "/v1/login/", data={"username": "testuser", "password": "testpassword"}
    )
    assert response_token.status_code == 200
    headers = {"Authorization": f"Bearer {response_token.json()['access_token']}"}
    user = {"username": "updateduser"}
    response = client.patch("/v1/users/1", headers=headers, json=user)
    assert response.status_code == 200


def test_create_news():
    response_token = client.post(
        "/v1/login/", data={"username": "updateduser", "password": "testpassword"}
    )
    assert response_token.status_code == 200

    headers = {"Authorization": f"Bearer {response_token.json()['access_token']}"}

    news_data = {
        "title": "Test News",
        "content": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Nam quam nunc, blandit vel, luctus pulvinar, hendrerit id, lorem. Maecenas nec odio et ante tincidunt tempus. Donec vitae sapien ut libero venenatis faucibus. Nullam quis ante. Etiam sit amet orci eget eros faucibus tincidunt. Duis leo. Sed fringilla mauris sit amet nibh. Donec sodales sagittis magna. Sed consequat, leo eget bibendum sodales, augue velit cursus nunc, quis gravida magna mi a libero. Fusce vulputate eleifend sapien. Vestibulum purus quam, scelerisque ut, mollis sed, nonummy id, metus. Nullam accumsan lorem in dui. Cras ultricies mi eu turpis hendrerit fringilla. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; In ac dui quis mi consectetuer lacinia. Nam pretium turpis et arcu. Duis arcu tortor, suscipit eget, imperdiet nec, imperdiet iaculis, ipsum. Sed aliquam ultrices mauris. Integer ante arcu, accumsan a, consectetuer eget, posuere ut, mauris. Praesent adipiscing. Phasellus ullamcorper ipsum rutrum nunc. Nunc nonummy metus. Vestibulum volutpat pretium libero. Cras id dui. Aenean ut eros et nisl sagittis vestibulum. Nullam nulla eros, ultricies sit amet, nonummy id, imperdiet feugiat, pede. Sed lectus. Donec mollis hendrerit risus. Phasellus nec sem in justo pellentesque facilisis. Etiam imperdiet imperdiet orci. Nunc nec neque. Phasellus leo dolor, tempus non, auctor et, hendrerit quis, nisi. Curabitur ligula sapien, tincidunt non, euismod vitae, posuere imperdiet, leo. Maecenas malesuada. Praesent congue erat at massa. Sed cursus turpis vitae tortor. Donec posuere vulputate arcu. Phasellus accumsan cursus velit. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Sed aliquam, nisi quis porttitor congue, elit erat euismod orci, ac placerat dolor lectus quis orci. Phasellus consectetuer vestibulum elit. Aenean tellus metus, bibendum sed, posuere ac, mattis non, nunc. Vestibulum fringilla pede sit amet augue. In turpis. Pellentesque posuere. Praesent turpis. Aenean posuere, tortor sed cursus feugiat, nunc augue blandit nunc, eu sollicitudin urna dolor sagittis lacus. Donec elit libero, sodales nec, volutpat a, suscipit non, turpis. Nullam sagittis. Suspendisse pulvinar, augue ac venenatis condimentum, sem libero volutpat nibh, nec pellentesque velit pede quis nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Fusce id purus. Ut varius tincidunt libero. Phasellus dolor. Maecenas vestibulum mollis diam. Pellentesque ut neque. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. In dui magna, posuere eget, vestibulum et, tempor auctor, justo. In ac felis quis tortor malesuada pretium. Pellentesque auctor neque nec urna. Proin sapien ipsum, porta a, auctor quis, euismod ut, mi. Aenean viverra rhoncus pede. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Ut non enim eleifend felis pretium feugiat. Vivamus quis mi. Phasellus a est. Phasellus magna. In hac habitasse platea dictumst. Curabitur at lacus ac velit ornare lobortis. Curabitur a felis in nunc fringilla tristique. Morbi mattis ullamcorper velit. Phasellus gravida semper nisi. Nullam vel sem. Pellentesque libero tortor, tincidunt et, tincidunt eget, semper nec, quam. Sed hendrerit. Morbi ac felis. Nunc egestas, augue at pellentesque laoreet, felis eros vehicula leo, at malesuada velit leo quis pede. Donec interdum, metus et hendrerit aliquet, dolor diam sagittis ligula, eget egestas libero turpis vel mi. Nunc nulla. Fusce risus nisl, viverra et, tempor et, pretium in, sapien. Donec venenatis vulputate lorem. Morbi nec metus. Phasellus blandit leo ut odio. Maecenas ullamcorper, dui et placerat feugiat, eros pede varius nisi, condimentum viverra felis nunc et lorem. Sed magna purus, fermentum eu, tincidunt eu, varius ut, felis. In auctor lobortis lacus. Quisque libero metus, condimentum nec, tempor a, commodo mollis, magna. Vestibulum ullamcorper mauris at ligula. Fusce fermentum. Nullam cursus lacinia erat. Praesent blandit laoreet nibh. Fusce convallis metus id felis luctus adipiscing. Pellentesque egestas, neque sit amet convallis pulvinar, justo nulla eleifend augue, ac auctor orci leo non est. Quisque id mi. Ut tincidunt tincidunt erat. Etiam feugiat lorem non metus. Vestibulum dapibus nunc ac augue. Curabitur vestibulum aliquam leo. Praesent egestas neque eu enim. In hac habitasse platea dictumst. Fusce a quam. Etiam ut purus mattis mauris",
        "section": "culture",
        "author": 1,
    }

    # Fake image data for testing
    import io

    file_content = b"fake image data"
    files = {"image": ("test_image.jpg", io.BytesIO(file_content), "image/jpeg")}

    response = client.post("/v1/news/", data=news_data, files=files, headers=headers)

    assert response.status_code == 201


def test_read_news():
    response = client.get("/v1/news/1")
    assert response.status_code == 200
    assert response.json()["title"] == "Test News"


def test_update_news():
    response_token = client.post(
        "/v1/login/", data={"username": "updateduser", "password": "testpassword"}
    )
    assert response_token.status_code == 200
    headers = {"Authorization": f"Bearer {response_token.json()['access_token']}"}
    news_update = {"title": "Updated Test News"}
    response = client.patch("/v1/news/1", headers=headers, json=news_update)
    assert response.status_code == 200


def test_delete_news():
    response_token = client.post(
        "/v1/login/", data={"username": "updateduser", "password": "testpassword"}
    )
    assert response_token.status_code == 200
    headers = {"Authorization": f"Bearer {response_token.json()['access_token']}"}
    response = client.delete("/v1/news/1", headers=headers)
    assert response.status_code == 200


def test_delete_user():
    response_token = client.post(
        "/v1/login/", data={"username": "updateduser", "password": "testpassword"}
    )
    assert response_token.status_code == 200
    headers = {"Authorization": f"Bearer {response_token.json()['access_token']}"}
    response = client.delete("/v1/users/1", headers=headers)
    assert response.status_code == 200


def test_delete_database():
    engine_test.dispose()
    db_path = os.path.join(os.path.dirname(__file__), "test.db")
    os.remove(db_path)
