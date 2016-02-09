from datetime import datetime
import csv
import pandas as pd

# class cfile(file):
#
#     def __init__(self, name, mode='r'):
#         self = file.__init__(self,name, mode)
#
#     def wl(self, string):
#         self.writelines(sring + '\n')
#         return None

def writetotxt():
    for i in range(2010,2016):
        start = datetime(i,1,1)
        end = datetime(i,12,31)
        # index = pd.date_range(start,end)
        fid = open('inputdates_{}.txt'.format(i), 'w')
        fid.write('racedate'+'\n')
        for d in pd.date_range(start, end):
            dout = datetime.strftime(d.date(), '%Y-%m-%d')
            fid.write(dout+'\n')
        fid.close()

writetotxt()

##next get list of raceurls?
