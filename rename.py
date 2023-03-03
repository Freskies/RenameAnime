import glob
import pathlib
import os


class Rename:

	@staticmethod
	def get_path_of_file(file_path: str) -> str:
		"""
		Get the path of the file
		:param file_path: absolute path of the file
		:return: the path of the folder
		"""
		return '\\'.join(file_path.split('\\')[:-1])

	@staticmethod
	def get_names_from_name_file(path: str) -> list:
		"""
		Get lines from file
		it deletes the last character in every line ('\n')
		:param path: the absolute path of the file
		:return: list of lines
		"""
		with open(f"{path}/names.txt", 'r', encoding = 'utf-8') as f:
			lines = f.readlines()

		return [line[:-1] for line in lines]

	@staticmethod
	def legal_line(line: str) -> bool:
		"""
		Check if the line is legal
		the line is legal when every char is in legal_char.txt
		:rtype: object
		:param line: the line to check
		:return: true if the line is legal
		"""
		if len(line) < 1:
			return False

		with open("legal_char.txt", 'r', encoding = 'utf-8') as f:
			legal_char = f.read()

		for c in line:
			if not c.lower() in legal_char:
				return False

		return True

	@staticmethod
	def exist_file(path: str) -> bool:
		"""
		Check if the file exist
		:rtype: object
		:param path: absolute path of the file
		:return: true if the file exist
		"""
		try:
			Rename.get_names_from_name_file(path)
			return True
		except FileNotFoundError:
			return False
		except EnvironmentError:
			return False

	@staticmethod
	def check_char(path: str) -> list[str]:
		"""
		Check if every char in names.txt are legal
		:param path: absolute path of the file
		:return: a list of illegal lines
		"""
		lines = Rename.get_names_from_name_file(path)

		error = list()

		for line in lines:
			if not Rename.legal_line(line):
				error.append(line)

		return error

	@staticmethod
	def get_hierarchy(path: str) -> list:
		"""
		Get the hierarchy of the folder in alphabetic order
		take first all the files in sub-folders and then the files in the folder
		remove the names.txt file
		:param path: absolute path of the folder
		:return: a list of path of all the files in the folder
		"""
		files = glob.glob(f"{path}/*.*")
		try:
			files.remove(f"{path}\\names.txt")
		except ValueError:
			pass
		folders = glob.glob(f"{path}/*")
		folders.reverse()

		for folder in folders:
			files = Rename.get_hierarchy(folder) + files

		return files

	@staticmethod
	def check_lines(path: str) -> bool:
		"""
		Check if the number of line in names.txt is equal to the number of files in the folder
		:rtype: bool
		:param path: absolute path of the file
		:return: true if are the same
		"""
		files = Rename.get_hierarchy(path)
		names = Rename.get_names_from_name_file(path)

		return len(files) == len(names)

	@staticmethod
	def rename(path: str, names = None) -> None:
		"""
		Rename all the files in the folder
		format the number to have the correct number of digits
		:param names: the list of names (if it is None, it will take the names from names.txt)
		:param path: absolute path of the folder
		"""

		files = Rename.get_hierarchy(path)
		if names is None:
			names = Rename.get_names_from_name_file(path)

		number_of_digits = len(str(len(files)))

		def format_number(number: int) -> str:
			"""
			Format the number to have the correct number of digits
			:param number: the number to format
			:return: the formatted number
			"""
			return str(number).zfill(number_of_digits)

		for i, file in enumerate(files):
			new_name = f"{format_number(i + 1)} - {names[i].strip()}"
			new_dir = f"{Rename.get_path_of_file(file)}"
			suffix = pathlib.Path(file).suffix
			print(f"{file} -> {new_dir}\\{new_name}{suffix}")

			try:
				os.rename(file, f"{new_dir}\\{new_name}{suffix}")
				pass
			except FileExistsError:
				print("File already exist")

	@staticmethod
	def check_file_name_is_not_number_in_list(path: str, start_number: int) -> list[str]:
		"""
		Check if the file name is number,
		if it is, check if the number is in the list,
		if it is, add the number to the list
		:param start_number: the number to start rename
		:param path: absolute path of the file
		:return: a list of illegal lines
		"""
		files = glob.glob(f"{path}/*.*")
		final_number = start_number + len(files)

		error = list()

		for file in files:
			try:
				if int(file.split('\\')[-1].split('.')[0]) in range(start_number, final_number):
					error.append(file.split('\\')[-1])
			except ValueError:
				pass

		return error

	@staticmethod
	def rename_from_number(path: str, from_: int) -> None:
		"""
		Rename the files in the folder
		names start from from_
		:param path: absolute path of the folder
		:param from_: the number of the first file to rename
		"""
		files = Rename.get_hierarchy(path)

		for i, file in enumerate(files):
			new_name = f"{str(i + from_).zfill(len(str(len(files))))}"
			new_dir = f"{Rename.get_path_of_file(file)}"
			suffix = pathlib.Path(file).suffix
			print(f"{file} -> {new_dir}\\{new_name}{suffix}")
			os.rename(file, f"{new_dir}\\{new_name}{suffix}")
