# import
import gymnasium as gym
from gymnasium.spaces import Box
import numpy as np
from utils import util
"""
    현재 회차 번호를 받고 다음회차 번호 예측
"""
class Env_v1(gym.Env) :
    # metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}
    
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
    
    def predict(self, model, num_repeats=5):
        self.reset()
        predictions = []
        
        for _ in range(num_repeats):
            # Reset the environment to the latest state
            self.ind = len(self.numList) - 1
            self.state = util.num2OneHot(self.numList[-1])
            observation = self.state

            # Get the predicted action from the model
            action, _states = model.predict(observation)

            # Decode the action to get the predicted lottery numbers
            predicted_numbers = self._pickNumber(action)

            # Convert one-hot encoded action to the actual numbers
            predicted_numbers_list = util.oneHot2Num(predicted_numbers)
            predictions.append(predicted_numbers_list)
        
        return predictions
    
    


"""
    5개 번호 세트 (5000원) 기준 최소 번호 한개 이상에서 따기.
"""
class Env_v2(gym.Env) :
    
    def __init__(self, numList, render_mode=None):
        super(Env_v2, self).__init__()
        
        ## Tuple is not supported... 
        ## flatten version
        self.action_space = Box(0, 1, shape=(45 * 5,), dtype=float)  
        self.observation_space = Box(low=np.zeros([45]), 
                                     high=np.ones([45]), 
                                     dtype=float)

        # 현재 회차
        self.ind = 0
        
        # 시작지점
        self.state = util.num2OneHot(numList[0])
        
        # 로또 번호 리스트
        self.numList = numList
        
        
    def step(self, action):
        # Generate the picked numbers based on the action
        stepNums = self.pickNumber(action)

        # Update the state
        self.ind += 1

        # Check if the episode is terminated or truncated
        terminated = self.ind >= len(self.numList)
        truncated = False

        if not terminated:
            # Get the target numbers for the current draw
            target = util.num2OneHot(self.numList[self.ind])

            # Compute the reward
            reward = self.checkReward(stepNums, target)

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
        # action => Box(0, 1, shape=(45 * 5,), dtype=float).sample()    
    """
    def pickNumber(self, action) :
        
        nums = []
        
        for i in range(5) :
            tmp = action[i*45:(i+1)*45]
            for _ in range(6) :
                tmp[tmp.argmax()] = -2
            ceilFnc = np.vectorize(lambda x:1 if x == -2 else 0)
            nums.append(ceilFnc(tmp))

        return nums



        ## 보상 체크 함수
    """
    args:
        numbers = 원핫인코딩된 비교숫자 리스트. 5세트
        targets = 원핫인코딩된 다음회차 숫자

    return:
        rewards = 맞는 숫자에 따라 보상 반환  
    """
    def checkReward (self, numbers, target):
        total = 0
        
        for num in numbers :
            numMathced = (num * target).sum()
        
            if numMathced == 3.0 :
                total+= 1
            elif numMathced == 4.0 :
                total+=10
            elif numMathced == 5.0 :
                total+=100
            elif numMathced == 6.0 :
                total+=1000
            # else :
            #     total-=1
        return total
    
    def predict(self, model):
        self.reset()
        
        # Reset the environment to the latest state
        self.ind = len(self.numList) - 1
        self.state = util.num2OneHot(self.numList[-1])
        observation = self.state

        # Get the predicted action from the model
        action, _states = model.predict(observation)

        # Decode the action to get the predicted lottery numbers
        predicted_numbers = self.pickNumber(action)
        
        # for i, num in enumerate(predicted_numbers) :
        #     predicted_numbers[i] = util.oneHot2Num(num)
        
        return [util.oneHot2Num(x) for x in predicted_numbers]
