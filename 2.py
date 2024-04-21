import os
import re
import sys  # 导入sys模块
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox
)
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette
from PyQt5.QtCore import Qt
from PyQt5.Qt import QStyleFactory

# 定义提取汉字的正则表达式
chinese_pattern = re.compile(r'[\u4e00-\u9fff]')

# 获取当前时间
current_time = datetime.now().strftime("%Y%m%d%H%M%S")

class ChineseCharacterExtractor(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("汉字提取工具")
        self.setGeometry(100, 100, 400, 200)

        # 创建和布局控件
        self.input_folder_label = QLabel("输入文件夹:")
        self.input_folder_entry = QLineEdit()
        self.input_folder_button = QPushButton("选择文件夹", clicked=self.select_input_folder)

        self.output_folder_label = QLabel("输出文件夹:")
        self.output_folder_entry = QLineEdit()
        self.output_folder_button = QPushButton("选择文件夹", clicked=self.select_output_folder)

        self.extract_button = QPushButton("提取汉字并保存", clicked=self.extract_and_display)

        input_folder_layout = QHBoxLayout()
        input_folder_layout.addWidget(self.input_folder_label)
        input_folder_layout.addWidget(self.input_folder_entry)
        input_folder_layout.addWidget(self.input_folder_button)

        output_folder_layout = QHBoxLayout()
        output_folder_layout.addWidget(self.output_folder_label)
        output_folder_layout.addWidget(self.output_folder_entry)
        output_folder_layout.addWidget(self.output_folder_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(input_folder_layout)
        main_layout.addLayout(output_folder_layout)
        main_layout.addWidget(self.extract_button)

        self.setLayout(main_layout)

    def select_input_folder(self):
        input_folder_path = QFileDialog.getExistingDirectory(self, "选择输入文件夹")
        self.input_folder_entry.setText(input_folder_path)

    def select_output_folder(self):
        output_folder_path = QFileDialog.getExistingDirectory(self, "选择输出文件夹")
        self.output_folder_entry.setText(output_folder_path)

    def extract_chinese_characters(self, input_folder_path, output_folder_path):
        # 存储所有汉字的集合
        chinese_characters = set()

        # 遍历文件夹下的所有.md、.html、.txt、.json、.xml、.css文件
        allowed_extensions = (".md", ".html", ".txt", ".json", ".xml", ".css")
        for root, dirs, files in os.walk(input_folder_path):
            for file in files:
                if file.endswith(allowed_extensions):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # 使用正则表达式提取汉字并添加到集合中
                        chinese_characters.update(re.findall(chinese_pattern, content))

        # 去除重复的汉字
        unique_chinese_characters = list(chinese_characters)

        # 将汉字按照要求横排显示，不间隔
        output_content = ''.join(unique_chinese_characters)

        # 将提取后的汉字内容写入txt文本
        output_file_path = os.path.join(output_folder_path, f"{current_time}.txt")
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(output_content)

        # 提取完成后弹出提示框
        msg_box = QMessageBox()
        msg_box.setWindowTitle("提取完成")
        msg_box.setText("汉字提取完成！")
        msg_box.exec()

    def extract_and_display(self):
        input_folder_path = self.input_folder_entry.text()
        output_folder_path = self.output_folder_entry.text()
        self.extract_chinese_characters(input_folder_path, output_folder_path)

    def resource_path(self, relative_path):  # 将resource_path函数定义在类内部
        """将相对路径转为exe运行时资源文件的绝对路径"""
        if getattr(sys, 'frozen', False):  # 是否打包为exe
            base_path = sys._MEIPASS  # exe运行时的临时目录路径
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    app = QApplication([])
    app.setStyle(QStyleFactory.create("Fusion"))  # 使用 Fusion 风格

    font = QFont("Arial", 10)
    app.setFont(font)

    # 创建窗口
    window = ChineseCharacterExtractor()

    # 设置应用程序图标
    icon_path = window.resource_path("C:/Users/Administrator/Desktop/dabao/favicon.ico")  # 使用resource_path函数设置图标路径
    app.setWindowIcon(QIcon(icon_path))
    
    # 设置 macOS 风格的调色板
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(236, 236, 236))  # 窗口背景色
    # ... 其他调色板设置 ...

    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))  # 高亮文本颜色
    app.setPalette(palette)

    window.show()

    app.exec_()
