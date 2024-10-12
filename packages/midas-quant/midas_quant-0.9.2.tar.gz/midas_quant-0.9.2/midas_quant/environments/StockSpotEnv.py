from .TradeEnv import TradeEnv
from .AccountSpot import AccountSpot
from .ActionSpot import ActionSpot
from enum import Enum
from typing import Callable
from ..feed import IFeeder


class StockSpotEnv(TradeEnv):
    """
    A specialized trading environment for stock spot trading, inheriting from TradeEnv.

    This environment is tailored for handling stock spot transactions, utilizing the 
    AccountSpot class for account management and ActionSpot enum for defining trading actions.
    It integrates with a market data feeder to simulate real-time trading scenarios.

    Attributes:
        Inherits all attributes from the TradeEnv base class.
    """

    def __init__(
        self,
        feeder: IFeeder,
        balance: int = 1_000_000,
        quantity: int = 10,
        fee: float = 0.015,
        tax: float = 0.38
    ):
        """
        Initializes the StockSpotEnv environment with specific parameters for stock trading.

        Args:
            feeder (IFeeder): An instance that provides market data and manages the data feed.
            balance (int, optional): The initial cash balance available for trading. Defaults to 1,000,000.
            quantity (int, optional): The default quantity of assets to buy per transaction. Defaults to 10.
            fee (float, optional): The transaction fee percentage applied to each trade. Defaults to 0.015.
            tax (float, optional): The transaction tax percentage applied to each sale. Defaults to 0.38.
        """
        super(StockSpotEnv, self).__init__(feeder, AccountSpot, ActionSpot, balance, quantity, fee, tax)
    
    def _act(self, action, rate, obs, feed_change):
        """
        Executes the specified trading action within the environment.

        Depending on the action (BUY, SELL, CUT, PLUS, HOLD), this method interacts with the 
        AccountSpot instance to perform the corresponding trade operation.

        Args:
            action (ActionSpot): The action to be taken, as defined in the ActionSpot enum.
            rate (float): An additional parameter that may influence the action, typically representing 
                the rate or proportion for CUT and PLUS actions.
            obs (np.ndarray): The current observation array containing market data.
            feed_change (object): Information about changes in the data feed.
        """
        # Extract relevant market data from the observation
        daytime = obs[0][self._feeder.col_daytime()]  # Current datetime from the observation
        price = obs[0][self._feeder.col_price()]      # Current price from the observation
        
        if action == ActionSpot.BUY:
            quantity = self._account.calcMaxBuy(price)
            self._account.buy(daytime, price, self._buy_quantity)
        
        elif action == ActionSpot.SELL:
            quantity = self._account.calcMaxSell()
            self._account.sell(daytime, price, quantity)
        
        elif action == ActionSpot.CUT:
            quantity = int(self._account.calcMaxSell() * (rate / 100))
            self._account.sell(daytime, price, quantity)
        
        elif action == ActionSpot.PLUS:
            quantity = int(self._buy_quantity * (rate / 100))
            self._account.buy(daytime, price, quantity)
        
        else:  # ActionSpot.HOLD
            self._account.hold(daytime, price)
    
    def _reward(self, action, rate, obs, feed_change, asset, trade):
        """
        Calculates the reward for the given action and state transition.

        The reward is computed based on the change in the account's total value before and after the action.

        Args:
            action (ActionSpot): The action taken.
            rate (float): An additional parameter that may influence the reward.
            obs (np.ndarray): The current observation array after the action.
            feed_change (object): Information about changes in the data feed after the action.
            asset (object or None): The latest asset history record.
            trade (object or None): The latest trade history record.

        Returns:
            float: The calculated reward, representing the relative change in account value.
        """
        price = obs[0][self._feeder.col_price()]
        quantity = asset.quantity
        account_prev = asset.account
        account = quantity * price + self._account._balance  # Assuming _balance is updated
        
        # Compute the reward as the relative change in account value
        # (New account value - Previous account value) / Previous account value
        reward = (account - account_prev) / account_prev * 100
        
        return reward
