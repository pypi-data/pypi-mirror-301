"""Module containing the requirement class."""
from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Union

__all__ = ["ConnectionRequirement", "ModelRequirement"]


class RequirementBase(ABC):
    """Simple class containing the requirement properties."""

    def __init__(self, attribute_name: str,
                 submodel_types: type | tuple[type, ...],
                 description: str | None = None,
                 hard: bool = True,
                 full_name: str | None = None,
                 type_name: str | None = None) -> None:
        """Initialize a new instance of the requirement.

        Parameters
        ----------
        attribute_name : str
            Name of the attribute that is used to store the object in the parent.
        submodel_types : type | tuple[type, ...]
            Supported types of the object.
        description : str, optional
            Description of the object, by default None.
        hard : bool, optional
            Whether the requirement is hard, i.e. the requirement should be satisfied
            for the model to be defined, by default True.
        full_name : str, optional
            Full name of the object, by default capitalized version of the attribute
            name, where the underscores are replaced by spaces.
        type_name : str, optional
            Names of the supported types of the object. The names of the type classes
            are used by default.
        """
        attribute_name = str(attribute_name)
        if not attribute_name.isidentifier():
            raise ValueError(f"'{attribute_name}' is not a valid attribute name, "
                             f"because it cannot be used as a variable name.")
        self._attribute_name = attribute_name
        if not isinstance(submodel_types, Iterable):
            submodel_types = (submodel_types,)
        self._types = tuple(submodel_types)
        if description is None:
            description = self.types[0].__doc__.split("\n", 1)[0]
        self._description = str(description)
        self._hard = bool(hard)
        if full_name is None:
            full_name = self.attribute_name.replace("_", " ").capitalize()
        self._full_name = str(full_name)
        if type_name is None:
            type_name = " or ".join(tp.__name__ for tp in self.types)
        self._type_name = str(type_name)

    @property
    def attribute_name(self) -> str:
        """Name of the attribute that is used to store the object in the parent."""
        return self._attribute_name

    @property
    def types(self) -> tuple[type, ...]:
        """Supported types of the submodel."""
        return self._types

    @property
    def description(self) -> str:
        """Description of the object."""
        return self._description

    @property
    def hard(self) -> bool:
        """Boolean whether the requirement is a hard requirement."""
        return self._hard

    @property
    def full_name(self) -> str:
        """Full name of the object."""
        return self._full_name

    @property
    def type_name(self) -> str:
        """Names of the supported types of the submodel."""
        return self._type_name

    @property
    def type_hint(self) -> type:
        """Type hint for the submodel."""
        return Union[self.types]

    def __str__(self) -> str:
        return self.attribute_name

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}(attribute_name={self.attribute_name!r}, "
                f"types={self.types!r}, description={self.description!r}, "
                f"full_name={self.full_name!r}, type_name={self.type_name!r})")

    @abstractmethod
    def is_satisfied_by(self, obj: object | type) -> bool:
        """Check whether the object satisfies the requirement.

        Parameters
        ----------
        obj : object
            Object to check.

        Returns
        -------
        bool
            Whether the object satisfies the requirement.
        """


class ModelRequirement(RequirementBase):
    """Class representing a requirement for a submodel."""

    def is_satisfied_by(self, submodel: object | type) -> bool:
        """Check whether the submodel satisfies the requirement.

        Parameters
        ----------
        submodel : Model | type
            Submodel to check.

        Returns
        -------
        bool
            Whether the submodel satisfies the requirement.
        """
        return isinstance(submodel, self.types) or issubclass(submodel, self.types)


class ConnectionRequirement(RequirementBase):
    """Class representing a requirement for a connection."""

    def is_satisfied_by(self, connection: object | type) -> bool:
        """Check whether the connection satisfies the requirement.

        Parameters
        ----------
        connection : Connection
            Connection to check.

        Returns
        -------
        bool
            Whether the connection satisfies the requirement.
        """
        return isinstance(connection, self.types) or issubclass(connection, self.types)
