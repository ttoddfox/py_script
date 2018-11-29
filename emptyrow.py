#-*- encoding=utf-8 -*-

import os
from math import isnan
import pandas as pd
import math
import os
import re
import numpy as np
    
work_dir=r'C:\Users\txu1\Desktop'
data_path=os.path.join(work_dir,'test1.csv')
data=pd.read_csv(data_path,encoding="gb2312",header=0)
data=data.dropna(thresh=1)
data.to_csv(os.path.join(work_dir,'test1_result.csv'))
