from utils.util import inst_all_from_requirements

def main():
    import numpy as np
    import pandas as pd
    import os
    from pathlib import Path
    from dotenv import load_dotenv

    
    import numCrawling as nc
    from customEnv import Env_v1, Env_v2
   
    
    
    load_dotenv("./setting/keys.env")
    drw_dir = os.environ['DRW_DIR']
    
    
    ## 데이터 업데이트
    ## load data
    print("loading numbers...")
    df = nc.updateCSV(drw_dir)
    numList = df[['num1','num2','num3','num4','num5','num6']].values.tolist()
    
    ## 강화학습 클래스
    model = None
    
    
    print("*"*30)
    print("\nLOTTO PREDICTION!!!!\n")
    print("*"*30)
    ## TODO
    ## 메인 프로그램 loop
    while True :
        print(f"현재 선택된 모델 : {model}")
        
        try :
            inp = int(input("Operation \n1. {}\n2. {}\n3. {}\n4. {}\n5. {}\n Select : ".format(
                "model select",
                "model train",
                "model evaluate",
                "model predict",
                "exit"
            )))
        except ValueError :
            print("select number")
         
         
        ## main operations
        if inp == 0 :
            pass
        elif inp == 1 :
            pass
        elif inp == 2 :
            pass
        elif inp == 3 :
            pass
        elif inp == 4 :
            pass
        elif inp == 5 :
            print("exit program")
            break
        
    
    ## 1. 모델 선택.
    ## 2. 모델 예측
    ## 3. 모델 추가 학습
    ## 4. 숫자별 통계
    ## 5. GUI
    

    
        



if __name__ == "__main__":
    # inst_all_from_requirements('./setting/requirements.txt')
    
    main()