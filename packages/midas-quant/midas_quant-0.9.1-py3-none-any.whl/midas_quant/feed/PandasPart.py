from .IFeedPart import IFeedPart
from typing import Union, List
import pandas as pd


class PandasPart(IFeedPart):
    """
    Provides an enhanced interface to a Pandas DataFrame, supporting backward or forward indexing,
    value comparisons, and detection of cross events between DataFrame columns. This class 
    facilitates flexible data manipulation and analysis by allowing integer and slice-based 
    indexing in both backward and forward directions, along with utility methods for 
    value comparisons and cross-event detections.

    Attributes:
        _df (pd.DataFrame): The underlying Pandas DataFrame being managed.
        _size (int): The number of rows present in the DataFrame.
        _backword (bool): Defines the indexing direction (True for backward, False for forward).
        columns (List[str]): A list of column names in the DataFrame.
    """

    def __init__(self, df: pd.DataFrame, backword: bool = True) -> None:
        """
        Initializes the PandasPart with a given DataFrame and the preferred indexing direction.

        Args:
            df (pd.DataFrame): The Pandas DataFrame to be managed.
            backword (bool, optional): Flag indicating the indexing direction (True for backward, 
                                       False for forward). Defaults to True.
        """
        self._df: pd.DataFrame = df
        self._size: int = len(df)
        self._backword: bool = backword
        self.columns = df.columns.tolist()

    def addColumn(self, col, value):
        self._df[col] = value

    def isBackword(self) -> bool:
        """
        Indicates whether the current indexing mode is set to backward.

        Returns:
            bool: True if backward indexing is active, False otherwise.
        """
        return self._backword

    def _repr_html_(self) -> str:
        """
        Generates the HTML representation of the DataFrame for display in Jupyter notebooks.

        Returns:
            str: HTML string representation of the DataFrame.
        """
        return self._df.to_html()

    def __repr__(self) -> str:
        """
        Produces the string representation of the DataFrame for console output.

        Returns:
            str: String representation of the DataFrame.
        """
        return repr(self._df)

    def __len__(self) -> int:
        """
        Returns the number of rows in the DataFrame.

        Returns:
            int: The number of rows in the DataFrame.
        """
        return self._size

    def __getitem__(self, index: Union[int, slice, str]) -> Union[pd.Series, 'PandasPart']:
        """
        Supports row or column access using integer, slice, or string-based indexing.

        Args:
            index (Union[int, slice, str]): 
                - int: Retrieve a single row as a Series.
                - slice: Retrieve multiple rows as a new PandasPart instance.
                - str: Retrieve a single column as a Series.

        Returns:
            Union[pd.Series, PandasPart]: 
                - pd.Series: When accessing a single row or column.
                - PandasPart: When slicing rows.

        Raises:
            TypeError: If the provided index is of an unsupported type.
            AssertionError: If an integer index exceeds the DataFrame's row count.
        """
        if isinstance(index, int):
            assert index < self._size, f"Index must be smaller than {self._size}"
            position: int = -(index + 1) if self._backword else index
            return self._df.iloc[position]

        elif isinstance(index, slice):
            start, stop, step = index.indices(self._size)
            indices: range = range(start, stop, step)

            if self._backword:
                positions: List[int] = [self._size - idx - 1 for idx in indices]
                if step > 0:
                    positions = positions[::-1]
            else:
                positions = list(indices)

            sliced_df: pd.DataFrame = self._df.iloc[positions].reset_index(drop=True)
            return PandasPart(sliced_df, self._backword)

        elif isinstance(index, str):
            return self._df[index]

        elif isinstance(index, tuple):
            return self._df[list(index)]

        else:
            raise TypeError(f"Invalid index type: {type(index)}. Supported types are int, slice, and str.")

    def upCompare(self, index: int, target: str, compare: str) -> bool:
        """
        Determines if the value in the target column is greater than the value in the compare column at the specified index.

        Args:
            index (int): The row index for comparison.
            target (str): The target column for comparison.
            compare (str): The column to compare against.

        Returns:
            bool: True if target column value > compare column value, False otherwise.
        """
        return self[index][target] > self[index][compare]

    def downCompare(self, index: int, target: str, compare: str) -> bool:
        """
        Determines if the value in the target column is less than the value in the compare column at the specified index.

        Args:
            index (int): The row index for comparison.
            target (str): The target column for comparison.
            compare (str): The column to compare against.

        Returns:
            bool: True if target column value < compare column value, False otherwise.
        """
        return self[index][target] < self[index][compare]

    def upValue(self, index: int, target: str, value: float) -> bool:
        """
        Checks if the value in the target column is greater than a specified value at the given index.

        Args:
            index (int): The row index for comparison.
            target (str): The target column for comparison.
            value (float): The reference value for comparison.

        Returns:
            bool: True if target column value > the specified value, False otherwise.
        """
        return self[index][target] > value

    def downValue(self, index: int, target: str, value: float) -> bool:
        """
        Checks if the value in the target column is less than a specified value at the given index.

        Args:
            index (int): The row index for comparison.
            target (str): The target column for comparison.
            value (float): The reference value for comparison.

        Returns:
            bool: True if target column value < the specified value, False otherwise.
        """
        return self[index][target] < value

    def betweenValue(self, index: int, target: str, value: float, percent: float = 1.0) -> bool:
        """
        Checks if the value in the target column is within a specified percentage range around the given value.

        Args:
            index (int): The row index for comparison.
            target (str): The target column for comparison.
            value (float): The reference value for comparison.
            percent (float, optional): The percentage range for comparison. Defaults to 1.0.

        Returns:
            bool: True if the target column value is within the range, False otherwise.
        """
        percent_value: float = value * (percent / 100)
        upper_bound: float = value + percent_value
        lower_bound: float = value - percent_value

        target_value: float = self[index][target]
        return lower_bound < target_value < upper_bound

    def betweenCompare(self, index: int, target: str, compare: str, percent: float) -> bool:
        """
        Checks if both the target and compare column values are within a specified percentage range of each other.

        Args:
            index (int): The row index for comparison.
            target (str): The target column for comparison.
            compare (str): The column to compare against.
            percent (float): The percentage range for comparison.

        Returns:
            bool: True if both values are within the percentage range, False otherwise.
        """
        target_value: float = self[index][target]
        percent_value: float = target_value * (percent / 100)
        upper_bound: float = target_value + percent_value
        lower_bound: float = target_value - percent_value

        compare_value: float = self[index][compare]

        return lower_bound < compare_value < upper_bound and lower_bound < target_value < upper_bound

    def equalValue(self, index: int, target: str, value: float) -> bool:
        """
        Checks if the value in the target column is equal to the specified value at the given index.

        Args:
            index (int): The row index for comparison.
            target (str): The target column for comparison.
            value (float): The value to compare against.

        Returns:
            bool: True if the value in the target column equals the specified value, False otherwise.
        """
        return self[index][target] == value

    def equalCompare(self, index: int, target: str, compare: str) -> bool:
        """
        Checks if the values in the target and compare columns are equal at the specified index.

        Args:
            index (int): The row index for comparison.
            target (str): The target column for comparison.
            compare (str): The column to compare against.

        Returns:
            bool: True if both values are equal, False otherwise.
        """
        return self[index][target] == self[index][compare]
    
    def cross(self, index: int, target: str, compare: str, updn: str = "up") -> bool:
        """
        Detects if a 'cross' event occurs between the target and compare columns at the specified index.
        A 'cross' event is when the target column crosses above or below the compare column.

        Args:
            index (int): The row index for the cross event detection.
            target (str): The target column for comparison.
            compare (str): The column to compare against.
            updn (str, optional): The direction of the cross event ("up" for upward cross, "down" for downward cross). 
                                  Defaults to "up".

        Returns:
            bool: True if the specified cross event occurs, False otherwise.

        Raises:
            AssertionError: If the index is out of bounds for the current indexing direction.
            ValueError: If the 'updn' parameter is not "up" or "down".
        """
        if self._backword:
            assert index < self._size - 1, f"Index must be smaller than {self._size - 1} for backward indexing."
        else:
            assert index > 0, f"Index must be greater than 0 for forward indexing."

        previous_index: int = index + 1 if self._backword else index - 1

        if updn == "up":
            return (
                self[previous_index][target] <= self[previous_index][compare] and
                self[index][target] > self[index][compare]
            )
        elif updn == "down":
            return (
                self[previous_index][target] >= self[previous_index][compare] and
                self[index][target] < self[index][compare]
            )
        else:
            raise ValueError("Parameter 'updn' must be either 'up' or 'down'.")
