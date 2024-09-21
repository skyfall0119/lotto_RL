from utils.util import inst_all_from_requirements
import argparse
import os

def predict(modelname : str):
    import numpy as np
    import pandas as pd
    from pathlib import Path
    from dotenv import load_dotenv
    from stable_baselines3 import PPO

    import numCrawling as nc
    from customEnv import Env_v1, Env_v2
   
    
    load_dotenv("./setting/keys.env")
    drw_dir = os.environ['DRW_DIR']
    
    
    ## 데이터 업데이트
    ## load data
    print("1. 로또 번호 업데이트 ...")
    df = nc.updateCSV(drw_dir)
    # numList = df[['num1','num2','num3','num4','num5','num6']].values.tolist()
    print(f"최신 회차 {df.iloc[-1]['round']}화. {df.iloc[-1]['date']} \n")
    # print(df.iloc[-1])
    # round          1137
    # date     2024-09-14
    # Name: 1136, dtype: object
    
    ## 강화학습 모델 로드
    print(f"2. 모델 {modelname} 로딩중...")
    model = None
    path = os.path.join("models", modelname)
    try :
        model = PPO.load(path)
    except Exception as e :
        print("모델 로딩 에러", e)
    if model is not None :        
        print(f"2. 모델 {modelname} 로딩 완료\n")
    
    
    print("*"*30)
    print("\nLOTTO PREDICTION!!!!\n")
    print("*"*30)
    
    ## TODO
    ## 메인 predict


if __name__ == "__main__":
    # inst_all_from_requirements('./setting/requirements.txt')
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-cm", '--check', required=False, default=False)
    parser.add_argument('-m', '--model', required=False, default="Env_v1")

    args = parser.parse_args()
    
    if args.check :
        print("현재 가능 모델") 
        for i in os.listdir("./models") :
            print(i[:-4])
        print("default model : Env_v1")
        
    else :
        predict(args.model)