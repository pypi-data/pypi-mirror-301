from .IFeeder import IFeeder
from .IFeedPart import IFeedPart
from .PandasPart import PandasPart
from typing import List, Tuple, Optional, Type, TypeVar, Generic, Union
import pandas as pd

# Define a generic type variable bound to IFeedPart
T = TypeVar('T', bound=IFeedPart)

class PandasFeeder(IFeeder, Generic[T]):
    """
    Feeder class that iterates over a list of Pandas DataFrames, providing windowed segments 
    of each DataFrame as defined by the window size. Supports both backward and forward indexing, 
    utilizing a specified part class (default: IFeedPart) to manage each windowed segment.

    Implements the IFeeder interface, adhering to required methods and behaviors.

    Attributes:
        _dfs (List[pd.DataFrame]): List of DataFrames to iterate over.
        _window (int): Number of rows per windowed segment.
        _backword (bool): Determines direction of indexing (True for backward, False for forward).
        _part_class (Type[T]): Class used to manage each windowed DataFrame segment.
        _col_daytime (str): Name of the column representing date or time.
        _col_price (str): Name of the column representing price.
        _infos (List[dict]): Additional information for each DataFrame.

        _dfs_index (int): Current index in the list of DataFrames.
        _dfs_size (int): Total number of DataFrames.
        _df (pd.DataFrame): The current DataFrame being processed.
        _df_index (int): Current row index within the DataFrame.
        _df_size (int): Total number of rows in the current DataFrame.
        _size_item (int): Total number of windowed segments across all DataFrames.
    """

    def __init__(
        self, 
        dfs: List[pd.DataFrame], 
        window: int = 5, 
        backword: bool = True, 
        part_class: Type[T] = PandasPart,
        col_daytime: str = "reg_day",
        col_price: str = "price",
        infos: List[dict] = None
    ) -> None:
        """
        Initializes the PandasFeeder with a list of DataFrames, window size, indexing direction,
        and the part class for handling segments.

        Args:
            dfs (List[pd.DataFrame]): List of DataFrames to be processed.
            window (int, optional): Size of each window (number of rows). Defaults to 5.
            backword (bool, optional): Direction of indexing (True for backward, False for forward). Defaults to True.
            part_class (Type[T], optional): Class used to handle each windowed segment. Defaults to IFeedPart.
            col_daytime (str): Column representing date or time.
            col_price (str): Column representing price.
            infos (List[dict], optional): Extra information for each DataFrame.
        """
        self._dfs: List[pd.DataFrame] = dfs
        self._window: int = window
        self._backword: bool = backword
        self._part_class: Type[T] = part_class
        self._col_daytime: str = col_daytime
        self._col_price: str = col_price
        self._infos: List[dict] = infos
        
        self._dfs_index: int = 0
        self._dfs_size: int = len(dfs)
        self._df: pd.DataFrame = dfs[self._dfs_index] if self._dfs_size > 0 else pd.DataFrame()
        self._df_index: int = window
        self._df_size: int = len(self._df)

        # Calculate total number of windowed segments across all DataFrames
        self._size_item: int = sum(max(len(df) - window + 1, 0) for df in dfs)

    def col_daytime(self) -> str:
        """
        Retrieves the name of the column representing date or time.

        Returns:
            str: The column name.
        """
        return self._col_daytime

    def col_price(self) -> str:
        """
        Retrieves the name of the column representing price.

        Returns:
            str: The column name.
        """
        return self._col_price

    def infos(self) -> Optional[List[dict]]:
        """
        Returns the list of extra information dictionaries, if available.

        Returns:
            Optional[List[dict]]: List of info dictionaries or None if not provided.
        """
        return self._infos

    def info(self) -> Optional[dict]:
        """
        Returns the current info dictionary for the active DataFrame, if available.

        Returns:
            Optional[dict]: The current info dictionary or None if not applicable.
        """
        if self._infos and len(self._infos) == len(self._dfs):
            return self._infos[self._dfs_index]
        return None

    def datas(self) -> List[pd.DataFrame]:
        """
        Retrieves the list of all DataFrames managed by the feeder.

        Returns:
            List[pd.DataFrame]: The list of DataFrames.
        """
        return self._dfs

    def data(self) -> pd.DataFrame:
        """
        Retrieves the current active DataFrame.

        Returns:
            pd.DataFrame: The current DataFrame.
        """
        return self._dfs[self._dfs_index]

    def dataPrevious(self) -> pd.DataFrame:
        """
        Retrieves the previous DataFrame.

        Returns:
            pd.DataFrame: The previous DataFrame.
        """
        return self._dfs[self._dfs_index - 1]

    def shape(self) -> Tuple[int, int]:
        """
        Returns the shape of the current DataFrame (rows, columns).

        Returns:
            Tuple[int, int]: The shape of the current DataFrame.
        """
        return self.data().shape

    def partShape(self) -> Tuple[int, int]:
        """
        Returns the shape of the current windowed segment (rows, columns).

        Returns:
            Tuple[int, int]: The shape of the windowed segment.
        """
        return (self._window, self.data().shape[1])

    def __iter__(self) -> 'PandasFeeder[T]':
        """
        Resets the feeder to the initial state and returns the iterator object.

        Returns:
            PandasFeeder[T]: The iterator object.
        """
        self._dfs_index = 0
        self._df = self._dfs[self._dfs_index] if self._dfs_size > 0 else pd.DataFrame()
        self._df_index = self._window
        self._df_size = len(self._df)
        return self

    def __len__(self) -> int:
        """
        Retrieves the total number of windowed segments across all DataFrames.

        Returns:
            int: The total number of segments.
        """
        return self._size_item

    def __next__(self) -> Tuple[T, bool]:
        """
        Retrieves the next windowed segment and whether a DataFrame change occurred.

        Returns:
            Tuple[T, bool]: 
                - T: Instance of the part_class containing the windowed DataFrame segment.
                - bool: True if feeder has moved to a new DataFrame, False otherwise.

        Raises:
            StopIteration: If all DataFrames have been processed.
        """
        is_change: bool = False

        if self._df_index > self._df_size:
            self._dfs_index += 1
            if self._dfs_index >= self._dfs_size:
                raise StopIteration
            self._df = self._dfs[self._dfs_index]
            self._df_index = self._window
            self._df_size = len(self._df)
            is_change = True

        if self._df_index - self._window < 0 or self._df_index > self._df_size:
            raise StopIteration

        df_part: pd.DataFrame = self._df.iloc[self._df_index - self._window : self._df_index].reset_index(drop=True)
        part: T = self._part_class(df_part, self._backword)
        self._df_index += 1

        return part, is_change

    def reset(self) -> None:
        """
        Resets the feeder to its initial state, restarting iteration from the beginning.
        """
        self.__iter__()

    def next(self) -> Tuple[Optional[T], Optional[bool]]:
        """
        Safely retrieves the next windowed segment, returning None if iteration is complete.

        Returns:
            Tuple[Optional[T], Optional[bool]]: 
                - Optional[T]: The next windowed segment or None if complete.
                - Optional[bool]: True if DataFrame changed, False if not, or None if complete.
        """
        try:
            return self.__next__()
        except StopIteration:
            return None, None
