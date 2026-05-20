from urllib.parse import quote

from src import app as app_module


def test_get_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity(client):
    email = "newstudent@mergington.edu"
    activity_name = quote("Chess Club", safe="")

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"
    assert email in app_module.activities["Chess Club"]["participants"]


def test_duplicate_signup_returns_400(client):
    email = "emma@mergington.edu"
    activity_name = quote("Programming Class", safe="")

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_for_unknown_activity_returns_404(client):
    response = client.post(
        "/activities/Unknown%20Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant(client):
    email = "michael@mergington.edu"
    activity_name = quote("Chess Club", safe="")

    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from Chess Club"
    assert email not in app_module.activities["Chess Club"]["participants"]


def test_unregister_missing_participant_returns_404(client):
    email = "missing@mergington.edu"
    activity_name = quote("Chess Club", safe="")

    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not signed up"
