def test_create_and_list_tasks(client):
    # Register and login to get a token
    client.post(
        "/api/v1/auth/register",
        json={"email": "task@example.com", "password": "password123"},
    )
    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": "task@example.com", "password": "password123"},
    )
    token = login_res.json()["accessToken"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create a task
    response = client.post(
        "/api/v1/tasks",
        json={"title": "Test Task", "description": "This is a test"},
        headers=headers,
    )
    assert response.status_code == 201
    task_id = response.json()["id"]

    # List tasks
    response = client.get("/api/v1/tasks", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "Test Task"

    # Get single task
    response = client.get(f"/api/v1/tasks/{task_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"


def test_unauthorized_access(client):
    response = client.get("/api/v1/tasks")
    assert response.status_code == 401
