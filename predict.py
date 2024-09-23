from utils.util import inst_all_from_requirements
import argparse
import os
from stable_baselines3 import PPO
import numCrawling as nc
from customEnv import Env_v1, Env_v2

from dotenv import load_dotenv
load_dotenv("./setting/keys.env")
drw_dir = os.environ['DRW_DIR']





if __name__ == "__main__":
    # inst_all_from_requirements('./setting/requirements.txt')
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-cm", '--check', required=False, default=False)
    parser.add_argument('-m', '--model', required=False, default="Env_v1")

    args = parser.parse_args()
    
    ######## 데이터 업데이트 & 로드
    print("1. 로또 번호 업데이트 ...")
    df = nc.updateCSV(drw_dir)
    print(f"최신 회차 {df.iloc[-1]['round']}화. {df.iloc[-1]['date']} \n")
    numList = df[['num1','num2','num3','num4','num5','num6']].values.tolist()

    
    if args.check :
        print("현재 가능 모델") 
        for i in os.listdir("./models") :
            print(i[:-4])
        print("default model : Env_v1")
    
        
    else :
        modelname = args.model
        
            ######## 모델 로드
        print(f" 모델 {modelname} 로딩중...")
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
        

        ######## predict
        # env load
        if modelname == "Env_v1" :
            env = Env_v1(numList=numList)
        elif modelname == "Env_v2" :
            env = Env_v2(numList=numList)
        
        # reset env
        pred = env.predict(model=model)
        
        for i, num in enumerate(pred) :
            print(f"예측번호 {i+1} : {num}")
    