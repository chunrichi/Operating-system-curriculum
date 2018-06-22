from tkinter.messagebox import *
import re

# 打开文件
def open_prc(fileName):
    file = open(fileName,'r', encoding= 'utf-8')
    file_str = file.read()
    if len(file_str)<0:
        showerror('文档错误','内容读取失败')
    return file_str

# 处理,生成字典
def make_dict(str):
    str_array = str.split('\n')
    # 分割字符串结果
    print('-'*30 + '生成字典-分割结果')
    print(str_array)

    P = locals()    # 进程的一名命名空间
    P_times = 0     # 进程数量
    for s in str_array:
        if s.find('P')>=0:
            P_times = P_times + 1
            P['P%s' % P_times] = []
        else:
            P['P%s' % P_times].append(s)
    
    P_dict = {}
    # 进程提取结果
    for times in range(1, P_times + 1):
        print('-'*30 + '生成字典-进程提取结果')
        print('P%s:%s' % (times,P['P%s' % times]))

        P_dict['P%s' % times] = P['P%s' % times]
    
    print('-'*30 + '字典生成-字典生成结果')
    print(P_dict)
    return P_times,P_dict

# 专门获得进程数量的，用来终止
def get_pcb_times(str):
    times = 0
    str_array = str.split('\n')
    for s in str_array:
        if s.find('P')>=0:
            times = times + 1
    return times

# 处理，生成PCB对象
def make_pcbs(file_str):
    Ptimes,Pdict = make_dict(file_str)
    # 创建PCB
    pcbs = []
    for times in range(1, Ptimes + 1):
        # 进程提取
        CIs = []
        for cis_str in Pdict['P%s' % times]:
            cis = CInstruction(cis_str)
            CIs.append(cis)

        pcb = PCB(CIs, 'P%s' % times, times)
        pcbs.append(pcb)
        # 显示Pcb中的内容
        print('-'*30 + '显示Pcb中的内容')
        pcb.pcb_print()
    print(pcbs)
    return pcbs

# 进程控制块类
class PCB():
    # self.PName
    def __init__(self,P_list,PName,Pid):
        # 进程名
        self.PName = 'P%s' % Pid
        # 进程标识符
        self.Pid = Pid
        # 指令列表
        self.Plist = P_list
        # 进程剩余时间
        self.ReaminedTime = 0
        # 正在运行或者将要运行的指令
    
    def get_PName(self):
        return self.PName

    def get_Pid(self):
        return self.Pid

    def get_Plist(self)->list:
        return self.Plist

    def get_ReaminedTime(self)->int:
        return self.ReaminedTime
        
    def set_Plist(self,plist):
        self.Plist = plist

    def set_ReaminedTime(self,time):
        self.ReaminedTime = time

    
    def pcb_print(self):
        print('PNamem:%s \nPid:%s \nPlist:%s \nReaminedTime:%s' % (self.PName,self.Pid,self.Plist,self.ReaminedTime))
        for i in range(len(self.Plist)):
            print('Plist.list[0]:\t%s' %  self.Plist[i].get_InstrucionId())
        print()

# 指令类
class CInstruction(object):
    def __init__(self, string):
        # 指令运行时间
        self.RunTime = int(re.findall('(\d+)',string)[0])
        # 指令类型
        self.InstructionId = re.findall('(\w)',string)[0]

    def get_RunTime(self):
        return self.RunTime

    def get_InstrucionId(self):
        return self.InstructionId

if __name__ == '__main__':
    print('测试CIs类')
    c = CInstruction('C30')
    print('%s %s' %(c.get_RunTime(),c.get_InstrucionId()))

    # file_str = open_prc(u'.\sourse\Prc.txt')
    # pcbs = make_pcbs(file_str)


