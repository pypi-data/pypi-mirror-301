"""
# Abstract Base Classes

This module contains the abstract base classes for the supamodel package. These classes will help define the core functionality and structure of the models used in the package.

The primary abstract base classes defined in this module are:

* `BaseModel`: An abstract base class for Pydantic models that provides additional functionality and customization options.
* `OrmModel`: An abstract base class for models that interact with databases using an an existing ORM if necessary.
* `Data`: An abstract base class for data models that can handle dynamic fields and aliasing. This class is designed to be flexible and accommodate various data structures between systems.
* `Singleton`: An abstract base class for creating singleton classes that ensure only one instance of the class is created. We work to ensure that the class is thread-safe and can be used in a multi-threaded environment.
* `SupaModel`: An abstract base class for models that interact with Supabase using the Supabase API. This class provides a consistent interface for interacting with Supabase and handling errors.

These abstract base classes provide a foundation for the models used in the supamodel package, ensuring consistency, flexibility, and extensibility across different types of models.


"""

from functools import cached_property
from typing import Dict

from pydantic import BaseModel as _BaseModel, ConfigDict, alias_generators
from supamodel.utils import cached_classattr

#


class BaseModel(_BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        extra="allow",
        populate_by_name=True,
        ignored_types=(cached_property, cached_classattr),
    )

    def none_dump(self) -> Dict:
        """Return the model's data in a dictionary format without incuding None values.

        Returns:
            Dict: A dict with the model's data without None values.
        """
        return self.model_dump(exclude_none=True)

    def supa_dump(self, by_alias: bool = False) -> Dict:
        """Supabase serialization dump.

        Args:
            by_alias (bool, optional): Option to use aliases. Defaults to False.

        Returns:
            Dict: The response in a dictionary format.
        """
        return self.model_dump(exclude_none=True, mode="json", by_alias=by_alias)


class IgnoreModel(BaseModel):
    model_config = ConfigDict(extra="ignore")


class CamelModel(IgnoreModel):
    model_config = ConfigDict(alias_generator=alias_generators.to_camel)


class EntityModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        ignored_types=(cached_property, cached_classattr),
        arbitrary_types_allowed=True,
    )
