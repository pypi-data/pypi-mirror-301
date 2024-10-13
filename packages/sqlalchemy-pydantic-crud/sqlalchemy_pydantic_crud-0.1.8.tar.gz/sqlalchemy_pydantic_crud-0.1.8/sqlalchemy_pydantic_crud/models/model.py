from sqlalchemy.orm import ColumnProperty, class_mapper, DeclarativeBase


class ModelMixin:
    def to_dict(self):
        """Return a dictionary representation of the model instance.

        This method converts the model instance to a dictionary where the keys
        are the column names and the values are the corresponding attribute values.
        This can be useful for serializing tests_models to JSON or other formats.

        Returns:
            dict: A dictionary representation of the model instance.
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def from_dict(cls, data):
        """
        Creates a new instance of the model from a dictionary of attributes.

        Args:
            data (dict): A dictionary containing the attributes and values for the new instance.

        Returns:
            An instance of the model with the provided attributes.
        """
        return cls(**data)

    @classmethod
    def attribute_names(cls) -> set:
        return set(
            prop.key
            for prop in class_mapper(cls).iterate_properties
            if isinstance(prop, ColumnProperty)
        )




class DbBaseModel(DeclarativeBase, ModelMixin):
    __abstract__ = True

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.to_dict()}>"

    @classmethod
    def attribute_names(cls) -> set:
        return set(
            prop.key
            for prop in class_mapper(cls).iterate_properties
            if isinstance(prop, ColumnProperty)
        )
