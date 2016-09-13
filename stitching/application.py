# import matplotlib
# import skimage.io
# import tkinter
# import tkinter.filedialog
#
# matplotlib.use("TkAgg")
#
#
# class Application:
#     def __init__(self, master):
#         self.master = master
#
#         master.title("Stitching")
#
#         menu = tkinter.Menu(root)
#
#         file_menu = tkinter.Menu(menu, tearoff=0)
#
#         file_menu.add_command(label="Open…", command=self.open)
#
#         file_menu.add_separator()
#
#         file_menu.add_command(label="Save As…", command=self.save_as)
#
#         file_menu.add_command(label="Export As…", command=self.export_as)
#
#         menu.add_cascade(label="File", menu=file_menu)
#
#         master.config(menu=menu)
#
#         self.image = None
#
#         self.photo = None
#
#     def open(self):
#         filename = tkinter.filedialog.askopenfilename()
#
#         self.image = skimage.io.imread(filename)
#
#         self.photo = self.image
#
#     def save_as(self):
#         filename = tkinter.filedialog.asksaveasfilename()
#
#         skimage.io.imsave(filename, self.image)
#
#     def export_as(self):
#         filename = tkinter.filedialog.asksaveasfilename()
#
#         skimage.io.imsave(filename, self.image)
#
# root = tkinter.Tk()
#
# application = Application(root)
#
# root.mainloop()

import matplotlib
matplotlib.use('TkAgg')

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
import skimage.data


from matplotlib.figure import Figure

import sys

if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

root = Tk.Tk()

root.wm_title("Embedding in TK")

image = skimage.data.camera()

figure, axis = matplotlib.pyplot.subplots(
    ncols=1
)

axis.imshow(image)

axis.set_axis_off()

canvas = FigureCanvasTkAgg(figure, master=root)

canvas.get_tk_widget().pack()

Tk.mainloop()
