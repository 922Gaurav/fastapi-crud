from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    
def test_get_teas():
    response = client.get("/teas")
    assert response.status_code == 200
    
def test_post_teas():
    response = client.post("/teas", json={"id": 6, "name": "Green Tea", "origin": "China"})
    assert response.status_code == 201