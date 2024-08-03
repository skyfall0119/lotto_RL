# import
import gymnasium as gym
from gymnasium.spaces import Box, Tuple
import numpy as np
import utils.util as util
"""
    simple unconditioned learning.
    guess. check matches, and move to next.
"""
class Env_v1(gym.Env) :
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}
    
    def __init__(self, numList, render_mode=None):
        super(Env_v1, self).__init__()
        
        self.action_space = Box(0, 1, shape=(45,), dtype=float)
        self.observation_space = Box(low=np.zeros([45]), high=np.ones([45]))
        
        # 현재 회차
        self.ind = 0
        
        # 시작지점
        self.state = util.num2OneHot(numList[0])
        
        # 로또 번호 리스트
        self.numList = numList
        
        
    ## logic 1. guess , move
    def step(self, action):
        # Generate the picked numbers based on the action
        stepNum = self._pickNumber(action)

        # Update the state
        self.ind += 1

        # Check if the episode is terminated or truncated
        terminated = self.ind >= len(self.numList)
        truncated = False

        if not terminated:
            # Get the target numbers for the current draw
            target = util.num2OneHot(self.numList[self.ind])

            # Compute the reward
            reward = self.checkReward(stepNum, target)

            # Update the state to the new target
            self.state = target
        else:
            reward = 0

        # Return the new observation, reward, termination status, truncation status, and additional info
        observation = self.state
        info = {}

        return observation, reward, terminated, truncated, info

    ## no need
    def render(self):
        pass

    def reset(self, seed=None):
        super().reset(seed=seed)
        self.ind = 0
        self.state = util.num2OneHot(self.numList[0])
        
        return self.state, seed

    """
        generate action of random 6 unique numbers of 1~45.
        # action => Box(0, 1, shape=(45,), dtype=float).sample()    
    """
    def _pickNumber(self, action) :
        
        tmp = action.copy()
        
        for _ in range(6) :
            tmp[tmp.argmax()] = -2
            
        ceilFnc = np.vectorize(lambda x:1 if x == -2 else 0)
        nums = ceilFnc(tmp)
        
        return nums



        ## 보상 체크 함수
    """
    args:
        numbers = 원핫인코딩된 비교숫자
        targets = 원핫인코딩된 다음회차 숫자

    return:
        rewards = 맞는 숫자에 따라 보상 반환  
    """
    def checkReward (self, numbers, targets):
        matching = numbers * targets
        numMathced = matching.sum()
        if numMathced == 3.0 :
            return 1
        elif numMathced == 4.0 :
            return 10
        elif numMathced == 5.0 :
            return 20
        elif numMathced == 6.0 :
            return 100
        else :
            return -1


