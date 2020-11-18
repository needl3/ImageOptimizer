import tinify as tf
import variable_container as vc
import shutil
import os
import time

def convert_the_images(optimizing_times):
	from GUI import tk
	if check_informations():
		pass
	else:
		return
	for i in range(1,optimizing_times+1):
		optimize_first()
		vc.files_log_dialog.insert(tk.END, '\nOptimized {} times\n'.format(i))

	vc.files_log_dialog.insert(tk.END, '\nFinished Optimizing Images\n\n')
	vc.update_compression_counter()
	vc.files_log_dialog.see('end')



def optimize_first():
	from GUI import tk
	
	vc.files_log_dialog.insert(tk.END, '\n\nOptimizing Images')
	vc.files_log_dialog.update_idletasks()

	vc.files_log_dialog.insert(tk.END, '\nHeight set as: ' + str(vc.var_height.get()))
	vc.files_log_dialog.insert(tk.END, '\nWidth set as: ' + str(vc.var_width.get()))
	
	for i in vc.var_images:
		
		source = tf.from_file(i)	
		
		# Delete Metadatas
		source.preserve(delete_metadata(source))
		vc.files_log_dialog.insert(tk.END, '\nDeleting Metadatas')

		if vc.var_height.get() != 0 and vc.var_width.get() != 0:
			# RESIZING IF DIMENTION IS MENTIONED
			print('\nResizing Image ' + i)
			vc.files_log_dialog.update_idletasks()
			source = source.resize(
			    method="fit",
			    width=vc.var_width.get(),
			    height=vc.var_height.get()
			)
			vc.files_log_dialog.insert(tk.END, '\nResizing and Compressing Image ' + i + ' succeeded...')

		source.to_file(i.split('.')[0] + "_optimized." + vc.var_extension.get())
		vc.files_log_dialog.see('end')
		
		try:
			shutil.move(i.split('.')[0] + "_optimized." + vc.var_extension.get(), vc.destination_directory)
		except:
			vc.files_log_dialog.insert(tk.END, '\nMoving images to given destination failed...\nCurrent location of optimized Images: {}'.format(os.path.dirname(vc.var_images[0])))
		vc.files_log_dialog.update_idletasks()

def delete_metadata(source):
	deleting_candidates = ''
	for keys, i in vc.metadata_list.items():
		if i[0] == None:
			deleting_candidates += keys + ','
	return deleting_candidates


def check_informations():
	from GUI import tk
	
	if vc.var_extension.get() == '':
		vc.files_log_dialog.insert(tk.END, '\nChoose an extension to file before begining to optimize')
		return False

	try:
		for i in vc.var_images:
			pass
	except:
		vc.files_log_dialog.insert(tk.END, '\nNo Images Added')
		return False
	
	try:
	  vc.files_log_dialog.insert(tk.END, '\nValidating API Key')
	  vc.files_log_dialog.update_idletasks()
	  
	  tf.key = vc.api_entry.get()
	  tf.validate()
	  
	except tf.Error:
	  vc.files_log_dialog.insert(tk.END, '\nAPI Key Authentication Failed. Try another API key or check Internet connection...')
	  vc.files_log_dialog.update_idletasks()
	  return False
	
	vc.files_log_dialog.insert(tk.END, '\nAPI Authentication Succeeded.')	
	vc.files_log_dialog.update_idletasks()
	  
	# If there is no api key stored it will grab api key from entry and store it in vc file
	try:
		tf.key = vc.var_api_key
	except AttributeError:
		with open('test_only_temp.py' ,'w') as file:
			file.write('var_api_key = \'' + vc.api_entry.get() + '\'\n')
			with open('variable_container.py', 'r') as original:
				file.write(original.read())
		with open('variable_container.py', 'w') as original:
			with open('test_only_temp.py', 'r') as to_be_copied:
				original.write(to_be_copied.read())
			os.remove('test_only_temp.py')
		vc.files_log_dialog.insert(tk.END, '\nAPI Key updated successfully')

	return True
