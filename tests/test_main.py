import pytest
from src.main import app
import json

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_main(client):
    response = client.get('/')
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data['message'] == 'hola'
    
def test_get_books(client):
    response = client.get('/book')
    json_data = response.get_json()
    assert response.status_code == 200
    
def test_get_book(client):
    response = client.get('/book/1')
    json_data = response.get_json()
    assert response.status_code == 200

def test_get_book_not_found(client):
    response = client.get('/book/3000')
    json_data = response.get_json()
    assert response.status_code == 404
    
def test_save_book(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    test_book = {
        "title" : "test title book",
        "author" : "test author book",
        "price" : 400.00,
        "quantity" : 5,
        "isbn" : "1"
    }
    response = client.post('/book', data=json.dumps(test_book), headers=headers)
    json_data = response.get_json()
    assert response.status_code == 201
    
def test_update_book(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    test_book = {
        "title" : "test title book",
        "author" : "test author book",
        "price" : 400.00,
        "quantity" : 5,
        "isbn" : "1"
    }
    response = client.put('/book/1', data=json.dumps(test_book), headers=headers)
    json_data = response.get_json()
    assert response.status_code == 200
    
def test_update_book_failed(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    test_book = {
        "title" : "test title book",
        "author" : "test author book",
        "price" : 400.00,
        "quantity" : 5,
        "isbn" : "1"
    }
    response = client.put('/book/3000', data=json.dumps(test_book), headers=headers)
    json_data = response.get_json()
    assert response.status_code == 404
    
def test_delete_book_failed(client):
    response = client.delete('/book/3000')
    json_data = response.get_json()
    assert response.status_code == 404
    
def test_sell_book(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    test_book = {
        "quantity" : 1
    }
    response = client.put('/book/1/sell', data=json.dumps(test_book), headers=headers)
    json_data = response.get_json()
    assert response.status_code == 200
    
def test_sell_book_notfound(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    test_book = {
        "quantity" : 5
    }
    response = client.put('/book/3000/sell', data=json.dumps(test_book), headers=headers)
    json_data = response.get_json()
    assert response.status_code == 404
    
def test_sell_book_quantity_zero(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    test_book = {
        "quantity" : 0
    }
    response = client.put('/book/1/sell', data=json.dumps(test_book), headers=headers)
    json_data = response.get_json()
    assert response.status_code == 405
    
def test_sell_book_quantity_negative(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    test_book = {
        "quantity" : -10
    }
    response = client.put('/book/1/sell', data=json.dumps(test_book), headers=headers)
    json_data = response.get_json()
    assert response.status_code == 405
    
def test_sell_book_without_enought_stock(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    test_book = {
        "quantity" : 100
    }
    response = client.put('/book/1/sell', data=json.dumps(test_book), headers=headers)
    json_data = response.get_json()
    assert response.status_code == 405
    
def test_restock_book(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    test_book = {
        "quantity" : 1
    }
    response = client.put('/book/1/restock', data=json.dumps(test_book), headers=headers)
    json_data = response.get_json()
    assert response.status_code == 200
    
def test_restock_book_notfound(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    test_book = {
        "quantity" : 5
    }
    response = client.put('/book/3000/restock', data=json.dumps(test_book), headers=headers)
    json_data = response.get_json()
    assert response.status_code == 404
    
def test_restock_book_quantity_zero(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    test_book = {
        "quantity" : 0
    }
    response = client.put('/book/1/restock', data=json.dumps(test_book), headers=headers)
    json_data = response.get_json()
    assert response.status_code == 405
    
def test_restock_book_quantity_negative(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    test_book = {
        "quantity" : -10
    }
    response = client.put('/book/1/sell', data=json.dumps(test_book), headers=headers)
    json_data = response.get_json()
    assert response.status_code == 405