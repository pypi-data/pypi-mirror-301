from .TradeStateMachine import TradeStateMachine
from ..environments.StockSpotEnv import StockSpotEnv, ActionSpot


class TSMStockSpotEnv(TradeStateMachine):
    def __init__(self, transitions=None, initial_state=None, env:StockSpotEnv=None) -> None:
        super().__init__(transitions, initial_state)
        self._env = env

    def getEnvironments(self):
        return self._env

    def reset(self):
        self.initState()
        self._obs, self._info = self._env.reset()
        
        return self._obs, self._info

    def step(self, action):
        obs, reward, terminate, truncate, info = self._env.step(action)

        return obs, reward, terminate, truncate, info

    def _find_state_method(self):
        state = self.state
        
        return getattr(self, f"Strategy{state}", None)

    def _invoke_action(self, action):
        method = getattr(self, action)
        return method()

    def devTest(self, state, verbose: bool = True):
        self.reset()
        method = getattr(self, f"Strategy{state}", None)
        print(method)
        action = method(self, self._obs, self._info, verbose)

        if action is None:
            self.step(ActionSpot.HOLD)
        else:
            action_success = self._invoke_action(action)
            if action_success:
                self.step(ActionSpot(action.split("_")[-1]))

    def simulation(self, verbose: bool = False):
        self.reset()
        try:
            while True:
                method = self._find_state_method()
                action = method(self, self._obs, self._info, verbose)
        
                if action is None:
                    self._obs, reward, terminate, truncate, self._info = self.step(ActionSpot.HOLD)
                else:
                    action_success = self._invoke_action(action)
                    if action_success:
                        self._obs, reward, terminate, truncate, self._info = self.step(ActionSpot(action.split("_")[-1]))
                    else:
                        self._obs, reward, terminate, truncate, self._info = self.step(ActionSpot.HOLD)
    
                if terminate:
                    break
        except:
            print(f"method : Strategy{self.state} is not working")








