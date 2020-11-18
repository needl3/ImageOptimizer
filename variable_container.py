'''
Created this extra file to store variables used by both files 
so that circular import won't happen
'''
import tkinter as tk
import tinify as tf


def update_compression_counter():
	try:
		compression_status_container.delete(0.0, tk.END)
		compression_counter_data['Current API:'] = var_api_key
		for key, i in compression_counter_data.items():
				compression_status_container.insert(0.0, key + '\t' + str(i) + '\n')
		compression_status_container.update_idletasks()
	except:
		compression_status_container.insert(tk.END, "No API key")

# Values of these keys are the row and column information
extension_list = {
	'png' : [0,0],
	'jpg':[0,1],
	'jpeg':[1,0],
	'webp':[1,1]
}


# Data Required for Image Compression
current_directory = ''
destination_directory = ''

var_height = None
var_width = None
var_extension = None
var_copyright = None
var_creation = None
var_location = None
var_output_path = 'Current path'

# Values are the row information and respective checkbox variables
metadata_list = {
	'copyright': [0, var_copyright],
	'location': [1, var_location],
	'creation': [2,var_creation]
}

# To Avoid Circular Import
files_log_dialog = None
api_entry  = None
optimization_number_entry = None
compression_status_counter = None

# List of File Types Supported
filetypes = [
	("PNG File",".png"),
	("JPG File",".jpg"),
	("JPEG File",".jpeg"),
	('WEBP File', '.webp')
]

try:
	tf.key = var_api_key
	tf.validate()
	compression_counter_data = {
		'Current Compression through API:\n': api_entry,
		'Compressions Done:': tf.compression_count,
		'Compressions Remaining:': 500-tf.compression_count
	}
except:
	print("No key")
