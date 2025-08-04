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
