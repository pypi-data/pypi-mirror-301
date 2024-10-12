from .feed import *
from .environments import *
from .trader import *
import gymnasium as gym


__version__ = '0.9.4'


gym.register(
    id="StockSpotEnv",
    entry_point="midas_quant:StockSpotEnv",
    kwargs={
        "feeder": None,
        "balance": 1_000_000,
        "quantity": 10,
        "fee": 0.015,
        "tax": 0.38
    }
)