import tkinter as tk
from tkinter import filedialog
import variable_container as vc
import api_work
import os
import urllib

background_color = 'light green'
def generateKey():
	def submitted(subRoot, subRoot2, ent, root):
		subRoot2.destroy()
		
		subRoot2 = tk.LabelFrame(subRoot, border=0)
		subRoot2.grid(padx=10, pady=10)
		
		tk.Label(subRoot2, text="Generating key....").grid()
		root.update()
		print("generating.....")
		#--------------------Key generation center--------------------------------------
		from selenium import webdriver
		
		options = webdriver.ChromeOptions()
		options.add_argument("headless")

		browser = webdriver.Chrome(options=options)
		browser.get("https://tinypng.com/developers")

		fnameObj = browser.find_element_by_name("fullName")
		emailObj = browser.find_element_by_name("mail")

		fnameObj.send_keys("Noone")

		emailObj.send_keys(ent.get())

		fnameObj.submit()

		browser.quit()
		# #-----------------------------------------------------------------------------
		subRoot2.grid_forget()
		tk.Label(subRoot2, text="Now, check your email for the key and paste it in the empty API field", height=5).grid(padx=10)
		print("Done")
		root.update()

	root = tk.Tk()

	root.title('Key Generator')
	subRoot = tk.LabelFrame(root, border=0)
	subRoot.grid(padx=10, pady=10)
	
	subRoot2 = tk.LabelFrame(subRoot, border=0)
	subRoot2.grid()

	tk.Label(subRoot2, text="Enter your email:").grid(row=1, column=1, padx=5, pady=5)
	ent = tk.Entry(subRoot2, width=30)
	ent.grid(row=1, column=2, padx=5)
	
	tk.Button(subRoot2, text='Submit', command=lambda: submitted(subRoot, subRoot2, ent, root), width=5).grid(row=2, columnspan=3)

	root.mainloop()


def reset_all_data():
	reset_image_list()
	reset_log_screen()
	entry.delete(0, tk.END)
	vc.optimization_number_entry.delete(0, tk.END)
	update_destination_path(False)
	height_entry.delete(0,tk.END)
	width_entry.delete(0,tk.END)


def update_destination_path(stat):
	
	def button_pressed():
		vc.destination_directory = catch_here.get()

		vc.files_log_dialog.insert(tk.END, '\nOutput image path updated to: ' + vc.destination_directory)
		temp_window.destroy()	

	if stat:
		temp_window = tk.Tk()
		temp_window.title('Set Output Path')
		tk.Label(temp_window, height = 3, text = 'Enter path to store images').pack(anchor = 'w')
		catch_here = tk.Entry(temp_window, width = 50, border = 2)
		catch_here.pack()
		catch_here.insert(0, os.getcwd())
		tk.Button(temp_window, height = 2, width = 10, text = 'Set Path', command = button_pressed).pack(pady = 10)
	else:
		try:
			vc.destination_directory = os.path.dirname(vc.var_images[0])
		except:
			raise
		vc.current_directory = os.getcwd()


def reset_log_screen():
	vc.files_log_dialog.delete(2.0,tk.END)

def reset_image_list():
	vc.var_images = None
	vc.files_log_dialog.insert(tk.END, '\nNo Images selected currently.. Select Images before begining optimization')
	entry.delete(0, tk.END)

def import_images():
	# update_compression_counter()
	vc.files_log_dialog.insert(tk.END, '\nAdding Images')
	vc.var_images = filedialog.askopenfilenames(parent = root, title = "Select your images", filetypes = (vc.filetypes))
	for i in vc.var_images:
		entry.insert(0, i + ',  ')
		vc.files_log_dialog.insert(tk.END, '\n' + 'Added Image:  ' + i)
		vc.files_log_dialog.update_idletasks()
	update_destination_path(False)

def update_extension_status():
	vc.files_log_dialog.insert(tk.END, '\n"' + vc.var_extension.get().upper() + '" selected as output format')

def optimizing_animation():
	pass 

def metadata_log_update(metadata_to_delete):
	if 	vc.metadata_list.get(metadata_to_delete)[1].get() == 1:
		vc.files_log_dialog.insert(tk.END, ('\n' + metadata_to_delete + '\'s metadata is marked to be deleted'))
	if 	vc.metadata_list.get(metadata_to_delete)[1].get() == 0:
		vc.files_log_dialog.insert(tk.END, ('\n' + metadata_to_delete + ' is unmarked and it\'s metadata now is to be preserved'))
'''
if __name__ == "__main__":
	rootPrime = tk.Tk()
	rootPrime.geometry('1125x700')
	rootPrime.configure(bg = background_color)
	rootPrime.title('Image Resizer')
	root = tk.LabelFrame(rootPrime, bg=background_color)
	root.grid(padx=10, pady=10)
	#----------------------------------------------GUI FROM HERE---------------------------------------------
	entry_frame = tk.LabelFrame(root, text = 'Add Images', height = 65, font = ' Arial, 13', bg = background_color)
	entry = tk.Entry(entry_frame, width = 50)
	entry.grid(row = 0, column = 0, sticky = 'ew', padx = 10)
	entry_button = tk.Button(entry_frame, text = 'Add Images', height = 1, width = 10, command = import_images).grid(row = 0, column = 1, pady = 5)
	entry_frame.grid(row = 0, column = 0, pady = 5)

	files_frame = tk.LabelFrame(root, text = 'Files Log', font = "Arial, 13", bg = background_color)
	vc.files_log_dialog = tk.Text(files_frame, width = 70, height = 35, bg = 'black', fg= 'light green')
	vc.files_log_dialog.insert(tk.END, '---------------------------Operation Log----------------------------')
	vc.files_log_dialog.grid(row = 0, column = 0)
	files_frame.grid(row = 1, column = 0, columnspan = 2, padx = 10)

	# Extension checkboxes
	output_file_frame = tk.LabelFrame(root, text = 'Output Format', bg = background_color)
	vc.var_extension = tk.StringVar()	
	for key, i in vc.extension_list.items():
		tk.Checkbutton(output_file_frame, text = key.upper(), onvalue = key, offvalue = None, variable = vc.var_extension, bg = background_color, command = update_extension_status).grid(row = i[0], column = i[1], padx = 2, pady = 2)
	output_file_frame.grid(row = 0, column = 1)

	# Left parent frame
	left_frame_wrapper = tk.LabelFrame(root, bg = background_color, border = 0)

	# Height and width options
	dimension_frame = tk.LabelFrame(left_frame_wrapper, text = 'Output file dimension', bg = background_color)
	vc.var_height = tk.IntVar()
	vc.var_width = tk.IntVar()
	tk.Label(dimension_frame, text = 'Height', bg = background_color).grid(row = 0, column = 0)
	tk.Label(dimension_frame, text = 'Width', bg = background_color).grid(row = 0, column = 1)
	height_entry = tk.Entry(dimension_frame, textvariable = vc.var_height)
	width_entry = tk.Entry(dimension_frame, textvariable = vc.var_width)
	height_entry.grid(row = 1, column = 0, padx = 5, pady = 5)
	width_entry.grid(row = 1, column = 1, padx = 5, pady = 5)

	dimension_frame.grid(row = 0, sticky = 'n')

	# Metadata options
	metadata_frame = tk.LabelFrame(left_frame_wrapper, text = 'Delete Image Metadata(Checked = Delete Metadata)', bg = background_color)	
	for key, i in vc.metadata_list.items():
		i[1] = tk.IntVar()
		tk.Checkbutton(metadata_frame, text = key.upper(), bg = background_color, variable = i[1], command = lambda param = key: metadata_log_update(param)).grid(row = i[0])
	metadata_frame.grid(row = 1, sticky = 'n', pady = 10)

	# Frame to provide API Key
	api_frame = tk.LabelFrame(left_frame_wrapper, text = 'API Key Field', bg = background_color)
	vc.api_entry = tk.Entry(api_frame, width = 50)
	vc.api_entry.grid(row=0)
	try:
		vc.api_entry.insert(0, vc.var_api_key)
		vc.files_log_dialog.insert(tk.END, '\nAdded API key: {}'.format(vc.api_entry.get()))
	except AttributeError:
		generateButton = tk.Button(api_frame, text='Generate API Key', command=generateKey, bg=background_color)
		generateButton.grid(row=1)
		vc.files_log_dialog.insert(tk.END, "\nInsert API key or generate one from the API Key Field....")
		pass
	vc.files_log_dialog.update_idletasks()
	api_frame.grid(row = 2)

	left_frame_wrapper.grid(row = 0, column = 2, rowspan = 2, sticky = 'n')
	# Left Parent frame ends


	# Left Bottom Buttons Frame
	bottom_frame = tk.LabelFrame(root, bg = background_color, border=0)
	tk.Button(bottom_frame, text = 'Reset Image List', height = 1, width = 20, command = reset_image_list).grid(row = 1, column = 0, padx = 5, pady = 5)
	tk.Button(bottom_frame, text = 'Reset All Data', height = 1, width = 20, command = reset_all_data).grid(row = 1, column = 1, padx = 5, pady = 5)
	tk.Button(bottom_frame, text = 'Reset Log Screen', height = 1, width = 20, command = reset_log_screen).grid(row = 2, column = 0, padx = 5, pady = 5)
	tk.Button(bottom_frame, text = 'Set Image Output Path', height = 1, width = 20, command =  lambda: update_destination_path(True)).grid(row = 2, column = 1, padx = 5, pady = 5)
	tk.Button(bottom_frame, text = "Optimize for one time", height = 3, width = 30, command = lambda: api_work.convert_the_images(1)).grid(row = 3, column = 0, pady = 10, columnspan = 2)	
	tk.Button(bottom_frame, text = "Optimize Multiple Times", height = 3, width = 30, command = lambda: api_work.convert_the_images(int(vc.optimization_number_entry.get()))).grid(row = 4, column = 0, pady = 10, columnspan = 2)
	
	tk.Label(bottom_frame, width = 30, height = 2, text = 'Enter the no of optimizations', anchor = 'n', bg = background_color).grid(row = 6, columnspan = 2)
	vc.optimization_number_entry = tk.Entry(bottom_frame, width = 15, border = 1)
	vc.optimization_number_entry.grid(row = 5, columnspan = 2, sticky = 's')
	
	compression_count = tk.LabelFrame(bottom_frame, text = 'Compression Counter', bg = background_color)
	vc.compression_status_container = tk.Text(compression_count, height = 4, width = 45, bg = 'black', fg = 'light green')
	vc.compression_status_container.pack()
	compression_count.grid(row = 0, columnspan = 2, pady = 10)
	bottom_frame.grid(row = 1, column = 2, padx = 5, pady = 5, sticky = 's')
	try:
		vc.update_compression_counter()
	except:
		vc.files_log_dialog.insert(tk.END, 'Something is wrong...\nCheck Internet Connection')
	root.mainloop()
'''
if __name__ == "__main__":
	generateKey()