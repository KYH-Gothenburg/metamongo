from collections import UserDict, UserList
from pymongo import MongoClient
from abc import ABC


client = MongoClient('mongodb://root:s3cr37@localhost:27027')


db = client.api_project

class Dict(dict):
    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return repr(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __delitem__(self, key):
        del self.__dict__[key]

    def clear(self):
        return self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    def has_key(self, k):
        return k in self.__dict__

    def update(self, *args, **kwargs):
        return self.__dict__.update(*args, **kwargs)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def pop(self, *args):
        return self.__dict__.pop(*args)

    def __eq__(self, dict_):
        return self.__eq__(self.__dict__, dict_)

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)


class ResultList(UserList):
    def first_or_none(self):
        return self[0] if len(self) > 0 else None

    def last_or_none(self):
        return self[-1] if len(self) > 0 else None


class Document(Dict, ABC):
    collection = None

    def __init__(self, data):
        super().__init__()
        if '_id' not in data:
            self._id = None
        self.__dict__.update(data)

    def __repr__(self):
        return '\n'.join(f'{k} = {v}' for k, v in self.__dict__.items())

    def save(self):
        if not self._id:
            del(self.__dict__['_id'])
            return self.collection.insert_one(self.__dict__)
        else:
            return self.collection.update_one({'_id': self._id}, {'$set': self.__dict__})

    def update_doc(self, field):
        return self.collection.update_one({'_id': self._id}, {'$set': {field: self.__dict__[field]}})

    def update_field(self, field_name, new_value):
        self.collection.update_one({'_id': self._id},{'$set': {field_name: new_value}})

    def insert_into_embedded_list(self, field_name, new_value):
        self.collection.update_one({'_id': self._id},{'$push': {field_name: new_value}})

    # self.collection.update_one({'_id': ObjectId('5fce3603d1be4b17885292b6'),{'$push': {'cars': {'brand': 'Volvo', 'year': 2010}}})

    @classmethod
    def insert_many(cls, items):
        for item in items:
            cls(item).save()

    @classmethod
    def all(cls):
        return [cls(item) for item in cls.collection.find({})]

    @classmethod
    def find(cls, **kwargs):
        return ResultList(cls(item) for item in cls.collection.find(kwargs))

    @classmethod
    def query(cls, args):
        return ResultList(cls(item) for item in cls.collection.find(args))

    @classmethod
    def select_fields(cls, filter, fields):
        return ResultList(cls(item) for item in cls.collection.find(filter, fields))

    @classmethod
    def delete(cls, **kwargs):
        cls.collection.delete_many(kwargs)







