def test_create_and_get_weather(client):
    # 1. Wettereintrag speichern
    response = client.post("/weather", json={
        "city": "Berlin",
        "temperature": 23.5
    })
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "Berlin"
    assert data["temperature"] == 23.5
    assert "id" in data

    # 2. Abrufen und prüfen, ob Eintrag da ist
    get_response = client.get("/weather")
    assert get_response.status_code == 200
    results = get_response.json()
    assert len(results) == 1
    assert results[0]["city"] == "Berlin"

def test_delete_weather_success(client):
    # Erst neuen Eintrag anlegen
    response = client.post("/weather", json={"city": "Berlin", "temperature": 25})
    entry_id = response.json()["id"]

    # Dann löschen
    delete_response = client.delete(f"/weather/{entry_id}")
    assert delete_response.status_code == 200
    assert "gelöscht" in delete_response.json()["message"]

def test_get_weather_range(client):
    client.post("/weather", json={"city": "Berlin", "temperature": 23.0, "timestamp": "2024-01-01T10:00:00"})
    response = client.get("/weather/range?from_date=2024-01-01&to_date=2024-01-02")
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_get_available_dates(client):
    client.post("/weather", json={"city": "Berlin", "temperature": 23.0, "timestamp": "2024-01-01T10:00:00"})
    response = client.get("/weather/dates")
    assert response.status_code == 200
    assert "2024-01-01" in response.json()

def test_download_weather_excel(client):
    client.post("/weather", json={"city": "Berlin", "temperature": 23.0, "timestamp": "2024-01-01T10:00:00"})
    response = client.get("/weather/download_excel?from_date=2024-01-01&to_date=2024-01-02")
    assert response.status_code == 200
    assert response.headers["Content-Disposition"].startswith("attachment")

def test_preview_weather_data(client):
    for i in range(6):
        client.post("/weather", json={
            "city": "Berlin",
            "temperature": 20 + i,
            "timestamp": f"2024-01-0{i+1}T10:00:00"
        })
    response = client.get("/weather/preview?from_date=2024-01-01&to_date=2024-01-10")
    assert response.status_code == 200
    assert len(response.json()) >= 6
