from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:12345@localhost:3306/book-inventory-python"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

##### MODELS #####
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    author = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Double(), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.String(50), nullable=False)
    
    def __init__(self, title, author, price, quantity, isbn):
        self.title = title 
        self.author = author 
        self.price = price 
        self.quantity = quantity 
        self.isbn = isbn
        
    def __repr__(self):
        return f'<Book {self.title}>'


##### ROUTES #####
@app.route('/', methods=['GET'])
def main():
    return jsonify({'message': 'hola'}), 200

@app.route("/book", methods=['GET'])
def getBooks():
    books = Book.query.all()
    book_list = []
    for book in books:
        bookData = {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "price": book.price,
            "quantity": book.quantity,
            "isbn": book.isbn
        }
        book_list.append(bookData)
    return jsonify(book_list), 200

@app.route('/book/<int:id>', methods=['GET'])
def getBookById(id):
    book = Book.query.get(id)
    if book is None:
        return jsonify({'message': 'Book not found!'}), 404
        
    bookData = {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "price": book.price,
        "quantity": book.quantity,
        "isbn": book.isbn
    }
    return jsonify(bookData), 200

@app.route("/book", methods=['POST'])
def saveBook():
    data = request.get_json()
    
    title = data['title'] 
    author = data['author'] 
    price = data['price'] 
    quantity = data['quantity'] 
    isbn = data['isbn']
    
    book = Book(title, author, price, quantity, isbn)
    db.session.add(book)
    db.session.commit()
    
    newBook = {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "price": book.price,
        "quantity": book.quantity,
        "isbn": book.isbn
    }
    
    return jsonify(newBook), 201

@app.route("/book/<int:id>", methods=['PUT'])
def updateBook(id):
    
    book = Book.query.get(id)
    data = request.get_json()
    
    if book is None:
        return jsonify({'message': 'Book not found!'}), 404
        
    
    book.title = data['title'] 
    book.author = data['author'] 
    book.price = data['price'] 
    book.quantity = data['quantity'] 
    book.isbn = data['isbn']
    
    db.session.commit()
    
    bookData = {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "price": book.price,
        "quantity": book.quantity,
        "isbn": book.isbn
    }
    
    return jsonify(bookData), 200

@app.route("/book/<int:id>", methods=['DELETE'])
def deleteBook(id):
    
    book = Book.query.get(id)
    
    if book is None:
        return jsonify({'message': 'Book not found!'}), 404
    
    db.session.delete(book)
    db.session.commit()
    
    return jsonify({"message": "Book deleted!"}), 200

@app.route("/book/<int:id>/sell", methods=['PUT'])
def sellBook(id):
    
    book = Book.query.get(id)
    data = request.get_json()
    
    if book is None:
        return jsonify({'message': 'Book not found!'}), 404
        
    if data['quantity'] <= 0:
        return jsonify({'message': 'The quantity of sale must be a positive number!'}), 405
    elif book.quantity >= data['quantity']:
        book.quantity = book.quantity - data['quantity']
    else:
        return jsonify({'message': 'Book does not have enought stock!'}), 405
        
    db.session.commit()
    
    bookData = {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "price": book.price,
        "quantity": book.quantity,
        "isbn": book.isbn
    }
    
    return jsonify(bookData), 200

@app.route("/book/<int:id>/restock", methods=['PUT'])
def restockBook(id):
    
    book = Book.query.get(id)
    data = request.get_json()
    
    if book is None:
        return jsonify({'message': 'Book not found!'}), 404
        
    if data['quantity'] <= 0:
        return jsonify({'message': 'The quantity of restock must be a positive number!'}), 405
    else:
        book.quantity = book.quantity + data['quantity']
        
    db.session.commit()
    
    bookData = {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "price": book.price,
        "quantity": book.quantity,
        "isbn": book.isbn
    }
    
    return jsonify(bookData), 200

if __name__ == '__main__':
    app.run(port=5000)