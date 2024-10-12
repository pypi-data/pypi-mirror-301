#!/usr/bin/env python
# coding: utf-8

# 第一部分：程序说明###################################################################################
# coding=utf-8
# 药械不良事件工作平台
# 开发人：蔡权周

# 第二部分：导入基本模块及初始化 ########################################################################
 
import tkinter as Tk
from tkinter import ttk,Menu,Frame,Canvas,StringVar,LEFT,RIGHT,TOP,BOTTOM,BOTH,Y,X,YES,NO,DISABLED,END,Button,LabelFrame,GROOVE, Toplevel,Label,Entry,Scrollbar,Text, filedialog, dialog, PhotoImage
import tkinter.font as tkFont
from tkinter.messagebox import showinfo
from tkinter.scrolledtext import ScrolledText
import os
import pip

import pandas as pd  
 




pip.main(['install', 'adrmdr'])
pip.main(['install', 'pinggutools'])
pip.main(['install', 'treadtools'])
pip.main(['install', 'easyformstat'])




def update_software(package_name):
    # 检查当前安装的版本
    print("正在检查更新...") 
    pip.main(['install', package_name, '--upgrade'])
    print("\n更新操作完成，您可以开展工作。")



def load_app(package_name):
	file_path = pd.__file__
	update_software(package_name)
	package_names=package_name+".py"
	current_directory =str(os.path.dirname(file_path)).replace("pandas",package_name)
	file_path = os.path.join(current_directory, package_names)
	root.destroy()
	os.system(f"python {file_path}")
		
if __name__ == '__main__':
	

	root = Tk.Tk()
	root.title("数据统计工作平台")

	sw_root = root.winfo_screenwidth()
	# 得到屏幕宽度
	sh_root = root.winfo_screenheight()
	# 得到屏幕高度
	ww_root = 700
	wh_root = 620
	# 窗口宽高为100
	x_root = (sw_root - ww_root) / 2
	y_root = (sh_root - wh_root) / 2
	root.geometry("%dx%d+%d+%d" % (ww_root, wh_root, x_root, y_root))
	root.configure(bg="steelblue")  # royalblue

	try:
		frame0 = ttk.Frame(root, width=90, height=20)
		frame0.pack(side=LEFT)
		
		B_open_files1 = Button(
			frame0,
			text="药械妆不良反应报表统计工具\n（适用于全字段标准数据）",
			bg="steelblue",
			fg="snow",
			height=2,
			width=30,
			font=("微软雅黑", 12),
			relief=GROOVE,
			activebackground="lightsteelblue",
			command=lambda:load_app('adrmdr'),
		)
		B_open_files1.pack()
			
		

		B_open_files2 = Button(
			frame0,
			text="阅易评报告表质量评估工具\n（适用于全字段标准数据）",
			bg="steelblue",
			fg="snow",
			height=2,
			width=30,
			font=("微软雅黑", 12),
			relief=GROOVE,
			activebackground="lightsteelblue",
			command=lambda:load_app('pinggutools'),
		)
		B_open_files2.pack()
		

		B_open_files2 = Button(
			frame0,
			text="易析数据分析工具\n（适用于个性化数据）",
			bg="steelblue",
			fg="snow",
			height=2,
			width=30,
			font=("微软雅黑", 12),
			relief=GROOVE,
			activebackground="lightsteelblue",
			command=lambda:load_app('easyformstat'),
		)
		B_open_files2.pack()


		B_open_files2 = Button(
			frame0,
			text="医疗器械警戒趋势分析工具\n（仅供器械警戒试点使用）",
			bg="steelblue",
			fg="snow",
			height=2,
			width=30,
			font=("微软雅黑", 12),
			relief=GROOVE,
			activebackground="lightsteelblue",
			command=lambda:load_app('treadtools'),
		)
		B_open_files2.pack()

	except KEY:
		pass


	##############提示框########################
	text = ScrolledText(root, height=400, width=400, bg="#FFFFFF")
	text.pack(padx=5, pady=5)
	text.insert(
		END, "\n\n\n\n\n\n\n\n\n\n\n 本工作站适用于整理和分析国家医疗器械不良事件信息系统、国家药品不良反应监测系统和国家化妆品不良反应监测系统中导出的监测数据。如您有改进建议，请联系蔡老师 411703730(QQ或微信)。\n\n本平台所有工具仅支持Python 3.8.10运行环境，如出现不兼容情况，请下载安装运行环境。\n地址：https://www.123pan.com/s/D9rSVv-xB6nH.html"
	)
	text.insert(END, "\n\n")



	root.mainloop()
	print("done.")
