import random,sys,os
from tkinter import *
from tkinter.ttk import *
from pynput import mouse
import tkinter as tk
from threading import Thread, Timer
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime,timedelta  # 导入 timedelta
from control import Controller  # 添加这行在文件顶部其他导入语句附近

def resource_path(relative_path):
    """ Get absolute path to resource, works for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        # 设置窗口图标
        icon_path = resource_path('.\\config\\click.png')  # 使用 resource_path 函数
        self.set_icon(icon_path)
        self.tk_label_time_title = self.__tk_label_time_title(self)
        self.tk_label_m2sokmro = self.__tk_label_m2sokmro(self)
        self.tk_label_m2soln9w = self.__tk_label_m2soln9w(self)
        self.tk_input_nextCycleTime = self.__tk_input_nextCycleTime(self)
        self.tk_label_m2somc08 = self.__tk_label_m2somc08(self)
        self.tk_input_nextTime = self.__tk_input_nextTime(self)
        self.tk_text_locationMsg = self.__tk_text_locationMsg(self)
        self.tk_text_msg = self.__tk_text_msg(self)
        self.tk_label_m3z74nqu = self.__tk_label_m3z74nqu(self)
        self.tk_button_clearAll = self.__tk_button_clearAll(self)
        self.tk_button_startOrStop = self.__tk_button_startOrStop(self)
        self.tk_button_delete = self.__tk_button_delete(self)
        self.tk_input_deleteNum = self.__tk_input_deleteNum(self)
        self.tk_button_add = self.__tk_button_add(self)
        self.tk_button_save = self.__tk_button_save(self)
        self.tk_input_addNum = self.__tk_input_addNum(self)
        self.tk_label_opMsg1 = self.__tk_label_opMsg1(self)
        self.tk_label_opMsg2 = self.__tk_label_opMsg2(self)
        self.tk_label_xText = self.__tk_label_xText(self)
        self.tk_input_x = self.__tk_input_x(self)
        self.tk_label_yText = self.__tk_label_yText(self)
        self.tk_input_y = self.__tk_input_y(self)

        self.tray_icon = None
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.tk_label_timeMsg1 = self.__tk_label_timeMsg1(self)
        self.placeholder_text = "如：00:00:00:000"
        self.tk_input_date = self.__tk_input_date(self)
        self.tk_button_timing = self.__tk_button_timing(self)
        self.scheduler = BackgroundScheduler()  # 创建后台调度器
        self.scheduler.start()  # 启动调度器
        self.job_id = None  # 用于存储当前的任务对象

        self.tk_button_search = self.__tk_button_search(self)
        self.tk_label_locMsg1 = self.__tk_label_locMsg1(self)
        self.tk_input_loc = self.__tk_input_loc(self)
        self.tk_label_locMsg2 = self.__tk_label_locMsg2(self)

        try:
            self.listener = mouse.Listener(on_move=self.on_move)
            self.listener.start()
        except Exception as e:
            print("==pynput== ",e)

        # 初始更新时间
        self.tk_button_showMs = self.__tk_button_showMs(self)
        self.yesNoShowMs = False
        self.current_time = None
        self.update_time()

    def update_time(self):
        # 获取当前时间，格式化为 "年-月-日 时:分:秒.毫秒"
        if self.yesNoShowMs:
            self.current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            # 1000毫秒后再次调用update_time来更新时间
            self.after(1, self.update_time)
        else:
            self.current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # 1000毫秒后再次调用update_time来更新时间
            self.after(1000, self.update_time)
        self.tk_label_time_title.config(text=f"{self.current_time}",anchor="center")


    def set_icon(self, path):
        try:
            icon = PhotoImage(file=path)
            self.wm_iconphoto(True, icon)
        except Exception as e:
            print(f"无法设置图标：{e}")

    def __win(self):
        self.title("自动连点器 V3.5.3")
        # 设置窗口大小、居中
        width = 641
        height = 430
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        
        self.resizable(width=False, height=False)
    def set_icon(self, path):
        icon = PhotoImage(file=path)
        self.wm_iconphoto(True, icon)
    def scrollbar_autohide(self,vbar, hbar, widget):
        """自动隐藏滚动条"""
        def show():
            if vbar: vbar.lift(widget)
            if hbar: hbar.lift(widget)
        def hide():
            if vbar: vbar.lower(widget)
            if hbar: hbar.lower(widget)
        hide()
        widget.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Leave>", lambda e: hide())
        if hbar: hbar.bind("<Enter>", lambda e: show())
        if hbar: hbar.bind("<Leave>", lambda e: hide())
        widget.bind("<Leave>", lambda e: hide())
    
    def v_scrollbar(self,vbar, widget, x, y, w, h, pw, ph):
        widget.configure(yscrollcommand=vbar.set)
        vbar.config(command=widget.yview)
        vbar.place(relx=(w + x) / pw, rely=y / ph, relheight=h / ph, anchor='ne')
    def h_scrollbar(self,hbar, widget, x, y, w, h, pw, ph):
        widget.configure(xscrollcommand=hbar.set)
        hbar.config(command=widget.xview)
        hbar.place(relx=x / pw, rely=(y + h) / ph, relwidth=w / pw, anchor='sw')
    def create_bar(self,master, widget,is_vbar,is_hbar, x, y, w, h, pw, ph):
        vbar, hbar = None, None
        if is_vbar:
            vbar = Scrollbar(master)
            self.v_scrollbar(vbar, widget, x, y, w, h, pw, ph)
        if is_hbar:
            hbar = Scrollbar(master, orient="horizontal")
            self.h_scrollbar(hbar, widget, x, y, w, h, pw, ph)
        self.scrollbar_autohide(vbar, hbar, widget)

    def __tk_button_showMs(self,parent):
        btn = Button(parent, text="显示/关闭毫秒", takefocus=False,command=self.updateStatus)
        btn.place(x=20, y=10, width=150, height=30)
        return btn
    def updateStatus(self):
        if self.yesNoShowMs:
            self.yesNoShowMs = False
        else:
            self.yesNoShowMs = True
    def __tk_label_time_title(self, parent):
        label = Label(parent, text="",anchor="center", )
        label.place(x=0, y=10, width=640, height=30)
        return label
    def __tk_label_m2sokmro(self,parent):
        label = Label(parent,text="====================按下F6获取当前鼠标坐标====================",anchor="center", )
        label.place(x=0, y=40, width=640, height=30)
        return label
    def on_move(self, x, y):
        # 更新Label的文本，显示鼠标的位置
        self.tk_label_m2sokmro.config(text=f"==========按下F6获取当前鼠标坐标，当前鼠标位置：x={x}, y={y} ==========",
                                      anchor="center")

    def __tk_label_m2soln9w(self,parent):
        label = Label(parent,text="- 距离下一个循环时间：",anchor="center", )
        label.place(x=352, y=80, width=170, height=30)
        return label
    def __tk_input_nextCycleTime(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=515, y=80, width=50, height=30)
        return ipt
    def __tk_label_m2somc08(self,parent):
        label = Label(parent,text="- 距离下一个点击时间：",anchor="center", )
        label.place(x=352, y=113, width=170, height=30)
        return label
    def __tk_input_nextTime(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=515, y=113, width=50, height=30)
        return ipt
    def __tk_text_locationMsg(self,parent):
        text = Text(parent, state='disabled')
        text.place(x=9, y=177, width=220, height=245)
        return text
    def __tk_text_msg(self,parent):
        text = Text(parent, state='disabled')
        text.place(x=232, y=209, width=402, height=245)
        return text
    def __tk_label_m3z74nqu(self,parent):
        label = Label(parent,text="s/秒",anchor="center", )
        label.place(x=577, y=80, width=51, height=63)
        return label
    def __tk_button_save(self,parent):
        btn = Button(parent, text="保存坐标", takefocus=False,command=self.ctl.saveOp)
        btn.place(x=232, y=147, width=132, height=30)
        return btn
    def __tk_button_clearAll(self,parent):
        btn = Button(parent, text="清空（F5）", takefocus=False,command=self.ctl.clear)
        btn.place(x=366, y=147, width=132, height=30)
        return btn
    def __tk_button_startOrStop(self,parent):
        btn = Button(parent, text="启动/停止（F7）", takefocus=False,command=self.ctl.startOrStop)
        btn.place(x=499, y=147, width=132, height=30)
        return btn

    def __tk_button_delete(self,parent):
        btn = Button(parent, text="删除", takefocus=False,command=self.ctl.deleteOp)
        btn.place(x=9, y=80, width=50, height=30)
        return btn
    def __tk_input_deleteNum(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=89, y=80, width=90, height=30)
        return ipt
    def __tk_button_add(self,parent):
        btn = Button(parent, text="添加", takefocus=False,command=self.ctl.addOp)
        btn.place(x=9, y=113, width=50, height=30)
        return btn

    def __tk_input_addNum(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=89, y=113, width=90, height=30)
        return ipt
    def __tk_label_opMsg1(self,parent):
        label = Label(parent,text="第",anchor="center", )
        label.place(x=62, y=80, width=30, height=63)
        return label
    def __tk_label_opMsg2(self,parent):
        label = Label(parent,text="个位置",anchor="center", )
        label.place(x=180, y=80, width=50, height=63)
        return label

    def __tk_label_xText(self, parent):
        label = Label(parent, text="X：", anchor="center", )
        label.place(x=230, y=80, width=50, height=30)
        return label
    def __tk_input_x(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=262, y=80, width=90, height=30)
        return ipt
    def __tk_label_yText(self, parent):
        label = Label(parent, text="Y：", anchor="center", )
        label.place(x=230, y=113, width=50, height=30)
        return label
    def __tk_input_y(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=262, y=113, width=90, height=30)
        return ipt

    def __tk_label_timeMsg1(self,parent):
        label = Label(parent,text="在",anchor="center", )
        label.place(x=9, y=147, width=20, height=30)
        return label
    def __tk_input_date(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=31, y=145, width=158, height=30)
        ipt.insert(0, self.placeholder_text)  # 插入占位符文本
        ipt.bind("<Button-1>", self.on_click)  # 绑定点击事件
        ipt.bind("<FocusIn>", self.on_focus)  # 绑定获得焦点事件
        ipt.bind("<FocusOut>", self.on_blur)  # 绑定失去焦点事件
        return ipt

    def on_click(self, event):
        # 点击时如果文本是占位符，则删除
        widget = event.widget
        if widget.get() == self.placeholder_text:
            widget.delete(0, tk.END)

    def on_focus(self, event):
        # 获得焦点时如果文本是占位符，则删除
        widget = event.widget
        if widget.get() == self.placeholder_text:
            widget.delete(0, tk.END)

    def on_blur(self, event):
        # 失去焦点时如果文本为空，则插入占位符
        widget = event.widget
        if widget.get() == '':
            widget.insert(0, self.placeholder_text)
    def __tk_button_timing(self,parent):
        btn = Button(parent, text="定时", takefocus=False,command=self.startTask)
        btn.place(x=190, y=147, width=40, height=30)
        return btn

    def startTask(self):
        time_str = self.tk_input_date.get()
        if time_str == self.placeholder_text or not time_str:
            tk.messagebox.showerror("错误", "时间格式不正确，请输入时分秒毫秒（例如：00:00:00:000）")
            return
        try:
            # 尝试替换中文冒号为英文冒号
            time_str = time_str.replace('：', ':')
            #hours, minutes, seconds, milliseconds = map(int, time_str.split(':'))
            time_parts = time_str.split(':')
            hours, minutes, seconds = map(int, time_parts[:3])
            milliseconds = int(time_parts[3]) if len(time_parts) == 4 else 0  # 如果没有输入毫秒，则默认为0
            now = datetime.now()
            year, month, day, _ = now.year, now.month, now.day, now.hour
            run_date = datetime(year, month, day, hours, minutes, seconds, milliseconds)
            # 如果设置的时间已经过去，则顺延到明天
            if run_date < now:
                run_date += timedelta(days=1)
                self.ctl.update_msg(f"当前设定时间：{run_date} 已过\n将于明天同一时间点执行\n")
            else:
                self.ctl.update_msg(f"当前设定时间点为：{run_date}\n")

            self.schedule_task(run_date,hours,minutes, seconds, milliseconds)
        except ValueError:
            tk.messagebox.showerror("错误", "时间格式不正确，请输入时分秒毫秒（例如：00:00:00:000）")

    def schedule_task(self, run_date,hours,minutes,seconds,milliseconds):
        def task():
            try:
                # 在这里添加您需要定时执行的任务代码
                self.ctl.update_msg("时间到，执行点击\n")
                self.ctl.startOrStop()
            except Exception as e:
                print(f"任务执行时发生错误: {e}")
            self.stop_task()

        # 添加任务，设置触发器为 date，第一个参数是任务函数，第二个参数是毫秒级延迟
        self.job_id = self.scheduler.add_job(task, 'date', run_date=run_date).id
        self.ctl.update_msg(f"已开启定时点击，将在 {hours}:{minutes}:{seconds}:{milliseconds} 执行循环点击\n")

    def stop_task(self):
        # 停止当前任务
        if self.job_id:
            if self.scheduler.get_job(self.job_id):
                self.scheduler.remove_job(self.job_id)
                self.ctl.update_msg("定时任务已取消\n")
            else:
                self.ctl.update_msg("任务不存在或已执行完毕\n")
        else:
            self.ctl.update_msg("没有任务正在运行\n")

    def __tk_button_search(self,parent):
        btn = Button(parent, text="查询", takefocus=False,command=self.ctl.searchLoc)
        btn.place(x=232, y=177, width=40, height=30)
        return btn
    def __tk_label_locMsg1(self, parent):
        label = Label(parent, text="第",anchor="center")
        label.place(x=275, y=177, width=40, height=30)
        return label
    def __tk_input_loc(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=313, y=177, width=270, height=30)
        return ipt
    def __tk_label_locMsg2(self, parent):
        label = Label(parent, text="个位置",anchor="center")
        label.place(x=575, y=177, width=60, height=30)
        return label

    # 最小化代码
    def on_close(self):
        self.ctl.on_close()
    def minimize_to_tray(self):
        self.withdraw()  # 隐藏窗口
        if not self.tray_icon:
            self.ctl.create_tray_icon()

class Win(WinGUI):
    def __init__(self, controller):
        self.ctl = controller
        super().__init__()
        # self.__event_bind()
        self.__style_config()
        self.ctl.init(self)
        self.ctl.loadOp()
        # 显示雷霆战机点位
        # self.ctl.showLocation()
    # def __event_bind(self):
    #     self.tk_button_clearAll.bind('<Button>',self.ctl.clear)
    #     self.tk_button_startOrStop.bind('<Button>',self.ctl.startOrStop)
    #     self.bind('<KeyPress>', self.ctl.on_key_press)  # 绑定F6键
    #     pass
    def __style_config(self):
        pass
if __name__ == "__main__":
    controller = Controller()
    win = WinGUI(controller)
    win.mainloop()
