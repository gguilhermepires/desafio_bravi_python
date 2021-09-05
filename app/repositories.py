# -*- coding: utf-8 -*-
from datetime import datetime
from sqlalchemy import exc, desc
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext import declarative
import app.infrastructure.database
from app.infrastructure import exceptions

db = app.infrastructure.database.AppRepository.db


class AbstractModel(object):

    @classmethod
    def one_or_none(cls, **kwargs):
        return cls.filter(**kwargs).one_or_none()

    @classmethod
    def filter(cls, **kwargs):
        return cls.query.filter_by(**kwargs)

    @classmethod
    def create_from_json(cls, json_data):
        try:
            instance = cls()
            instance.set_values(json_data)
            instance.save_db()
            return instance
        except exc.IntegrityError as ex:
            db.session.rollback()
            raise exceptions.RepositoryError(ex)

    @classmethod
    def create_from_json_with_prepare(cls, json_data):
        try:
            instance = cls()
            instance.set_values(json_data)
            instance.prepare_save()
            return instance
        except exc.IntegrityError as ex:
            db.session.rollback()
            raise exceptions.RepositoryError(ex)

    @classmethod
    def list_with_filter(cls, **kwargs):
        return cls.query.filter_by(**kwargs).all()

    @classmethod
    def list_with_filter_order_by_id(cls, **kwargs):
        return cls.query.order_by(desc("id")).filter_by(**kwargs).all()

    @classmethod
    def list_all(cls):
        return cls.query.all()

    @classmethod
    def get_with_filter(cls, **kwargs):
        return cls.query.filter_by(**kwargs).one_or_none()

    @classmethod
    def get(cls, item_id):
        item = cls.query.get(item_id)
        if item is None:
            raise exceptions.NotExist(f'Could not find a {__class__.__name__} wit id {item_id}')
        return item

    @classmethod
    def close_session(cls):
        db.session.remove()

    def save_db(self):
        db.session.add(self)
        db.session.commit()

    def prepare_save(self):
        db.session.add(self)
        db.session.flush()

    def delete_db(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except exc.IntegrityError as ex:
            db.session.rollback()
            raise exceptions.RepositoryError(ex)

    def update_from_json(self, json_data):
        try:
            self.set_values(json_data)
            self.save_db()
            return self
        except exc.IntegrityError as ex:
            db.session.rollback()
            raise exceptions.RepositoryError(ex)

    def set_values(self, json_data):
        for key, value in json_data.items():
            setattr(self, key, json_data.get(key, getattr(self, key)))


class AuditMixin(object):
    @declarative.declared_attr
    def created_at(cls):
        return db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @declarative.declared_attr
    def updated_at(cls):
        return db.Column(db.DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)


class ChessBoard(db.Model, AuditMixin, AbstractModel):
    __tablename__ = 'teste_chessboard'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    positions = db.Column(postgresql.JSONB, nullable=False)


class Piece(db.Model, AuditMixin, AbstractModel):
    __tablename__ = 'teste_pieces'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    color = db.Column(db.String, nullable=True)
    type = db.Column(db.String, nullable=True)
