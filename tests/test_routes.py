from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_ticket():
    payload = {
        "text": "I was overcharged on my last invoice. Please fix this."
    }
    response = client.post("/requests", json=payload)
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["ai_result"]["category"] == "billing"

def test_get_ticket():
    create_resp = client.post("/requests", json={"text": "System crash, need urgent help"})
    tid = create_resp.json()["id"]
    response = client.get(f"/requests/{tid}")
    assert response.status_code == 200
    assert response.json()["id"] == tid

def test_filter_tickets():
    response = client.get("/requests?category=technical")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
