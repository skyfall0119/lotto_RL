import numpy as np
import subprocess, sys
from enum import Enum


def inst_all_from_requirements(requirement_file):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirement_file])




def num2OneHot(numbers) :
    oneHot = np.zeros(45)
    
    for num in numbers :
        oneHot[int(num-1)] = 1
    return oneHot

def oneHot2Num(oneHot) :
    numbers = []
    for i in range(len(oneHot)) :
        if oneHot[i] == 1.0:
            numbers.append(i+1) 
    
    return numbers

