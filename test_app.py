from app import app, MESSAGE

client = app.test_client()


def test_home():
    res = client.get("/")
    assert res.status_code == 200
    assert MESSAGE in res.get_data(as_text=True)


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}


def test_info():
    res = client.get("/api/info")
    assert res.status_code == 200
    assert res.get_json()["message"] == MESSAGE
