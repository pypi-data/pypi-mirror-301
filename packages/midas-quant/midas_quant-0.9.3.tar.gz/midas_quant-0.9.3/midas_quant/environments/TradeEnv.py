from ..feed import IFeeder, IFeedPart
from .plot import showGraph
import numpy as np
import pandas as pd
from enum import Enum
from danbi import DotDict
import gymnasium as gym
from abc import ABC, abstractmethod
from typing import Callable, Optional, Dict, Any, Tuple


class TradeEnv(gym.Env, ABC):
    """
    Custom OpenAI Gym environment for simulating spot market trading.

    This environment simulates trading strategies by interacting with market data, managing 
    an account's balance, and executing buy/sell actions. It uses a data feeder for market data 
    and an account management system for handling transactions.

    Attributes:
        _feeder (IFeeder): Feeder for providing market data.
        _account_class (Callable): Callable for managing the trading account.
        _account (Optional[object]): Current trading account instance.
        _action (Enum): Enumeration of possible trading actions (e.g., BUY, SELL, HOLD).
        _balance (int): Initial balance for trading.
        _buy_quantity (int): Number of assets bought per transaction.
        _fee (float): Transaction fee as a percentage.
        _tax (float): Tax on sales as a percentage.
        _is_terminated (bool): Whether the episode has terminated.
        _is_truncated (bool): Whether the episode has been truncated.
        action_space (gym.spaces.Discrete): Action space for trading actions.
        observation_space (gym.spaces.Box): Observation space for market data.
    """

    def __init__(
        self, 
        feeder: IFeeder,
        account: Callable = None,
        action: Enum = None,
        balance: int = 1_000_000,
        buy_quantity: int = 10,
        fee: float = 0.3,
        tax: float = 0.38
    ) -> None:
        """
        Initializes the trading environment.

        Args:
            feeder (IFeeder): Data feeder for market data.
            account (Callable, optional): Callable to manage the trading account. Defaults to None.
            action (Enum, optional): Enum for possible trading actions. Defaults to None.
            balance (int, optional): Starting balance for trading. Defaults to 1,000,000.
            buy_quantity (int, optional): Number of assets to buy per trade. Defaults to 10.
            fee (float, optional): Transaction fee as a percentage. Defaults to 0.3.
            tax (float, optional): Tax on sales as a percentage. Defaults to 0.38.
        """
        super().__init__()

        feeder.reset()
        self._feeder = feeder
        self._account_class = account
        self._account = None
        self._accounts = []
        self._action = action
        self._balance = balance
        self._buy_quantity = buy_quantity
        self._fee = fee
        self._tax = tax
        self._is_terminated = False
        self._is_truncated = False
        
        self.action_space = gym.spaces.Discrete(len(action))
        self.observation_space = gym.spaces.Box(
            low=-np.inf, high=np.inf, shape=self._feeder.partShape(), dtype=np.float32
        )

    def getFeeder(self) -> IFeeder:
        """
        Returns the data feeder.

        Returns:
            IFeeder: The data feeder.
        """
        return self._feeder
    
    def getAccount(self) -> Optional[object]:
        """
        Returns the current trading account.

        Returns:
            Optional[object]: Current trading account, or None if not initialized.
        """
        return self._account
    
    def getAccounts(self) -> list:
        """
        Returns the list of all past accounts.

        Returns:
            list: List of past account states.
        """
        return self._accounts
    
    def getHistory(self) -> Tuple[Any, Any]:
        """
        Returns the history of assets and trades.

        Returns:
            Tuple[Any, Any]: Asset and trade history as DataFrames.
        """
        return self._account.getHistory()
    
    def reset(
        self, 
        seed: Optional[int] = None, 
        options: Optional[Dict[str, Any]] = None
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Resets the environment to the initial state.

        Args:
            seed (Optional[int], optional): Random seed. Defaults to None.
            options (Optional[Dict[str, Any]], optional): Reset options. Defaults to None.

        Returns:
            Tuple[np.ndarray, Dict[str, Any]]: Initial observation and additional info.
        """
        super().reset(seed=seed)

        if seed is not None:
            np.random.seed(seed)
        
        self._feeder.reset()
        feed_info = self._feeder.info()
        code, name = "test", "test"
        if feed_info is not None:
            code = feed_info["code"] if "code" in feed_info else "test"
            name = feed_info["name"] if "name" in feed_info else "test"
        self._account = self._account_class(
            code, name, balance=self._balance, fee=self._fee, tax=self._tax
        )
        self._is_terminated = False
        self._is_truncated = False
        self._accounts = []
        
        self._obs, self._feed_change = self._feeder.next()
        self._account.hold(
            self._obs[0][self._feeder.col_daytime()],
            self._obs[0][self._feeder.col_price()]
        )

        extra_info = self._extra_infos(self._obs)
        self._obs.addColumn("average_price", extra_info.asset.average_price)
        return self._obs, extra_info
    
    def _extra_infos(self, obs: np.ndarray) -> Dict[str, Any]:
        """
        Returns additional information about the current state.

        Args:
            obs (np.ndarray): Current observation.

        Returns:
            Dict[str, Any]: Additional info including asset and trade history.
        """
        hist_asset, hist_trade = self.getHistory()
        self._cant_trade = False
        if (
            hist_asset[0].balance < obs[0][self._feeder.col_price()] 
            and hist_asset[0].quantity == 0
        ):
            self._cant_trade = True
        return DotDict({
            "feed_change": self._feed_change,
            "asset": hist_asset[0] if len(hist_asset) > 0 else None,
            "trade": hist_trade[0] if len(hist_trade) > 0 else None,
        })
    
    def _terminated(self, obs: Optional[np.ndarray], feed_change: Optional[object]) -> bool:
        """
        Checks if the episode is terminated.

        Args:
            obs (Optional[np.ndarray]): Current observation.
            feed_change (Optional[object]): Data feed change.

        Returns:
            bool: True if terminated, False otherwise.
        """
        terminated = obs is None and feed_change is None
        
        if terminated:
            self._accounts.append(self._account)

        return terminated
    
    def _truncated(self, obs: Optional[np.ndarray], feed_change: Optional[object]) -> bool:
        """
        Checks if the episode is truncated.

        Args:
            obs (Optional[np.ndarray]): Current observation.
            feed_change (Optional[object]): Data feed change.

        Returns:
            bool: True if truncated, False otherwise.
        """
        return self._cant_trade
    
    @abstractmethod
    def _act(
        self, 
        action: int, 
        rate: float, 
        obs: np.ndarray, 
        feed_change: object
    ) -> None:
        """
        Executes the specified action.

        Args:
            action (int): Action to perform.
            rate (float): Rate that may influence the action.
            obs (np.ndarray): Current observation.
            feed_change (object): Data feed change.

        Raises:
            NotImplementedError: If not implemented in subclass.
        """
        pass
    
    @abstractmethod
    def _reward(
        self, 
        action: int, 
        rate: float, 
        obs: np.ndarray, 
        feed_change: object, 
        asset: Optional[object], 
        trade: Optional[object]
    ) -> float:
        """
        Calculates the reward for the action taken.

        Args:
            action (int): Action taken.
            rate (float): Rate that may influence the reward.
            obs (np.ndarray): Current observation after action.
            feed_change (object): Data feed change after action.
            asset (Optional[object]): Latest asset history.
            trade (Optional[object]): Latest trade history.

        Returns:
            float: The calculated reward.
        """
        return 0.0
    
    def step(self, action: int, rate: float = 0.0) -> Tuple[IFeedPart, float, bool, bool, Optional[Dict[str, Any]]]:
        """
        Executes one step in the environment.

        Args:
            action (int): Action to take.
            rate (float, optional): Rate influencing the action. Defaults to 0.0.

        Returns:
            Tuple[obs, reward, terminated, truncated, info]:
                - obs(IFeedPart): Observation after step
                - reward(float): Reward
                - terminated(bool): Termination flag
                - truncated(bool): Truncation flag
                - info(Optional[Dict[str, Any]]): Additional info
        """
        if self._is_terminated:
            return self._obs, 0.0, self._is_terminated, self._is_truncated, None
        
        self._act(action, rate, self._obs, self._feed_change)
        self._obs, self._feed_change = self._feeder.next()

        self._is_terminated = self._terminated(self._obs, self._feed_change)
        truncated = self._truncated(self._obs, self._feed_change)
        if self._is_terminated or truncated:
            return self._obs, 0.0, self._is_terminated, self._is_truncated, None
        
        extra_info = self._extra_infos(self._obs)
        if extra_info.feed_change:
            self._accounts.append(self._account)
            feed_info = self._feeder.info()
            self._account = self._account_class(
                feed_info["code"], feed_info["name"], balance=self._balance, fee=self._fee, tax=self._tax
            )
            self._obs, self._feed_change = self._feeder.next()
            self._account.hold(
                self._obs[0][self._feeder.col_daytime()],
                self._obs[0][self._feeder.col_price()]
            )

            return self._obs, 0.0, self._is_terminated, True, None
        
        reward = self._reward(
            action, rate, self._obs, self._feed_change, 
            extra_info.asset, extra_info.trade
        )
        self._obs.addColumn("average_price", extra_info.asset.average_price)
        
        return self._obs, reward, self._is_terminated, truncated, extra_info

    def stepHistorys(self, index: int) -> Tuple[str, str, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Retrieves the historical account and trade data for a specific step index.
    
        This method returns detailed information about a specific historical account state, 
        including the code and name of the asset, the original stock data at that step, 
        the asset changes, and the trade history.
    
        Args:
            index (int): The index of the step to retrieve the historical data for.
    
        Returns:
            Tuple[code, name, data, asset, trade]: 
                - code(str): The asset code. 
                - name(str): The asset name.
                - data(pd.DataFrame): The original stock data at the specified step.
                - asset(pd.DataFrame): The asset history DataFrame, which records changes in the asset.
                - trade(pd.DataFrame): The trade history DataFrame, which records buy/sell transactions.
        """
        accounts = self.getAccounts()
        datas = self.getFeeder().datas()
        
        account = accounts[index]
        code, name = account.getCode(), account.getName()
        asset, trade = account.getHistory()
        data = datas[index]
        
        return code, name, data, asset._df, trade._df

    def graphHistory(self, index: int = 0, width: int = 1200, extra_plots: list = [], extra_height = 130) -> None:
        """
        Retrieves and visualizes historical trading data for a specific account index.
    
        Args:
            index (int, optional): 
                The index of the account history to retrieve and visualize. Must be within the range 
                of available account histories. Defaults to 0.
            
            width (int, optional): 
                The width of the resulting graph in pixels. Defaults to 1200.
            
            extra_plots (list, optional): 
                A list of additional plots to include in the visualization. Each element in the list 
                should be a Bokeh plot object or a similar compatible object. Defaults to an empty list.
    
        Raises:
            AssertionError: 
                If the provided index is out of the valid range (i.e., not between 0 and history_size - 1).
    
        Returns:
            None
        """
        history_size = len(self.getAccounts())
        assert index < history_size, f"Index must be between 0 and {history_size-1}."
        
        code, name, data, asset, trade = self.stepHistorys(index)
        
        # Create buy history DataFrame
        trade_buy = trade[trade.action == "buy"][["reg_day", "price"]]
        trade_buy.rename(columns={'price': 'buy_price'}, inplace=True)
        
        # Create sell history DataFrame
        trade_sell = trade[trade.action == "sell"][["reg_day", "price"]]
        trade_sell.rename(columns={'price': 'sell_price'}, inplace=True)
    
        # Create average price DataFrame for the viewing period
        asset_average_price = asset[asset.average_price > 0][["reg_day", "average_price"]]
        
        # Merge basic data with buy and sell transactions and average price
        merged = pd.merge(data, trade_buy, on="reg_day", how="outer")
        merged = pd.merge(merged, trade_sell, on="reg_day", how="outer")
        merged = pd.merge(merged, asset_average_price, on="reg_day", how="outer")
        
        # Adjust positions for buy and sell markers
        merged.loc[merged["buy_price"].notnull(), "buy_price"] = merged["close"] * 0.95
        merged.loc[merged["sell_price"].notnull(), "sell_price"] = merged["close"] * 1.05

        col_daytime = self._feeder.col_daytime()
        # Display the graph using the showGraph function
        showGraph(code, name, asset, merged, col_daytime, extra_plots, width, extra_height=extra_height)
