
import numpy as np 
import pandas as pd 

def cost(h, y):
	return -y*log(h) - (1-y)*log(1-h)
