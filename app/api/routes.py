from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Book, contact_schema, contacts_schema

api = Blueprint('api',__name__, url_prefix='/api')

#Creating
@api.route('/library', methods = ['POST'])
@token_required
def create_book(current_user_token):
    authors_first_name = request.json['authors_first_name']
    authors_last_name = request.json['authors_last_name']
    book_title = request.json['book_title']
    genre = request.json['genre']
    pages=request.json['pages']

    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')




    book = Book(authors_first_name,authors_last_name,book_title,genre,pages, user_token = user_token )

    db.session.add(book)
    db.session.commit()

    response = contact_schema.dump(book)
    return jsonify(response)
#Retrieving all 
@api.route('/library', methods=['GET'])
@token_required
def get_all_books(current_user_token):
    a_user=current_user_token.token
    book=Book.query.filter_by(user_token=a_user).all()
    response=contacts_schema.dump(book)
    return jsonify(response)


#Retrieving single
@api.route('library/<id>',methods=['GET'])
@token_required
def get_single_book(current_user_token,id):
    book=Book.query.get(id)
    response=contact_schema.dump(book)
    return jsonify(response)

#Updating
@api.route('/library/<id>', methods=['POST','PUT'])
@token_required
def update_book(current_user_token, id):
    book=Book.query.get(id)
    book.authors_first_name = request.json['authors_first_name']
    book.authors_last_name = request.json['authors_last_name']
    book.book_title = request.json['book_title']
    book.genre = request.json['genre']
    book.pages = request.json['pages']
    book.user_token = current_user_token.token

    db.session.commit()
    response = contact_schema.dump(book)
    return jsonify(response)

#Deleting contact
@api.route('/library/<id>', methods=['Delete'])
@token_required
def delete_car(current_user_token,id):
    book= Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response= contact_schema.dump(book)
    return jsonify(response)

