import os

def test():
    os.mkdir('test')
    os.chdir(os.getcwd()+'/test')
    open('test0.py','w')
    open('test1.py','w')
    open('test2.py','w')

def pdtest():
    os.mkdir('test')
    os.chdir(os.getcwd()+'/test')
    open('df0.csv','w')
    open('df1.csv','w')
    open('test0.py','w')
    open('test0.py','w')
    open('test1.py','w')
    open('test2.py','w')