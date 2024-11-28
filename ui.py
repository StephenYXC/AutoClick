"""
本代码由[Tkinter布局助手]生成
官网:https://www.pytk.net
QQ交流群:905019785
在线反馈:https://support.qq.com/product/618914
"""
import random
from tkinter import *
from tkinter.ttk import *
class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        # 设置窗口图标
        self.set_icon('.\\config\\click.png')  # 替换为您的图标文件路径
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
    def __win(self):
        self.title("自动连点器 V2.0")
        # 设置窗口大小、居中
        width = 641
        height = 400
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
    def __tk_label_m2sokmro(self,parent):
        label = Label(parent,text="====================按下F6获取当前鼠标坐标====================",anchor="center", )
        label.place(x=0, y=10, width=640, height=30)
        return label
    def __tk_label_m2soln9w(self,parent):
        label = Label(parent,text="- 距离下一个循环时间：",anchor="center", )
        label.place(x=232, y=44, width=170, height=30)
        return label
    def __tk_input_nextCycleTime(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=403, y=44, width=167, height=30)
        return ipt
    def __tk_label_m2somc08(self,parent):
        label = Label(parent,text="- 距离下一个点击时间：",anchor="center", )
        label.place(x=232, y=78, width=170, height=30)
        return label
    def __tk_input_nextTime(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=403, y=78, width=167, height=30)
        return ipt
    def __tk_text_locationMsg(self,parent):
        text = Text(parent, state='disabled')
        text.place(x=9, y=44, width=220, height=343)
        return text
    def __tk_text_msg(self,parent):
        text = Text(parent, state='disabled')
        text.place(x=232, y=147, width=402, height=240)
        return text
    def __tk_label_m3z74nqu(self,parent):
        label = Label(parent,text="s/秒",anchor="center", )
        label.place(x=577, y=44, width=51, height=63)
        return label
    def __tk_button_clearAll(self,parent):
        btn = Button(parent, text="清空（F5）", takefocus=False,command=self.ctl.clear)
        btn.place(x=232, y=113, width=199, height=30)
        return btn
    def __tk_button_startOrStop(self,parent):
        btn = Button(parent, text="启动/停止（F7）", takefocus=False,command=self.ctl.startOrStop)
        btn.place(x=435, y=113, width=199, height=30)
        return btn

class Win(WinGUI):
    def __init__(self, controller):
        self.ctl = controller
        super().__init__()
        # self.__event_bind()
        self.__style_config()
        self.ctl.init(self)
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