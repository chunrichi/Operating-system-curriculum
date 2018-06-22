#-*- coding:utf-8 -*-


"""
@author: Shi Lei
@finish-date: 2018-6-22
"""



from tkinter import *
# from tkinter.messagebox import *
import tkinter.filedialog
import threading
import time
from save_log import *
from prc import *

# 解决深浅复制问题
import copy

# 全局变量
# ---- 就绪队列
ReadyPCBs = [] 
# ---- 后备就绪队列
BackupReadyPCBs = []
# ---- 输入等待队列
InputWaittingPCBs = []
# ---- 输出等待队列
OutputWaittingPCBs = []
# ---- 其他等待队列
PureWaittingPCBs = []
# ---- 结束队列
FinishPCBs = []

# ---- 当前运行
C_run = False
C_pcb = PCB([],'',0)
# ---- 当前输入
I_run = False
# ---- 当前输出
O_run = False
# ---- 当前其他
W_run = False

# ---- 时间片大小（定时器时间间隔的倍数）
TimeSlice = 0
# 减少时间的记录
timeslice = 0
# 记录运行状态的
run_flag = True




class My_GUI():
    def __init__(self,window_tk):
        self.window_tk = window_tk

    def set_init_window(self):
        self.window_tk.title('进程调度模拟程序')          # title
        self.window_tk.geometry('900x500+250+150')      # 主界面大小及位置

        # 变量定义-->使用的是tkinter自带的变量体系，用来直接更改属性
        # 用来显示时间片减少
        self.timeslice_text = StringVar()
        self.C_entry_text = StringVar()

        self.Cwait_list_text = StringVar()
        self.wait_list_text = StringVar()
        self.Iwait_list_text = StringVar()
        self.Owait_list_text = StringVar()
        self.other_list_text = StringVar()


        # 操作内容Frame框架
        btn_frame = Frame(width= 800, height= 50)
        # btn按钮
        # ----打开文件按钮-->事件：open_file
        self.open_btn = Button(btn_frame, text='打开文件', width= 10, height= 1, command=self.open_file)
        self.begin_btn = Button(btn_frame, text= '开始调度', width= 10, height= 1, command= self.begin)
        self.stop_btn = Button(btn_frame, text= '暂停调度', width= 10, height= 1, command= self.stop, state = DISABLED)   # 开始的时候禁用
        self.time_label = Label(btn_frame, text= '时间片大小:', width= 10, height= 1)
        self.time_entry = Entry(btn_frame, text= '200', width= 15, textvariable = self.timeslice_text)
        # ----显示
        btn_frame.place(x= 50, y= 20)
        self.open_btn.place(x= 0, y= 5)
        self.begin_btn.place(x= 150, y= 5)
        self.stop_btn.place(x= 300, y= 5)
        self.time_label.place(x= 500, y= 8)
        self.time_entry.place(x= 580, y= 8)

        # 信息显示Frame框架
        message_frame = Frame(width= 800, height= 50)
        # ----运行进程显示
        self.C_label = Label(message_frame, text= '当前CPU运行进程:', width= 15, height= 1)
        self.C_entry = Entry(message_frame, width= 15, state= 'readonly', textvariable = self.C_entry_text)
        # ----显示
        message_frame.place(x= 50, y= 80)
        self.C_label.grid(row = 0, column = 1)
        self.C_entry.grid(row = 0, column = 2, sticky='we', ipadx = 60 , padx= 5)

        # 队列信息Frame
        list_frame = Frame(width= 800, height= 330)
        # ----队列展示
        self.Cwait_list_lf = LabelFrame(list_frame, width= 160,height= 340, text= '就绪队列')
        self.wait_list_lf = LabelFrame(list_frame, width= 160,height= 340, text= '后备就绪队列')
        self.Iwait_list_lf = LabelFrame(list_frame, width= 160,height= 340, text= '输入等待队列')
        self.Owait_list_lf = LabelFrame(list_frame, width= 160,height= 340, text= '输出等待队列')
        self.other_list_lf = LabelFrame(list_frame, width= 160,height= 340, text= '其他等待队列')
        self.Cwait_list = Listbox(self.Cwait_list_lf, height= 15, listvariable = self.Cwait_list_text)
        self.wait_list = Listbox(self.wait_list_lf, height= 15, listvariable = self.wait_list_text)
        self.Iwait_list = Listbox(self.Iwait_list_lf, height= 15, listvariable = self.Iwait_list_text)
        self.Owait_list = Listbox(self.Owait_list_lf, height= 15, listvariable = self.Owait_list_text)
        self.other_list =Listbox(self.other_list_lf, height= 15, listvariable = self.other_list_text)
        # ----显示
        list_frame.place(x= 50, y= 130)
        self.Cwait_list_lf.pack(side= LEFT)
        self.wait_list_lf.pack(side= LEFT)
        self.Iwait_list_lf.pack(side= LEFT)
        self.Owait_list_lf.pack(side= LEFT)
        self.other_list_lf.pack(side= LEFT)
        self.Cwait_list.pack(anchor= CENTER)
        self.wait_list .pack(anchor= CENTER)
        self.Iwait_list.pack(anchor= CENTER)
        self.Owait_list.pack(anchor= CENTER)
        self.other_list.pack(anchor= CENTER)
                
# -----------------------------------------------------------------------------------------------------------------------
# 按钮事件

    def open_file(self):
        # 打开文件，并读取内容
        fileName = tkinter.filedialog.askopenfilename(initialdir = './sourse/')
        file_str = open_prc(fileName)
        # 获得PCB的一个列表，包含所有信息内容
        pcbs = make_pcbs(file_str)
        # 获得PCB数量，并记录
        self.times = get_pcb_times(file_str)

        for pcb in pcbs:
            # 将读取到的进程写入到写入队列
            ReadyPCBs.append(pcb)
        
        # 根据就绪队列添加显示-->一开始没有所以并不进入
        for pcb_print in ReadyPCBs:
            self.Cwait_list.insert(END, pcb_print.get_PName())

        # 显示完成后，将队列内容添加到该去的地方()
        if ReadyPCBs != []:
            self.deal_with_list(ReadyPCBs)
        
        # 打开文件的时候开始创建线程
        # 开始执行程序的线程
        self.t1 = threading.Thread(target=self.run_one_timeslice)

    def begin(self):
        global timeslice
        global TimeSlice
        global run_flag

        
        
        # 判断运行状态，区分是开始运行还是继续运行
        if run_flag:
            # 判断时间片是否输入
            if self.time_entry.get() == '':
                showerror(u'错误',u'请输入时间片大小')
            else:
                self.stop_btn.config(state = NORMAL)
                self.begin_btn.config(state = DISABLED)
                # 获得时间片的大小
                # timeslice_text <==> self.time_entry
                TimeSlice = int(self.time_entry.get())
                timeslice = TimeSlice
                # 执行线程-->run_one_timeslice
                self.t1.start()
        else:
            self.stop_btn.config(state = NORMAL)
            self.begin_btn.config(state = DISABLED)
            # 继续执行
            threading.Thread(target=self.change_flag_true).start()     
    
    def stop(self):
        self.begin_btn.config(state = NORMAL)
        self.stop_btn.config(state = DISABLED)
        # 暂停执行
        threading.Thread(target=self.change_flag_false).start()

    def change_flag_false(self):
        global run_flag
        run_flag = False

    def change_flag_true(self):
        global run_flag
        run_flag = True

# -----------------------------------------------------------------------------------------------------------------------
# 对内容处理

    # 运行一段时间
    def run_one_timeslice(self):
        global C_run
        global C_pcb
        global timeslice
        
        while(True):
            # 点击暂停之后进入这个循环等待
            while(not run_flag):
                pass

            # 对所有内容的剩余时间减一reduce 
            self.reduce_time()

            time.sleep(0.5)
            timeslice = timeslice - 1

            # 对时间片大小进行处理
            if timeslice < 0:
                timeslice = TimeSlice
                # 如果没执行完
                if C_pcb.ReaminedTime > 0:
                    # 生成一个Istruction添加到pcb里面的指令列表首部
                    C_pcb.Plist.insert(0, CInstruction('C%s' % (C_pcb.ReaminedTime + 1))) # 补回刚刚减去的
                    C_pcb.set_ReaminedTime(0)
                    BackupReadyPCBs.append(C_pcb)
                    C_run = False

            # 对正在运行的进行判断
            if C_run == True:
                if C_pcb.ReaminedTime < 0:
                    C_run = False
                    self.go_to_where(C_pcb)
            
            # 对队列进行判断
            if ReadyPCBs != []:
                self.deal_with_list(ReadyPCBs)
            if BackupReadyPCBs != []:
                if_pcb_list = BackupReadyPCBs.copy()
                for Rpcb in if_pcb_list:
                    if Rpcb.get_ReaminedTime()<=0:
                        BackupReadyPCBs.remove(Rpcb)
                        if C_run:
                            BackupReadyPCBs.append(Rpcb)
                        else:
                            # 获得运行时间
                            Rpcb.set_ReaminedTime( Rpcb.Plist[0].get_RunTime())
                            C_run = True
                            # 放进去之后，此时第一条指令已经进入到应该到达的位置，删除掉PCB中的第一条指令
                            Rpcb.Plist.pop(0)
                            C_pcb = Rpcb
                pass
            if InputWaittingPCBs != []:
                self.deal_with_list(InputWaittingPCBs)
            if OutputWaittingPCBs != []:
                self.deal_with_list(OutputWaittingPCBs)
            if PureWaittingPCBs != []:
                self.deal_with_list(PureWaittingPCBs)

            # 显示
            self.re_print()
            self.print_log()

            # 终止
            if self.times == len(FinishPCBs):
                # 对正在运行的清空
                self.timeslice_text.set('')

                print('+'*30 + '\t结束\t' + '+'*30)
                print(self.times,'\t\t',len(FinishPCBs))
                print('FinishPCBs',FinishPCBs,[fpcb.PName for fpcb in FinishPCBs])
                break

    # 减少时间-->这之中不判断 剩余时间是否已经小于零了
    def reduce_time(self):
        # 正在运行的时间减一
        if C_run == True:
            reaminedtime = C_pcb.get_ReaminedTime()
            C_pcb.set_ReaminedTime(reaminedtime - 1)
        # 输入队列减一
        if InputWaittingPCBs != []:
            for pcb in InputWaittingPCBs:
                reaminedtime = pcb.get_ReaminedTime()
                pcb.ReaminedTime = reaminedtime - 1
        # 输出队列减一
        if OutputWaittingPCBs != []:
            for pcb in OutputWaittingPCBs:
                reaminedtime = pcb.get_ReaminedTime()
                pcb.ReaminedTime = reaminedtime - 1
        # 其他队列减一
        if PureWaittingPCBs != []:
            for pcb in PureWaittingPCBs:
                reaminedtime = pcb.get_ReaminedTime()
                pcb.ReaminedTime = reaminedtime - 1
        pass

    # 处理队列里面的内容
    def deal_with_list(self,pcb_list):
        # 此处为拷贝过来，等于相当于指针，会随之改变
        if_pcb_list = pcb_list.copy()

        # 从队列读取内容
        for Rpcb in if_pcb_list:
            # 从队列里面读出来没运行时间的，有剩余时间的进行保留
            if Rpcb.get_ReaminedTime()<=0:
                # 从原始队列删除
                pcb_list.remove(Rpcb)
                self.go_to_where(Rpcb)


    # 判断导入的PCB前往哪个队列
    def go_to_where(self, Rpcb_tw:PCB):
        # 调用全局
        global C_run
        global I_run
        global O_run
        global W_run

        global C_pcb

        if Rpcb_tw.Plist[0].get_InstrucionId() == 'C':
            # 如果当前没有C指令运行
            if not C_run:
                # 获得运行时间
                Rpcb_tw.set_ReaminedTime( Rpcb_tw.Plist[0].get_RunTime())
                C_run = True
                # 放进去之后，此时第一条指令已经进入到应该到达的位置，删除掉PCB中的第一条指令
                Rpcb_tw.Plist.pop(0)
                C_pcb = Rpcb_tw
            else:
                ReadyPCBs.append(Rpcb_tw)
        elif Rpcb_tw.Plist[0].get_InstrucionId() == 'I':
            # 如果为输入指令，直接添加到输入队列中
            Rpcb_tw.set_ReaminedTime( Rpcb_tw.Plist[0].get_RunTime())
            Rpcb_tw.Plist.pop(0)
            InputWaittingPCBs.append(Rpcb_tw)
        elif Rpcb_tw.Plist[0].get_InstrucionId() == 'O':
            Rpcb_tw.set_ReaminedTime( Rpcb_tw.Plist[0].get_RunTime())
            Rpcb_tw.Plist.pop(0)
            OutputWaittingPCBs.append(Rpcb_tw)
        elif Rpcb_tw.Plist[0].get_InstrucionId() == 'W':
            Rpcb_tw.set_ReaminedTime( Rpcb_tw.Plist[0].get_RunTime())
            Rpcb_tw.Plist.pop(0)
            PureWaittingPCBs.append(Rpcb_tw)
        elif Rpcb_tw.Plist[0].get_InstrucionId() == 'H':
            FinishPCBs.append(Rpcb_tw)
        pass

    # 对窗口内容进行更新
    def re_print(self):
        # 对时间片更新
        self.timeslice_text.set(str(timeslice))
        # 显示输入窗口的内容
        if C_run == True:
            self.C_entry_text.set(C_pcb.get_PName() + '-->  ' + str(C_pcb.ReaminedTime))
        else:
            self.C_entry_text.set('')
         # 就绪队列----重新显示
        pcb_list_Ready_print = []
        for pcb_print in ReadyPCBs:
            pcb_list_Ready_print.append(pcb_print.PName)
        self.Cwait_list_text.set(pcb_list_Ready_print)

        # 后备就绪队列----重新显示
        pcb_list_Back_print = []
        for pcb_print in BackupReadyPCBs:
            pcb_list_Back_print.append(pcb_print.PName+ '-->   ' + str(pcb_print.ReaminedTime) + '-->   ' + str(pcb_print.Plist[0].get_RunTime()))
        self.wait_list_text.set(pcb_list_Back_print)

        # 输入队列----重新显示
        pcb_list_Input_print = []
        for pcb_print in InputWaittingPCBs:
            pcb_list_Input_print.append(pcb_print.PName + '-->I  ' + str(pcb_print.ReaminedTime))
        self.Iwait_list_text.set(pcb_list_Input_print)

        # 输出队列----重新显示
        pcb_list_Output_print = []
        for pcb_print in OutputWaittingPCBs:
            pcb_list_Output_print.append(pcb_print.PName + '-->O  ' + str(pcb_print.ReaminedTime))
        self.Owait_list_text.set(pcb_list_Output_print)

        # 其他等待队列----重新显示
        pcb_list_Pure_print = []
        for pcb_print in PureWaittingPCBs:
            pcb_list_Pure_print.append(pcb_print.PName + '-->W  ' + str(pcb_print.ReaminedTime))
        self.other_list_text.set(pcb_list_Pure_print)
        pass
    
    # 打印部分日志
    def print_log(self):
        print('*'*30 + '\t日志打印\t' + '*'*30)
        print('\t\tTimes_now--->%s' % (timeslice))
        print('-'*30 + '\t队列内容\t' + '-'*30)

        ReadyPCB_string = ''
        BackupReadyPCBs_string = ''
        InputWaittingPCBs_string = ''
        OutputWaittingPCBs_string = ''
        PureWaittingPCBs_string = ''
        FinishPCBs_string = ''

        print('ReadyPCBs:\t')
        for p in ReadyPCBs:
            print(p.PName,p.ReaminedTime,)
            ReadyPCB_string = ReadyPCB_string + p.PName +' --> '+ str(p.ReaminedTime)+ '\tnext:' + p.Plist[0].get_InstrucionId() + ':' + str(p.Plist[0].get_RunTime()) +'\t'
        print('BackupReadyPCBs:')
        for p in BackupReadyPCBs:
            print(p.PName,p.ReaminedTime,)
            BackupReadyPCBs_string = BackupReadyPCBs_string + p.PName +' --> '+ str(p.ReaminedTime)+ '\tnext:' + p.Plist[0].get_InstrucionId() + ':' + str(p.Plist[0].get_RunTime()) +'\t'
        print('InputWaittingPCBs:')
        for p in InputWaittingPCBs:
            print(p.PName,p.ReaminedTime,)
            InputWaittingPCBs_string = InputWaittingPCBs_string + p.PName +' --> '+ str(p.ReaminedTime) + '\t'
        print('OutputWaittingPCBs:')
        for p in OutputWaittingPCBs:
            print(p.PName,p.ReaminedTime,)
            OutputWaittingPCBs_string = OutputWaittingPCBs_string + p.PName +' --> '+ str(p.ReaminedTime) + '\t'
        print('PureWaittingPCBs:')
        for p in PureWaittingPCBs:
            print(p.PName,p.ReaminedTime,)
            PureWaittingPCBs_string = PureWaittingPCBs_string + p.PName +' --> '+ str(p.ReaminedTime) + '\t'

        for p in FinishPCBs:
            FinishPCBs_string = FinishPCBs_string + p.PName +' --> '+ str(p.ReaminedTime) + '\t'

        print(' '*30 + '\t正在运行\t' + ' '*30)
        print('C_pcb:\t'+ C_pcb.PName+'\t-->\t'+str(C_pcb.ReaminedTime))
        print('C_run:\t'+ str(C_run))

        file_string = '*'*60 + \
                    '\n--timeslice:\t' + str(timeslice) + \
                    '\n\t\tC_pcb:\t' + C_pcb.PName+'\t-->\t'+str(C_pcb.ReaminedTime) + \
                    '\t\tC_run:\t' + str(C_run) + \
                    '\nthe_list_message:\n' + \
                    '\tReadyPCBs: ' + ReadyPCB_string + \
                    '\n\tBackupReadyPCBs: ' + BackupReadyPCBs_string + \
                    '\n\tInputWaittingPCBs: ' + InputWaittingPCBs_string + \
                    '\n\tOutputWaittingPCBs: ' + OutputWaittingPCBs_string + \
                    '\n\tPureWaittingPCBs: ' + PureWaittingPCBs_string + \
                    '\n\tFinishPCBs: ' + FinishPCBs_string + '\n '

        write_to_file(file_string)


def GUI_start():
    window_tk = Tk()
    tk_gui = My_GUI(window_tk)
    tk_gui.set_init_window()

    window_tk.mainloop()



if __name__ == '__main__':
    GUI_start()
