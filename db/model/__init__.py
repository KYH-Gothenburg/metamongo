from db.base_document import Document, db


class Customer(Document):
    collection = db.customers

class Api(Document):
    collection = db.apis


class ApiDB(Document):
    collection = db.api_db