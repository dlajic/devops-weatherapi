def test_post_weather_missing_field(client):
    response = client.post("/weather", json={"temperature": 22.0})
    assert response.status_code == 422  # Unprocessable Entity (Validation Error)

def test_post_weather_invalid_type(client):
    response = client.post("/weather", json={"city": "Berlin", "temperature": "warm"})
    assert response.status_code == 422

def test_get_weather_when_empty(client):
    response = client.get("/weather")
    assert response.status_code == 200
    assert response.json() == []

def test_post_weather_extra_field(client):
    response = client.post("/weather", json={
        "city": "Berlin",
        "temperature": 20.5,
        "pressure": 1000  # Feld existiert nicht im Modell
    })
    assert response.status_code == 200  # Extra-Felder ignoriert FastAPI (by default)

def test_delete_weather_not_found(client):
    response = client.delete("/weather/9999")
    assert response.status_code == 404

def test_download_weather_excel_no_data(client):
    response = client.get("/weather/download_excel?from_date=2050-01-01&to_date=2050-01-02")
    assert response.status_code == 404

