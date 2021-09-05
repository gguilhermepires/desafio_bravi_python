# -*- coding: utf-8 -*-
from app.infrastructure import exceptions

logger = None


class EntityMixin(object):

    def save(self):
        self.db_instance.save_db()

    def update_me(self, json_data):
        json_data.pop('username', None)
        self.db_instance.update_from_json(json_data)

    def delete(self):
        self.delete()

    def as_dict(self):
        raise NotImplementedError


class Entity(EntityMixin):
    repository = None

    @classmethod
    def list_all(cls):
        return [cls.create_with_instance(db_instance) for db_instance in cls.repository.list_all()]

    @classmethod
    def create_new(cls, json_data):
        try:
            return cls.create_with_instance(cls.repository.create_from_json(json_data))
        except exceptions.RepositoryError as ex:
            if 'already exists' in str(ex).lower:
                raise exceptions.AlreadyExist('Entity with {} already exists in repository'.format(json_data))

    @classmethod
    def create_new_with_prepare(cls, json_data):
        try:
            return cls.create_with_instance(cls.repository.create_from_json_with_prepare(json_data))
        except exceptions.RepositoryError as ex:
            if 'already exists' in str(ex).lower:
                raise exceptions.AlreadyExist('Entity with {} already exists in repository'.format(json_data))

    @classmethod
    def create_with_id(cls, entity_id):
        db_instance = cls.repository.get(entity_id)
        return cls.create_with_instance(db_instance)

    @classmethod
    def create_with_instance(cls, db_instance):
        if db_instance is None:
            return None
        return cls(db_instance)

    def __init__(self, db_instance):
        self.db_instance = db_instance


class Aggregated(EntityMixin):
    repository = None

    @classmethod
    def create_with_parent(cls, db_instance, parent):
        if db_instance is None:
            return None
        return cls(db_instance, parent)

    @classmethod
    def create_with_id_for_parent(cls, entity_id, parent):
        db_instance = cls.repository.get(entity_id)
        return cls.create_with_parent(db_instance, parent)

    @classmethod
    def create_new_with_prepare(cls, json_data, parent):
        try:
            return cls.create_with_parent(cls.repository.create_from_json_with_prepare(json_data), parent)
        except exceptions.RepositoryError as ex:
            if 'already exists' in str(ex).lower:
                raise exceptions.AlreadyExist('Entity with {} already exists in repository'.format(json_data))

    def __init__(self, db_instance, parent):
        self.db_instance = db_instance
        self._parent = parent
        self._validate_parenthood()

    def _validate_parenthood(self):
        raise NotImplementedError
