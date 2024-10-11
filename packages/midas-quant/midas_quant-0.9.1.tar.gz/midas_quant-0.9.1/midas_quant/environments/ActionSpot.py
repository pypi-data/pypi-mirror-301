from enum import Enum


class ActionSpot(Enum):
    BUY = 0    # Action to purchase the stock or asset
    SELL = 1   # Action to sell the stock or asset
    HOLD = 2   # Action to maintain the current position without buying or selling
    CUT = 3    # Action to reduce the position, possibly to minimize losses
    PLUS = 4   # Action to increase the position, potentially to capitalize on gains

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    @classmethod
    def _missing_(cls, value):
        """
        Override the _missing_ method to handle string inputs.
        This allows instantiation using the member name as a string.
        If the value does not correspond to any member, return HOLD.
        
        Args:
            value: The value used to instantiate the Enum.
        
        Returns:
            The corresponding Enum member if a match is found, otherwise ActionSpot.HOLD.
        """
        if isinstance(value, str):
            try:
                # Attempt to return the member matching the provided name (case-insensitive)
                return cls[value.upper()]
            except KeyError:
                # If no matching member is found, return HOLD
                return cls.HOLD
        # If not a string, defer to the superclass implementation
        return super()._missing_(value)
