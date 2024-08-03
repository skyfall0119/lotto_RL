
# import helpers
import subprocess, sys

def inst_all_from_requirements(requirement_file):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirement_file])


def main():
    import numpy as np
    import pandas as pd
    import os
    from dotenv import load_dotenv
    import numCrawling as nc
    
    load_dotenv("./setting/keys.env")
    
    drw_dir = os.environ['DRW_DIR']
    
    
    ## 데이터 업데이트
    ## load data
    df = nc.updateCSV(drw_dir)
    numList = df[['num1','num2','num3','num4','num5','num6']].values.tolist()
    
    
    ## 강화학습 클래스
    
    ## TODO
    ## 메인 프로그램 loop
    
    ## 1. 모델 선택.
    ## 2. 모델 예측
    ## 3. 모델 추가 학습
    ## 4. 숫자별 통계
    ## 5. GUI

    
        



if __name__ == "__main__":
    inst_all_from_requirements('./setting/requirements.txt')
    
    main()