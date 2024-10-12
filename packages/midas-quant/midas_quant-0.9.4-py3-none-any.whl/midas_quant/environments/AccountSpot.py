import pandas as pd
from ..feed.PandasPart import PandasPart

class AccountSpot:
    """
    Represents a trading account for managing spot transactions, including buying and selling assets.

    Attributes:
        _code (str): Unique identifier for the account.
        _name (str): Name associated with the account.
        _fee (float): Transaction fee percentage (e.g., 0.015 for 0.015%).
        _tax (float): Transaction tax percentage (e.g., 0.38 for 0.38%).
        _balance (int): Current cash balance available for trading.
        _account_price (int): Total value of the account (cash + value of held assets).
        _quantity (int): Total number of asset units currently held.
        _invested (int): Total amount invested in purchasing assets.
        _average_price (int): Average price per asset unit based on investments.
        _history_asset (pd.DataFrame): DataFrame tracking the history of account assets.
        _history_trade (pd.DataFrame): DataFrame tracking the history of executed trades.
    """

    def __init__(self, code: str, name: str, balance: int = 1_000_000, fee: float = 0.015, tax: float = 0.38) -> None:
        """
        Initializes a new SpotAccount instance.

        Args:
            code (str): Unique identifier for the account.
            name (str): Name associated with the account.
            balance (int, optional): Initial cash balance. Defaults to 1,000,000.
            fee (float, optional): Transaction fee percentage. Defaults to 0.015 (1.5%).
            tax (float, optional): Transaction tax percentage. Defaults to 0.38 (38%).
        """
        self._code = code
        self._name = name
        self._fee = fee / 100   # Convert percentage to decimal (e.g., 0.015% becomes 0.00015)
        self._tax = tax / 100   # Convert percentage to decimal (e.g., 0.38% becomes 0.0038)
        
        self._balance = balance        # Current cash balance
        self._account_price = 0        # Total account value (cash + assets)
        
        self._quantity = 0             # Number of asset units held
        self._invested = 0             # Total amount invested in assets
        self._average_price = 0        # Average price per asset unit
        
        # DataFrame to track asset history
        self._history_asset = pd.DataFrame(columns=[
            "reg_day", "balance", "quantity", "average_price", "invested", "account"
        ])
        
        # DataFrame to track trade history
        self._history_trade = pd.DataFrame(columns=[
            "reg_day", "action", "price", "quantity", "fee", "tax", "net_price", "rate"
        ])

    def getCode(self) -> str:
        """
        Retrieves the account's unique identifier code.

        Returns:
            str: The account code.
        """
        return self._code

    def getName(self) -> str:
        """
        Retrieves the account's name.

        Returns:
            str: The account name.
        """
        return self._name

    def getHistory(self) -> tuple[PandasPart, PandasPart]:
        """
        Retrieves the historical records of account assets and trades.

        Returns:
            tuple[PandasPart, PandasPart]: 
                - Asset history processed by PandasPart.
                - Trade history processed by PandasPart.
        """
        asset = PandasPart(self._history_asset, backword=True)
        trade = PandasPart(self._history_trade, backword=True)
        
        return asset, trade

    def calcMaxBuy(self, price: int) -> int:
        """
        Calculates the maximum number of asset units that can be purchased with the current balance at the given price.

        Args:
            price (int): Price per asset unit.

        Returns:
            int: Maximum number of units that can be bought.
        """
        return self._balance // price

    def calcMaxSell(self) -> int:
        """
        Calculates the maximum number of asset units that can be sold based on current holdings.

        Returns:
            int: Maximum number of units available for sale.
        """
        return self._quantity

    def hold(self, reg_day: str, price: int) -> None:
        """
        Updates the account's total value based on the current price and quantity held,
        and records the current state in the asset history.

        Args:
            reg_day (str): Date of the record.
            price (int): Current price per asset unit.
        """
        self._account_price = price * self._quantity + self._balance
        self._average_price = 0 if self._quantity == 0 else int(self._invested / self._quantity)
        
        self._history_asset.loc[len(self._history_asset)] = {
            "reg_day": reg_day,
            "balance": self._balance,
            "quantity": self._quantity,
            "average_price": self._average_price,
            "invested": self._invested,
            "account": self._account_price
        }

    def buy(self, reg_day: str, price: int, quantity: int) -> None:
        """
        Executes a purchase of a specified quantity of assets at a given price,
        updates account balances, and records the trade.

        Args:
            reg_day (str): Date of the trade.
            price (int): Price per asset unit.
            quantity (int): Number of asset units to buy.
        """
        if quantity > 0:
            invested = int(price * quantity)  # Total cost for purchasing assets
            buy_fee = int(invested * self._fee)  # Transaction fee for buying
            total_invested = invested + buy_fee  # Total investment including fees
            rate = round(total_invested / self._balance * 100, 2)  # Percentage of balance used
            
            self._quantity += quantity
            self._invested += total_invested
            self._balance -= total_invested
        
            self._history_trade.loc[len(self._history_trade)] = {
                "reg_day": reg_day,
                "action": "buy",
                "price": price,
                "quantity": quantity,
                "fee": buy_fee,
                "tax": 0,
                "net_price": total_invested,
                "rate": rate,
            }
        self.hold(reg_day, price)

    def sell(self, reg_day: str, price: int, quantity: int) -> None:
        """
        Executes a sale of a specified quantity of assets at a given price,
        updates account balances, and records the trade.

        Args:
            reg_day (str): Date of the trade.
            price (int): Price per asset unit.
            quantity (int): Number of asset units to sell.
        """
        if quantity > 0:
            gross = int(price * quantity)  # Total revenue from selling assets
            sell_fee = int(gross * self._fee)  # Transaction fee for selling
            sell_tax = int(gross * self._tax)  # Transaction tax for selling
            net_revenue = gross - sell_fee - sell_tax  # Net revenue after fees and taxes
            rate = round(quantity / self._quantity * 100, 2)  # Percentage of holdings sold
        
            average_invested = int(self._invested / self._quantity) if self._quantity > 0 else 0
            self._invested -= average_invested * quantity
            self._quantity -= quantity
            self._balance += net_revenue
            
            self._history_trade.loc[len(self._history_trade)] = {
                "reg_day": reg_day,
                "action": "sell",
                "price": price,
                "quantity": quantity,
                "fee": sell_fee,
                "tax": sell_tax,
                "net_price": net_revenue,
                "rate": rate,
            }
        self.hold(reg_day, price)
