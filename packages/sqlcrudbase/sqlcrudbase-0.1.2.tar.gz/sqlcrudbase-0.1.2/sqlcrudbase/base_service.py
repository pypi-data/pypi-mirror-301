from .base_repository import BaseRepository


class BaseService:
    """
    A generic service that provides CRUD operations for a database entity.
    
    Args:
        entity (Model): A Peewee model that represents the database entity.
    """
    def __init__(self, entity):
        self.repository = BaseRepository(entity)

    def get_all(self):
        models = list(self.repository.get_all())
        return [model.__data__ for model in models]

    def get_by_id(self, id: int):
        return self.repository.get_by_id(id)

    def create(self, model: dict):
        return self.repository.create(model)

    def update(self, model: dict):
        existing = self.get_by_id(model["id"])

        if existing is None:
            return None

        for key, value in model.items():
            existing.__data__[key] = value

        existing.save()
        return existing

    def delete(self, id: int):
        return self.repository.delete(id)
