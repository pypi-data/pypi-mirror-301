import random
from typing import Any, Dict, Generic, List, Optional, TypeVar, cast

import pandas as pd
from supamodel.abstract.core import BaseModel, EntityModel
from supamodel.abstract.data import Data

DataT = TypeVar("DataT", bound="Data")
InputModelT = TypeVar("InputModelT", "BaseModel", "Data")
DataAny = DataT | Any


class Dataset(EntityModel, Generic[DataT]):
    # model_config = ConfigDict(
    #     from_attributes=True, arbitrary_types_allowed=True, ignored_types=[]
    # )
    # I'm now forcing the data to be a list of DataT
    # This is a breaking change. Luckily it's not used anywhere yet.
    data: Optional[List[DataT]] = []
    message: Optional[str] = None
    error: Optional[str] = None

    @property
    def is_list(self) -> bool:
        return isinstance(self.data, list)

    @property
    def is_dict(self) -> bool:
        return isinstance(self.data, dict)

    @property
    def is_base_model(self) -> bool:
        return isinstance(self.data, BaseModel)

    def sample(self) -> DataT:
        """
        Selects and returns a random item from the data.

        If the data is a list, a random item from the list is returned.
        If the data is a dictionary, a random item from the dictionary values is returned.
        If the data is neither a list nor a dictionary, the data itself is returned.

        Returns:
            Any: A random item from the data.
        """
        if self.is_list:
            return random.choice(self.data)
        return self.data

    # Add iterator methods if the data is a list
    def __iter__(self):
        if self.is_list:
            return iter(self.data)
        return iter([])

    def __getitem__(self, item):
        if self.is_list or self.is_dict:
            return self.data[item]
        return None

    def __len__(self):
        if self.is_list:
            return len(self.data)
        return 0

    def __contains__(self, item):
        if self.is_list:
            return item in self.data
        return False

    def empty(self) -> bool:
        if self.is_list:
            return len(self.data) == 0
        return True

    def to_dict(self) -> Dict[str, DataT] | List[DataT | Any] | Any:
        if self.is_list:
            self.data = cast(List[DataT], self.data)
            return [item.model_dump(by_alias=True, mode="json") for item in self.data]
        elif self.is_dict:
            return self.data
        elif self.is_base_model:
            return self.data.model_dump(by_alias=True, mode="json")
        return self.data

    def to_df(self) -> Any:
        if self.empty():
            return pd.DataFrame([])

        dataset_list = self.to_dict()
        if not isinstance(dataset_list, list):
            dataset_list = [dataset_list]
        return pd.DataFrame(dataset_list)
