from app import app


def test_home_page():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


def test_health_endpoint():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "ok"


def test_history_page():
    client = app.test_client()
    response = client.get("/history")
    assert response.status_code == 200


def test_generate_empty_email():
    client = app.test_client()
    response = client.post("/generate", data={
        "original_email": "",
        "tone": "formal",
        "reply_length": "short"
    })
    assert response.status_code == 200
    assert b"Please enter an email first." in response.data


def test_generate_with_email():
    client = app.test_client()
    response = client.post("/generate", data={
        "original_email": "Can we meet tomorrow?",
        "tone": "formal",
        "reply_length": "short"
    })
    assert response.status_code == 200


def test_save_without_data():
    client = app.test_client()
    response = client.post("/save", data={
        "original_email": "",
        "tone": "formal",
        "reply_length": "short",
        "generated_reply": ""
    }, follow_redirects=True)
    assert response.status_code == 200


def test_improve_reply_route():
    client = app.test_client()
    response = client.post("/improve", data={
        "original_email": "Can we meet tomorrow?",
        "tone": "formal",
        "reply_length": "short",
        "generated_reply": "Thank you for your email."
    })
    assert response.status_code == 200


def test_home_contains_title():
    client = app.test_client()
    response = client.get("/")
    assert b"MailMate AI" in response.data