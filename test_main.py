import http
import pytest
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == http.HTTPStatus.OK
    assert response.json() == {"Hello": "World"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == http.HTTPStatus.OK
    assert response.json() == {"status": "healthy"} 

def test_validation_error():
    response = client.post("/api/books/", json={}) 
    assert response.status_code == http.HTTPStatus.BAD_REQUEST
    assert "error" in response.json()
    assert response.json()["status_code"] == http.HTTPStatus.BAD_REQUEST

def test_internal_server_error():
    response = client.get("/api/force_error")
    assert response.status_code == http.HTTPStatus.INTERNAL_SERVER_ERROR
    assert "detail" in response.json()
    assert response.json()["detail"] == "Forced Error"

def test_create_book():
    response = client.post("/api/books/", json={
        "name": "Test Book",
        "isbn": "1234567890",
        "author": "Test Author"
    })
    assert response.status_code == http.HTTPStatus.CREATED
    assert response.json()["name"] == "Test Book"
    assert response.json()["isbn"] == "1234567890123"
    assert response.json()["author"] == "Test Author"


def test_get_book():
    response = client.get("/api/books/1") 
    assert response.status_code == http.HTTPStatus.OK
    assert "name" in response.json()

def test_update_book():
    response = client.put("/api/books/1", json={
        "name": "Updated Book",
        "isbn": "1234567890",
        "author": "Updated Author"
    })
    assert response.status_code == http.HTTPStatus.OK
    assert response.json()["name"] == "Updated Book"

def test_delete_book():
    response = client.delete("/api/books/1")
    assert response.status_code == http.HTTPStatus.NO_CONTENT

def test_get_books_list():
    response = client.get("/api/books/")
    assert response.status_code == http.HTTPStatus.OK
    assert isinstance(response.json(), list) 

def test_not_found_error():
    response = client.get("/api/nonexistent_endpoint")
    assert response.status_code == http.HTTPStatus.NOT_FOUND
    assert "error" in response.json()
    assert response.json()["status_code"] == http.HTTPStatus.NOT_FOUND
