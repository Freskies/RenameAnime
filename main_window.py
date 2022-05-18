from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLineEdit, QLabel, QMessageBox
from rename import Rename
from os import path as os_path


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		# window
		self.setWindowTitle("Rename Anime")
		self.setFixedSize(QSize(440, 240))

		# label
		self.l_path_input = QLabel(self)
		self.l_path_input.setText('Insert the Absolute path:')
		self.l_path_input.resize(QSize(200, 20))
		self.l_path_input.move(20, 20)

		# path
		self.path_input = QLineEdit(self)
		self.path_input.resize(QSize(400, 30))
		self.path_input.move(20, 50)

		# execute button
		self.button_execute = QPushButton("Execute", self)
		self.button_execute.clicked.connect(self.execute)
		self.button_execute.resize(QSize(190, 30))
		self.button_execute.move(20, 100)

		# info button
		self.button_info = QPushButton("Info", self)
		self.button_info.clicked.connect(lambda: self.info("info.html"))
		self.button_info.resize(QSize(190, 30))
		self.button_info.move(220, 100)

		# from number label
		self.l_from_number = QLabel(self)
		self.l_from_number.setText('From number:')
		self.l_from_number.resize(QSize(200, 20))
		self.l_from_number.move(20, 150)

		# from number
		self.from_number = QLineEdit(self)
		self.from_number.setText('1')
		self.from_number.resize(QSize(100, 30))
		self.from_number.move(20, 180)

		# execute from number button
		self.button_execute_from_number = QPushButton("Execute", self)
		self.button_execute_from_number.clicked.connect(self.execute_from_number)
		self.button_execute_from_number.resize(QSize(100, 30))
		self.button_execute_from_number.move(130, 180)

		# from number info button
		self.button_info_from_number = QPushButton("Info", self)
		self.button_info_from_number.clicked.connect(lambda: self.info("info_from_number.html"))
		self.button_info_from_number.resize(QSize(100, 30))
		self.button_info_from_number.move(240, 180)

		# when you press enter the line edit, the button is clicked
		self.path_input.returnPressed.connect(self.button_execute.click)

	def execute(self) -> None:
		"""
		Execute the rename process
		:rtype: None
		"""
		path = self.path_input.text()

		if not Rename.exist_file(path):
			with open("Messages/name_not_exist.html", "r") as f:
				self.pop_up(f.read())

		else:
			if Rename.check_lines(path):
				error = Rename.check_char(path)
				if len(error) > 0:
					with open("Messages/illegal_line.html", "r") as f:
						self.pop_up(f.read().format(error = str(error)))

				else:
					Rename.rename(path)
					print("Rename is done!")
			else:
				with open("Messages/number_of_line.html", "r") as f:
					self.pop_up(f.read())

	def execute_from_number(self) -> None:
		"""
		Execute the rename process from a number
		:rtype: None
		"""
		path = self.path_input.text()

		if os_path.exists(path):
			try:
				from_number = int(self.from_number.text())

				error = Rename.check_file_name_is_not_number_in_list(path, from_number)
				if len(error) > 0:
					with open("Messages/illegal_line.html", "r") as f:
						self.pop_up(f.read().format(error = str(error)))

				else:
					Rename.rename_from_number(path, from_number)
					print("Rename is done!")

			except ValueError:
				with open("Messages/input_number.html", "r") as f:
					self.pop_up(f.read())
		else:
			self.pop_up("The path is not exist!")

	@staticmethod
	def info(path: str) -> None:
		"""
		Show the info of the program
		Open a popup window
		:rtype: None
		"""
		msg = QMessageBox()
		msg.setWindowTitle("Info")

		with open(path, "r") as f:
			msg.setText(f.read())

		msg.exec()

	@staticmethod
	def pop_up(text) -> None:
		"""
		Show the text in a popup window
		:rtype: None
		"""
		msg = QMessageBox()
		msg.setWindowTitle("Alert!")
		msg.setText(text)
		msg.exec()
