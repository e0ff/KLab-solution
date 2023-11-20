import pytest
from fastapi.testclient import TestClient
from simple_rest_app.main import app

client = TestClient(app)

def test_select():
    response = client.get("/select")
    assert response.status_code == 200
    assert response.json() == []

def test_insert():
    data = {"value": "test"}
    response = client.post("/insert", json=data)
    assert response.status_code == 200
    assert response.json() == {"id": 1, "value": "test"}

def test_delete():
    client.post("/insert", json={"value": "test"})
    response = client.delete("/delete/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Record deleted successfully"}
    response = client.get("/select")
    assert response.json() == [{'id': 2, 'value': 'test'}]

def test_begin_commit():
    response = client.post("/begin")
    assert response.status_code == 200
    assert response.json() == {"message": "Transaction opened"}

    response = client.post("/insert", json={"value": "test"})
    assert response.status_code == 200
    assert response.json() == {"message": "{'type': 'insert', 'value': 'test'} added to transaction"}

    response = client.post("/commit")
    assert response.status_code == 200
    assert response.json() == {"message": "Transaction committed successfully"}

    response = client.get("/select")
    assert response.status_code == 200
    assert response.json() == [{'id': 2, 'value': 'test'}, {"id": 3, "value": "test"}]

def test_begin_rollback():
    response = client.post("/begin")
    assert response.status_code == 200
    assert response.json() == {"message": "Transaction opened"}

    response = client.post("/insert", json={"value": "test2"})
    assert response.status_code == 200
    assert response.json() == {"message": "{'type': 'insert', 'value': 'test2'} added to transaction"}

    response = client.post("/rollback")
    assert response.status_code == 200
    assert response.json() == {"message": "Transaction rolled back successfully"}

    response = client.get("/select")
    assert response.status_code == 200
    assert response.json() == [{'id': 2, 'value': 'test'}, {"id": 3, "value": "test"}]

def test_commit_without_begin():
    response = client.post("/commit")
    assert response.status_code == 200
    assert response.json() == {"message": "Session not found"}

    response = client.get("/select")
    assert response.status_code == 200
    assert response.json() == [{'id': 2, 'value': 'test'}, {"id": 3, "value": "test"}]
