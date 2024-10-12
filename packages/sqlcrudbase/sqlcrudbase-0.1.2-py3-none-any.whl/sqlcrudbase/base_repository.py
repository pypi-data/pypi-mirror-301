class BaseRepository:
    """
    A generic repository that provides CRUD operations for a database entity.
    
    Args:
        entity (Model): A Peewee model that represents the database entity.
    """
    def __init__(self, entity):
        self.entity = entity

    def get_all(self):
        return list(self.entity.select())

    def get_by_id(self, id: int):
        try:
            return self.entity.get(self.entity.id == id)
        except self.entity.DoesNotExist:
            return None

    def create(self, model: dict):
        return self.entity.create(**model)

    def delete(self, id: int) -> bool:
        query = self.entity.delete().where(self.entity.id == id)
        return query.execute() > 0
