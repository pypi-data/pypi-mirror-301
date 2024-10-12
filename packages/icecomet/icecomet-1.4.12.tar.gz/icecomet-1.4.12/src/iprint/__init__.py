import os
import inspect

class color_text:
    def __init__(self) -> None:
        self.gray = '\033[90m'
        self.red = '\033[91m'
        self.green = '\033[92m'
        self.yello = '\033[93m'
        self.blue = '\033[94m'
        self.magenta = '\033[95m'
        self.sky = '\033[96m'
        self.white = '\033[97m'


        self.grayk = '\033[100m'
        self.redk = '\033[101m'
        self.greenk = '\033[102m'
        self.yellok = '\033[103m'
        self.bluek = '\033[104m'
        self.magentak = '\033[105m'
        self.skyk = '\033[106m'
        self.whitek = '\033[107m'

        self.set = '\033[0m'
        self.ijset = '\033[92m'
        self.jiset = '\033[93m'
    def show(self):
        print(f"{self.gray}gray {self.red}red {self.green}green {self.yello}yello {self.blue}blue {self.magenta}magenta {self.sky}sky {self.white}white {self.set}")
        print(f"{self.grayk}gray {self.redk}red {self.greenk}green {self.yellok}yello {self.bluek}blue {self.magentak}magenta {self.skyk}sky {self.whitek}white {self.set}")
ct = color_text()

class status:
    def __init__(self,tag=0,len=0,type=0,line=0,path=0,round=0,var=0,color=ct.green,end='\n'):
        self.tag = tag
        self.len = len
        self.type = type
        self.line = line
        self.path = path
        self.round = round
        self.var = var
        self.color = color
        self.end = end
        self.npass = 0

class base_color:
    def __init__(self):
        self.cprint = ct.green
        self.ij=ct.green
        self.ji=ct.yello
        self.jk=ct.red
        self.set=ct.set

cb = base_color()

def oncode():
    current_file_path = os.path.abspath(__file__)
    directory = os.path.dirname(current_file_path)
    os.chdir(directory)


def cprint(*arg,color=cb.cprint,end='\n'):
    string = ' '.join([str(i) for i in arg])
    print(f'{color}{string}{cb.set}',end=end)


ij_global = {}
def ij(tag='',mode='',c=cb.ij,end='\n'):
    global ij_global
    if tag=='?':print(ct.magenta+'i_value t_type l_len n_round s_skip');exit()
    tag_toclass = str(tag)
    if tag_toclass not in ij_global.keys():
        if mode=='full':mode='iltaprv'
        ij_global[tag_toclass] = status(color=c,end=end)
        if 'i' in mode:ij_global[tag_toclass].tag = 1
        if 'l' in mode:ij_global[tag_toclass].len = 1
        if 't' in mode:ij_global[tag_toclass].type = 1
        if 'a' in mode:ij_global[tag_toclass].line = 1
        if 'p' in mode:ij_global[tag_toclass].path = 1
        if 'n' in mode:ij_global[tag_toclass].round = 1
        if 'v' in mode:ij_global[tag_toclass].var = 1
    if tag=='':#ถ้าใช้ ij()
        string=f'Passed : {ij_global[tag].npass}'
    elif mode=='':string=f'{tag}'
    elif 's' in mode:return None
    else :
        string=f''
        try : 
            if ij_global[tag_toclass].tag : string=string+f'{tag} \n' 
        except : pass
        try :
            if ij_global[tag_toclass].len : string=string+f'[len : {len(tag)} ]'
        except : pass
        try :
            if ij_global[tag_toclass].type :string=string+f'[type : {type(tag)} ]'
        except : pass
        try :
            if ij_global[tag_toclass].round :string=string+f'[Passed : {ij_global[tag].npass} ]'
        except : pass
        try :
            if ij_global[tag_toclass].line :
                frame = inspect.currentframe().f_back
                info = inspect.getframeinfo(frame)
                string+=f'[At Line {info.lineno} ]'
        except : pass
        try :
            if ij_global[tag_toclass].path :
                current_file_path = os.path.abspath(__file__)
                string+=f'\n{current_file_path}  '
        except : pass
    ij_global[tag_toclass].npass+=1
    string = '\n'.join([i.replace('\n','') for i in string.split('\n') if i != '\n'])#บรรทัดไหนเป็นบรรทัดว่างให้ลบทิ้ง
    print(c+string+cb.set)
    return tag




ji_global = {}
def ji(tag='',mode='',c=cb.ji,end='\n'):
    global ji_global
    if tag=='?':print(ct.magenta+'i_value t_type l_len n_round s_skip');exit()
    tag_toclass = str(tag)
    if tag_toclass not in ji_global.keys():
        if mode=='full':mode='iltaprv'
        ji_global[tag_toclass] = status(color=c,end=end)
        if 'i' in mode:ji_global[tag_toclass].tag = 1
        if 'l' in mode:ji_global[tag_toclass].len = 1
        if 't' in mode:ji_global[tag_toclass].type = 1
        if 'a' in mode:ji_global[tag_toclass].line = 1
        if 'p' in mode:ji_global[tag_toclass].path = 1
        if 'n' in mode:ji_global[tag_toclass].round = 1
        if 'v' in mode:ji_global[tag_toclass].var = 1
    if tag=='':#ถ้าใช้ ji()
        string=f'Passed : {ji_global[tag].npass}'
    elif mode=='':string=f'{tag}'
    elif 's' in mode:return None
    else :
        string=f''
        try : 
            if ji_global[tag_toclass].tag : string=string+f'{tag} \n' 
        except : pass
        try :
            if ji_global[tag_toclass].len : string=string+f'[len : {len(tag)} ]'
        except : pass
        try :
            if ji_global[tag_toclass].type :string=string+f'[type : {type(tag)} ]'
        except : pass
        try :
            if ji_global[tag_toclass].round :string=string+f'[Passed : {ji_global[tag].npass} ]'
        except : pass
        try :
            if ji_global[tag_toclass].line :
                frame = inspect.currentframe().f_back
                info = inspect.getframeinfo(frame)
                string+=f'[At Line {info.lineno} ]'
        except : pass
        try :
            if ji_global[tag_toclass].path :
                current_file_path = os.path.abspath(__file__)
                string+=f'\n{current_file_path}  '
        except : pass
    ji_global[tag_toclass].npass+=1
    string = '\n'.join([i.replace('\n','') for i in string.split('\n') if i != '\n'])#บรรทัดไหนเป็นบรรทัดว่างให้ลบทิ้ง
    print(c+string+cb.set)
    return tag



jk_global = {}
def jk(tag='',mode='',c=cb.jk,end='\n'):
    global jk_global
    if tag=='?':print(ct.magenta+'i_value t_type l_len n_round s_skip');exit()
    tag_toclass = str(tag)
    if tag_toclass not in jk_global.keys():
        if mode=='full':mode='iltaprv'
        jk_global[tag_toclass] = status(color=c,end=end)
        if 'i' in mode:jk_global[tag_toclass].tag = 1
        if 'l' in mode:jk_global[tag_toclass].len = 1
        if 't' in mode:jk_global[tag_toclass].type = 1
        if 'a' in mode:jk_global[tag_toclass].line = 1
        if 'p' in mode:jk_global[tag_toclass].path = 1
        if 'n' in mode:jk_global[tag_toclass].round = 1
        if 'v' in mode:jk_global[tag_toclass].var = 1
    if tag=='':#ถ้าใช้ jk()
        string=f'Passed : {jk_global[tag].npass}'
    elif mode=='':string=f'{tag}'
    elif 's' in mode:return None
    else :
        string=f''
        try : 
            if jk_global[tag_toclass].tag : string=string+f'{tag} \n' 
        except : pass
        try :
            if jk_global[tag_toclass].len : string=string+f'[len : {len(tag)} ]'
        except : pass
        try :
            if jk_global[tag_toclass].type :string=string+f'[type : {type(tag)} ]'
        except : pass
        try :
            if jk_global[tag_toclass].round :string=string+f'[Passed : {jk_global[tag].npass} ]'
        except : pass
        try :
            if jk_global[tag_toclass].line :
                frame = inspect.currentframe().f_back
                info = inspect.getframeinfo(frame)
                string+=f'[At Line {info.lineno} ]'
        except : pass
        try :
            if jk_global[tag_toclass].path :
                current_file_path = os.path.abspath(__file__)
                string+=f'\n{current_file_path}  '
        except : pass
    jk_global[tag_toclass].npass+=1
    string = '\n'.join([i.replace('\n','') for i in string.split('\n') if i != '\n'])#บรรทัดไหนเป็นบรรทัดว่างให้ลบทิ้ง
    print(c+string+cb.set)
    return tag




