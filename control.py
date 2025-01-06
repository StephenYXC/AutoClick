import pyautogui,time,logging,threading,keyboard,shelve
import tkinter as tk
from tkinter import messagebox,ttk

class Controller:
    # 导入UI类后，替换以下的 object 类型，将获得 IDE 属性提示功能
    ui: object
    # 初始化一个空列表来保存坐标点
    coordinates = []
    # coordinates = [(926,909),(976,909),(1011,910),(1115,498),(960,835),(959,896)]
    # 声明一个全局变量，用于控制循环的启动和停止
    is_running = False

    def __init__(self):
        pass
    def init(self, ui):
        """
        得到UI实例，对组件进行初始化配置
        """
        self.ui = ui
        self.bind_global_hotkeys()
        # TODO 组件初始化 赋值操作
    def clear(self):
        if messagebox.askyesno("确认", "是否清除所有数据？"):
            global click_count,is_running,coordinates
            # 清空已获取的坐标点
            self.ui.tk_input_nextCycleTime.delete(0, tk.END)
            self.ui.tk_input_nextTime.delete(0, tk.END)
            # self.ui.tk_input_deleteNum.delete(0, tk.END)
            self.ui.tk_input_loc.delete(0, tk.END)
            self.ui.tk_input_loc.insert(0, self.ui.placeholder_text2)  # 插入占位符文本
            self.ui.tk_input_addNum.delete(0, tk.END)
            self.ui.tk_input_x.delete(0, tk.END)
            self.ui.tk_input_y.delete(0, tk.END)
            self.ui.tk_input_date.delete(0, tk.END)
            self.ui.tk_input_date.insert(0, self.ui.placeholder_text)  # 插入占位符文本
            self.coordinates.clear()
            self.is_running = False
            self.click_count = 0  # 循环计数器
            self.locationNum = 0 # 点位数量
            # 清除循环信息
            self.ui.tk_text_msg.config(state='normal')
            self.ui.tk_text_msg.delete('1.0', tk.END)
            self.ui.tk_text_msg.config(state='disabled')
            # 清除位置信息
            self.ui.tk_text_locationMsg.config(state='normal')
            self.ui.tk_text_locationMsg.delete('1.0', tk.END)
            self.ui.tk_text_locationMsg.config(state='disabled')
            # 清空并删除已保存到文件里的数据
            messagebox.showinfo("信息", "所有数据已清空")

    click_count = 0  # 循环计数器
    # 启动或停止
    def startOrStop(self):
        global is_running
        if self.check_empty():
            # 如果两者都为空，则不执行任何操作
            messagebox.showwarning("警告", "时间和坐标列表都不能为空！\n")
            return
        if not self.is_running:
            self.is_running = True
            self.update_msg("-------启动连点,当前每 {} 秒点击一次-------\n".format(self.ui.tk_input_nextTime.get()))
            threading.Thread(target=self.startClickThread).start()  # 使用线程启动连点操作
        else:
            self.is_running = False
            self.update_msg("停止连点,若已开启连点，则等待一轮连点结束\n")

    def startClickThread(self):
        global click_count, is_running
        seconds1 = float(self.ui.tk_input_nextCycleTime.get())
        seconds2 = float(self.ui.tk_input_nextTime.get())
        while self.is_running:
            try:
                # 遍历coordinates列表中的每个坐标点
                for x, y in self.coordinates:
                    # 移动鼠标到坐标点(x, y)
                    pyautogui.moveTo(x, y)
                    # 模拟鼠标点击
                    pyautogui.click()
                    time.sleep(seconds2)
                # 一轮循环完成，增加计数器
                self.click_count += 1
                current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                self.update_msg(f"{current_time} 第 {self.click_count} 次循环结束\n距离下次循环还有 {seconds1} 秒\n--------------------------------------------")
                # 等待-秒
                time.sleep(seconds1)
            except pyautogui.FailSafeException:
                self.update_msg("操作取消，因为鼠标移动到了屏幕角落。\n")
                self.is_running = False
            except Exception as e:
                logging.error(f"发生错误：{e}")
                self.is_running = False

    def check_empty(self):
        # 检查entry1,entry2是否为空
        if self.ui.tk_input_nextCycleTime.get().strip() == "" or self.ui.tk_input_nextTime.get().strip() == "":
            return True
        if len(self.coordinates) == 0:
            return True
        return False

    def bind_global_hotkeys(self):
        # 使用 lambda 函数来忽略事件参数
        keyboard.add_hotkey('f5', lambda: self.clear())
        keyboard.add_hotkey('f6', lambda: self.print_mouse_position())
        keyboard.add_hotkey('f7', lambda: self.startOrStop())

    locationNum = 0
    def print_mouse_position(self):
        global locationNum, coordinates
        # 获取鼠标的x, y坐标
        x, y = pyautogui.position()
        if len(self.coordinates) != 0:
            self.locationNum = len(self.coordinates)
        self.coordinates.append((x, y))
        # 将坐标打印到指定的Text组件中
        self.update_localtionMsg(f"第{self.locationNum}个位置：{x} - {y}\n",0)
        self.update_msg(f"已添加第 {self.locationNum} 个位置：{x} - {y}\n")
        self.locationNum += 1

    def searchLoc(self):
        # input = self.ui.tk_input_loc.get().strip()
        if self.ui.tk_input_loc.get().strip() == "":
            self.update_msg(f"未填写需要查询的位置\n")
            return
        else:
            input_string = self.ui.tk_input_loc.get().strip().replace('，', ',')
            numbers = input_string.split(',')
            try:
                for number in numbers:
                    x, y = self.coordinates[int(number)]
                    # 移动鼠标到坐标点(x, y)
                    pyautogui.moveTo(x, y)
                    self.update_msg(
                        f"查询坐标值为 {int(number)} 的坐标，坐标点为 {x, y}，鼠标已移动到查询位置\n")
            except Exception as e:
                self.update_msg(
                    f"当前查询坐标值为 {numbers} 的坐标不存在\n")

    def update_msg(self,message_text):
        def safe_update():
            self.ui.tk_text_msg.config(state='normal')
            self.ui.tk_text_msg.insert(tk.END, message_text)
            self.ui.tk_text_msg.config(state='disabled')
            # 滚动到最底部
            self.ui.tk_text_msg.yview(tk.END)

        self.ui.after(0, safe_update)

    def update_localtionMsg(self, message_text,type):
        if type == 0:
            def safe_update():
                self.ui.tk_text_locationMsg.config(state='normal')
                self.ui.tk_text_locationMsg.insert(tk.END, message_text)
                self.ui.tk_text_locationMsg.config(state='disabled')
                # 滚动到最底部
                self.ui.tk_text_locationMsg.yview(tk.END)

            self.ui.after(0, safe_update)
        elif type == 1:
            # 清除位置信息
            self.ui.tk_text_locationMsg.config(state='normal')
            self.ui.tk_text_locationMsg.delete('1.0', tk.END)
            self.ui.tk_text_locationMsg.config(state='disabled')
            message = ""
            for idx, (x, y) in enumerate(self.coordinates):
                message += f"第{idx}个位置：{x} - {y}\n"
            # 一次性更新所有坐标信息
            self.update_localtionMsg(message, 0)

    def deleteOp(self):
        try:
            if self.ui.tk_input_addNum.get().strip() == "":
                messagebox.showwarning("警告", "删除坐标位置未填写！\n")
                return
            else:
                index = int(self.ui.tk_input_addNum.get().strip())
                self.update_msg(
                    f"已删除坐标值为 {index} 的坐标，坐标点为 {self.coordinates[index]}，位置已刷新\n")
                self.coordinates.pop(index)
                self.update_localtionMsg("",1)
        except Exception as e:
            print(e)
            messagebox.showwarning("警告", "出错了！\n")

    def addOp(self):
        if self.ui.tk_input_addNum.get().strip() == "" or self.ui.tk_input_x.get().strip() == "" or self.ui.tk_input_y.get().strip() == "":
            messagebox.showwarning("警告", "新增位置或坐标未填写！\n")
            return

        index = int(self.ui.tk_input_addNum.get().strip())
        x = int(self.ui.tk_input_x.get().strip())
        y = int(self.ui.tk_input_y.get().strip())
        if 0 <= index < len(self.coordinates):
            if messagebox.askyesno("坐标提示", f"当前位置已存在坐标,选择‘是’，\n"
                                               f"将替换位置为 {index} 的坐标值；选择‘否’，\n"
                                               f"则新增位置为 {index} 的坐标值，\n其余坐标顺延至下一坐标！\n"):
                self.coordinates[index] = (x, y)
                self.update_msg(
                    f"选择是：将替换为 {index} 的坐标值，坐标点为 {x} - {y}\n")
            else:
                self.coordinates.insert(index, (x, y))
                self.update_msg(
                    f"选择否：新增位置为 {index+1} 的坐标值，坐标点为 {x} - {y}，其余坐标顺延至下一坐标！\n")

        else:
            self.update_msg(f"所填位置 {index} 超出记录坐标点最大值，将新增坐标位置为： {len(self.coordinates)}，坐标点为 {x} - {y}\n")
            self.coordinates.insert(len(self.coordinates), (x, y))

        self.update_localtionMsg("", 1)

    def saveOp(self):
        # 保存缓存
        with shelve.open('cache.db') as db:
            db['coordinates'] = self.coordinates
            db['next_cycle_time'] = self.ui.tk_input_nextCycleTime.get().strip()
            db['next_time'] = self.ui.tk_input_nextTime.get().strip()
            db['timing'] = self.ui.tk_input_date.get().strip()
            self.update_msg(
                f"已保存信息\n")

    def loadOp(self):
        # 加载缓存
        with shelve.open('cache.db') as db:
            self.coordinates.extend(db.get('coordinates', []))
            self.ui.tk_input_nextCycleTime.insert(0,db.get('next_cycle_time', ""))
            self.ui.tk_input_nextTime.insert(0,db.get('next_time', ""))
            self.ui.tk_input_date.insert(0, db.get('timing', ""))
            if self.ui.tk_input_date.get().strip() == "":
                self.ui.tk_input_date.insert(0, self.ui.placeholder_text)  # 插入占位符文本
        self.update_localtionMsg("", 1)

    # 最小化代码
    def on_close(self):
        if messagebox.askyesno("关闭", "是否关闭程序？"):
            self.exit_app()
        else:
            return
    def exit_app(self):
        # 退出程序
        self.ui.destroy()
            # 雷霆战机点位
    # def showLocation(self):
    #     global locationNum
    #     for x, y in self.coordinates:
    #         self.locationNum += 1
    #         self.update_localtionMsg(f"第{self.locationNum}个位置：{x} - {y}\n")
