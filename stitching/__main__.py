from Tkinter import *
import tkFileDialog
import tkMessageBox
import bioformats
import bioformats.formatreader
import javabridge
import skimage.io
import skimage.util.montage
import math
import os
import os.path
import click
import numpy
import numpy.random
import matplotlib.pyplot as plt


class Stitching(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.parent = parent
		self.initUI()

	def initUI(self):
		self.parent.title("Stitching")
		self.config(bg = '#F0F0F0')
		self.pack(fill = BOTH, expand = 1)
		self.photo=PhotoImage(file="button.png")
		
		self.filename = ' '
		self.dirPath = ' '
		self.n_images = 0
		self.n_channels = 0
		self.reader = 0
		
        #create canvas1
		self.canvas1 = Canvas(self, relief = FLAT, background = "#D2D2D2",width = 500, height = 180)
		self.canvas1.place(x=20,y=20)
		
		self.button1 = Button(self.canvas1, text = "Open .cif file", command = self.read_cif)
		self.button1.configure(width = 18, height = 4, background = "#33B5E5")
		self.button1.place(x=30,y=60)
        
		self.label1 = Label(self.canvas1, text="Filename", fg='blue')
		self.label1.configure(width = 23, height = 2)
		self.label1.place(x=288,y=20)
        
		self.Text1 = Text(self.canvas1, height = 2,width=26, background = "#D2D2D2")
		self.Text1.config(state=DISABLED)
		self.Text1.place(x=288,y=40)
                
		self.label2 = Label(self.canvas1, text="Number of cells", fg='blue')
		self.label2.configure(width = 23, height = 2)
		self.label2.place(x=288,y=70)
        
		self.Text2 = Text(self.canvas1, height=2, width=26, background = "#D2D2D2")
		self.Text2.config(state=DISABLED)
		self.Text2.place(x=288,y=90)
      
		self.label3 = Label(self.canvas1, text="Number of channels", fg='blue')
		self.label3.configure(width = 23, height = 2)
		self.label3.place(x=288,y=120)    
   
		self.Text3 = Text(self.canvas1, height=2, width=26, background = "#D2D2D2")
		self.Text3.config(state=DISABLED)
		self.Text3.place(x=288,y=140) 
		
		
        #create canvas2
		self.canvas2 = Canvas(self, relief = FLAT, background = "#D2D2D2",width = 240, height = 240)
		self.canvas2.place(x=280,y=210)
		
		self.button4 = Button(self.canvas2, text = "Choose output directory", command = self.chooseDir)
		self.button4.configure(width = 20, height = 2, background = "#33B5E5")
		self.button4.place(x=28,y=10)
		
		self.Text4 = Text(self.canvas2, height = 2,width=26,background = "#D2D2D2")
		self.Text4.config(state=DISABLED)
		self.Text4.place(x=28,y=50)
		
		
		
		self.label5 = Label(self.canvas2, text="Choose channels", fg='blue')
		self.label5.configure(width = 13)
		self.label5.place(x=60,y=90)
		
		self.entry1 = Entry(self.canvas2,width = 13)
		self.entry1.place(x = 60,y=108)
 
		self.button5 = Button(self.canvas2, image = self.photo, command = self.messageBox1, height = 30,width = 30)
		self.button5.place(x=180,y=90)
			
		self.label6 = Label(self.canvas2, text="Grid size", fg='blue')
		self.label6.configure(width = 13)
		self.label6.place(x=60,y=135)
		
		self.entry2 = Entry(self.canvas2,width = 13)
		self.entry2.place(x = 60,y=153)
		
		self.button6 = Button(self.canvas2, image = self.photo, command = self.messageBox2, height = 30,width = 30)
		self.button6.place(x=180,y=135)
		
		self.button2 = Button(self.canvas2, text = "Generate tiled .tif", command = self.generate_tifs)
		self.button2.configure(width = 20, height = 3, background = "#33B5E5")
		self.button2.place(x=30,y=180)
		
        #create canvas3
		self.canvas3 = Canvas(self, relief = FLAT, background = "#D2D2D2",width = 240, height = 240)
		self.canvas3.place(x=20,y=210)
		
		self.label8 = Label(self.canvas3, text="Select cell", fg='blue')
		self.label8.configure(width = 13)
		self.label8.place(x=70,y=40)
		
		self.label9 = Label(self.canvas3, text="Select channel", fg='blue')
		self.label9.configure(width = 13)
		self.label9.place(x=70,y=120)
		
		self.entry4 = Entry(self.canvas3,width = 13)
		self.entry4.place(x = 70,y=58)
		
		self.entry5 = Entry(self.canvas3,width= 13)
		self.entry5.place(x = 70,y=138) 
		
		self.button3 = Button(self.canvas3, text = "Display image", command = self.display_cell)
		self.button3.configure(width = 20, height = 3, background = "#33B5E5")
		self.button3.place(x=30,y=180)
		
		
	def messageBox1(self):
		text = "Select channel numbers. Separate each channel or range with a comma (such as 1,3,5-7). Per default all channels will be used."
		tkMessageBox.showinfo("", text)
		
	def messageBox2(self):
		text = "Enter the number of cells per row and per column in the output image. The default value for the grid size is 32 and will yield output images with 32x32 cells per montage. The maximum possible value is 100."
		tkMessageBox.showinfo("", text)
		
	def chooseDir(self):
		self.dirPath = tkFileDialog.askdirectory()
		self.Text4.config(state=NORMAL)
		self.Text4.delete(1.0, END)
		self.Text4.insert(END,self.dirPath)
		self.Text4.config(state=DISABLED)
		
	def read_cif(self):
		old_file = self.filename
		self.filename = tkFileDialog.askopenfilename()
		if type(self.filename) != tuple:
			if self.filename.lower().endswith('.cif'):
				try:
					self.Text1.config(state=NORMAL)
					self.Text2.config(state=NORMAL)
					self.Text3.config(state=NORMAL)
					self.Text1.delete(1.0, END)
					self.Text2.delete(1.0, END)
					self.Text3.delete(1.0, END)
					self.entry1.delete(0,END)
					self.entry2.delete(0,END)
			
					javabridge.start_vm(class_path=bioformats.JARS, max_heap_size='8G')
					self.reader = bioformats.formatreader.get_image_reader("tmp", path=self.filename)
					self.n_images = int(0.5*javabridge.call(self.reader.metadata, "getImageCount", "()I"))
					self.n_channels = javabridge.call(self.reader.metadata, "getChannelCount", "(I)I", 0)

					#check, whether the .cif file is ok
					if self.n_images == 0 or self.n_channels == 0:
						raise ValueError('There is nothing in the file')
					self.Text1.insert(END,self.filename)
					self.Text1.config(state=DISABLED)
					self.Text2.insert(END,self.n_images)
					self.Text2.config(state=DISABLED)
					self.Text3.insert(END,self.n_channels)
					self.Text3.config(state=DISABLED)
					self.entry1.insert(0,'1-'+str(self.n_channels))
					self.entry2.insert(0,32)
				except:
					tkMessageBox.showinfo("Error", "Please choose a correct .cif file.")
			if self.filename and not self.filename.lower().endswith('.cif'):
				tkMessageBox.showinfo("Error", "Please choose a .cif file.")
			
	def generate_tifs(self):
		if self.reader != 0:
			if type(self.dirPath) != tuple:
				if os.path.isdir(self.dirPath):
					output = self.dirPath
				
					try:
						chooseChannels = self.entry1.get()
						channels = []
						t = chooseChannels.split(',')
						for k in t:
							r = k.split('-')
							for e in range(int(r[0]),int(r[-1])+1):
								channels.append(e-1)
								channels = list(set(channels))
						n_channels = int(javabridge.call(self.reader.metadata, "getChannelCount", "(I)I", 0))
						if max(channels) < n_channels and min(channels) >= 0:
							try:
								grid_size = int(self.entry2.get())
								if grid_size < 1 or grid_size > 100:
									raise ValueError
								
								self.stitch(self.reader, output,grid_size, 55, channels)
								tkMessageBox.showinfo("", "Tiled .tif images successfully generated.")
												
							except ValueError:
								tkMessageBox.showinfo("Error", "Please enter a positive integer number between 1 and 100 as grid size.")

						else:
							tkMessageBox.showinfo("Error", "Please choose correct channels.")
					except:
						tkMessageBox.showinfo("Error", "Please choose correct channels.")
				else:
					tkMessageBox.showinfo("Error", "Please choose an output directory.")
			else:
				tkMessageBox.showinfo("Error", "Please choose an output directory.")
		else:
			tkMessageBox.showinfo("Error", "Please choose a .cif file.")
					
	def display_cell(self):
		flag = False
		if self.reader != 0:
			try:
				selected_cell = int(self.entry4.get())
				selected_chan = int(self.entry5.get())
				if selected_cell < 1 or selected_cell > self.n_images or selected_chan < 1 or selected_chan > self.n_channels:
					raise ValueError
				image = self.__pad_or_crop(self.reader.read(c=selected_chan-1, series=2*(selected_cell-1)), 55)
				maxi = numpy.amax(image)
				mini = numpy.amin(image)
				'''
				f: [min,max] -> [0,255], f = m*x+n
				'''
				image = (255.0/(maxi-mini))*image - 255*mini/(maxi-mini)
				flag = True
			except:
				tkMessageBox.showinfo("Error", "Please select an available cell and channel.")
			if flag:
				plt.imshow(image, cmap='gray')
				plt.show()

			

		else:
			tkMessageBox.showinfo("Error", "Please choose a .cif file.")
	
	def stitch(self,reader, output, montage_size, image_size, channels = []):
		
		n_images = int(0.5*javabridge.call(reader.metadata, "getImageCount", "()I"))
		n_channels = javabridge.call(reader.metadata, "getChannelCount", "(I)I", 0)
		
		chunk_size = montage_size**2
		n_chunks = self.__compute_chunks(n_images/2,montage_size)
		
		if len(channels) == 0:
			channels = range(n_channels)
		
		for channel in channels:
			for i in range(n_chunks):
				try:
					images = [reader.read(c=channel, series=image) for image in range(n_images)[::2][i*chunk_size:(i+1)*chunk_size]]
				except javabridge.jutil.JavaException:
					break
				
				images = [self.__pad_or_crop(image, image_size) for image in images]
				montage = skimage.util.montage.montage2d(numpy.asarray(images), 0, grid_shape = (montage_size,montage_size))
				
				if i == (n_chunks-1):
					montage = self.__pad_to_same_chunk_size(montage, image_size, montage_size)
					
				skimage.io.imsave(os.path.join(output, "ch{:d}Im{:d}.tif".format(channel + 1,i+1)), montage)			
			
	def __pad_or_crop(self,image, image_size):
		bigger = max(image.shape[0], image.shape[1], image_size)

		pad_x = float(bigger - image.shape[0])
		pad_y = float(bigger - image.shape[1])

		pad_width_x = (int(math.floor(pad_x / 2)), int(math.ceil(pad_x / 2)))
		pad_width_y = (int(math.floor(pad_y / 2)), int(math.ceil(pad_y / 2)))
		sample = image[image.shape[0]/2-4:image.shape[0]/2+4, :8]

		std = numpy.std(sample)

		mean = numpy.mean(sample)

		def normal(vector, pad_width, iaxis, kwargs):
			vector[:pad_width[0]] = numpy.random.normal(mean, std, vector[:pad_width[0]].shape)
			vector[-pad_width[1]:] = numpy.random.normal(mean, std, vector[-pad_width[1]:].shape)
			return vector

		if bigger == image_size:
			return numpy.pad(image, (pad_width_x, pad_width_y), normal)
		else:
			if bigger == image.shape[0]:
				temp_image = numpy.pad(image, (pad_width_y), normal)
			else:
				temp_image = numpy.pad(image, (pad_width_x), normal)
		return temp_image[(bigger - image_size)/2:(bigger + image_size)/2,(bigger - image_size)/2:(bigger + image_size)/2]

	def __pad_to_same_chunk_size(self,small_montage, image_size, montage_size):
		pad_x = float(montage_size*image_size - small_montage.shape[0])
		pad_y = float(montage_size*image_size - small_montage.shape[1])
		npad = ((0,int(pad_y)), (0,int(pad_x)))
		return numpy.pad(small_montage, pad_width=npad, mode='constant', constant_values=0)
    	
	def __compute_chunks(self,n_images, montage_size):
		def remainder(images, groups):
			return (images - groups * (montage_size ** 2))

		n_groups = 1
		while remainder(n_images, n_groups) > 0:
			n_groups += 1
		return n_groups
		

@click.command()
@click.option("-image", type=click.Path(exists=True))
@click.option("-output", type=click.Path(exists=False))
@click.option("--image-size", default=55)
@click.option("--montage-size", default=30)
	
def main(image,output,image_size, montage_size):
	root = Tk()
	root.geometry('540x470+10+50')
	app = Stitching(root)
	if image == None:

		root.protocol("WM_DELETE_WINDOW", on_closing)
		img = PhotoImage(file='icon.png')
		root.tk.call('wm', 'iconphoto', root._w, img)
		app.mainloop()
	else:
		try:
			javabridge.start_vm(class_path=bioformats.JARS, max_heap_size='8G')
			try:
				os.mkdir(output)
			except:
				pass
			reader = bioformats.formatreader.get_image_reader("tmp", path=image)
			app.stitch(reader, output, montage_size,image_size)
			javabridge.kill_vm()
		except:
			pass
    
def on_closing():
    if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
        try:
            javabridge.kill_vm()
        finally:
            quit()
			
if __name__ == '__main__':
    main()
