import argparse
import os
from dotenv import load_dotenv

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import BaseCallback


import numCrawling as nc
from customEnv import Env_v1, Env_v2
import inspect
import importlib

load_dotenv("./setting/keys.env")
drw_dir = os.environ['DRW_DIR']




if __name__ == "__main__" :
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-cm", '--check', required=False, default=False)
    parser.add_argument('-m', '--model', required=False, default="Env_v1")
    parser.add_argument('-n', '--name', required=False, default="Env_v1")
    parser.add_argument('-e', '--env', required=False, default=4)
    parser.add_argument('-s', '--timesteps', required=False, default=50000)
    
    args = parser.parse_args()
    

    print("1. 로또 번호 업데이트 ...")
    df = nc.updateCSV(drw_dir)
    print(f"최신 회차 {df.iloc[-1]['round']}화. {df.iloc[-1]['date']} \n")
    numList = df[['num1','num2','num3','num4','num5','num6']].values.tolist()

    if args.check :
        print("현재 훈련 가능 모델:") 
        mod = importlib.import_module("customEnv")
        classes = inspect.getmembers(mod, inspect.isclass)
        
        for cls_name, cls_obj in classes :
            if cls_obj.__module__ == "customEnv" :
                print(cls_name)
        
    else :
        ## train
        modelname = args.model
        if modelname == "Env_v1" :
            vec_env = make_vec_env(lambda : Env_v1(numList=numList), n_envs=int(args.env))
        elif modelname == "Env_v2" :
            vec_env = make_vec_env(lambda : Env_v2(numList=numList), n_envs=int(args.env))
        
        log_path = os.path.join('Training', "Logs")
        model = PPO('MlpPolicy', vec_env, verbose = 1, tensorboard_log=log_path)
        
        model.learn(total_timesteps=int(args.timesteps))
        
        model.save(f"./models/{args.name}")
        
        print(f"training done. timesteps:{args.timesteps}.")
        ## TODO :
        ## implement callback for the final result of the training.

        
    