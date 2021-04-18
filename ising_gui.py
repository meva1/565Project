import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ROWS = 100
COLUMNS = 100

ROWS1 = 30
COLUMNS1 = 30

run_animation = False


class Ising(tk.Tk):

	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		container = ttk.Frame(self, width=800, height=1000)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}
		for F in (IsingAnimationPage, CritTempPage, HysteresisPage):
			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row=0, column=0, sticky="N,S,E,W")
		self.show_frame(IsingAnimationPage)

	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()
		
class IsingAnimationPage(tk.Frame):

	def random_grid(self):
		return np.random.choice([-1,1], size=(ROWS, COLUMNS))

	def updatefig(self,*args):
		global run_animation
		if run_animation:
			
			temp = self.temperature_slider.get()
			coupling = self.coupling_slider.get()
			magnetic = self.magnetic_slider.get()
			exp_dict = self.exponential_dict(magnetic, temp, coupling)
			self.spin_flip(self.ising_grid, magnetic, coupling, temp, exp_dict)			
			self.im.set_array(self.ising_grid)

		return self.im,

	def exponential_dict(self, magnetic, temp, coupling):
		exp_dict = {}
		spins = [-1,1]
		neighbor_sums = [-4,-2,0,2,4]
		for spin in spins:
			for neighbor_sum in neighbor_sums:
				exp = np.exp(-2*spin*(coupling*neighbor_sum + magnetic)/temp)
				exp_dict[(spin, neighbor_sum)] = exp
		return exp_dict
	

	def spin_flip(self, grid, magnetic, coupling, temp, exp_dict):
		for n in range(ROWS*COLUMNS):
			i = random.randint(0,ROWS-1)
			j = random.randint(0,COLUMNS-1)
			neighbor_sum = grid[(i+1)%ROWS,j]+grid[i-1,j]+grid[i,(j+1)%COLUMNS]+grid[i,j-1]
			spin = grid[i,j]
			pr = exp_dict[(spin, neighbor_sum)]
			change = np.random.rand(1)
			if np.minimum(1,pr) > change[0]:
				grid[i,j] = -1*grid[i,j]
		return grid
	
	def ising_animation_click(self):
		global run_animation
		if not run_animation:
			run_animation = True
		else:
			run_animation = False

	def switch_hysteresis_frame(self):
		global run_animation
		run_animation = False

		
	def switch_critical_frame(self):
		global run_animation
		run_animation = False

	def __init__(self, parent, controller):
		temp = 1.5
		coupling = 1
		magnetic = 0
		global run_animation
		self.controller = controller
		tk.Frame.__init__(self, parent,height=800, width=1000)
		label = ttk.Label(self, text="Ising Animation")
		label.place(relx = 0.5, rely=0)
		button1 = ttk.Button(self, text="Quit",command=lambda: quit())
		button1.place(relx = 0.2, rely=0.05)
		button2 = ttk.Button(self, text="Hysteresis Page", command=lambda: (controller.show_frame(HysteresisPage), self.switch_hysteresis_frame()))
		button2.place(relx = 0.4, rely=0.05)
		button3 = ttk.Button(self, text="Critical Temperature Page",command=lambda: (controller.show_frame(CritTempPage), self.switch_critical_frame()))
		button3.place(relx = 0.6, rely=0.05)

		ising_animation_button = tk.Button(self, text="Ising animation", command=self.ising_animation_click)
		ising_animation_button.place(relx = 0.05, rely = 0.2, relwidth = 0.15)

		self.temperature_slider = tk.Scale(self, from_=0.1, to=3.5,variable=temp, resolution=0.1, orient=tk.HORIZONTAL, label="Temperature", length=120, tickinterval=3.5, fg="blue")
		self.temperature_slider.place(relx = 0.25, rely = 0.2)
		self.temperature_slider.set(1.5)

		self.coupling_slider = tk.Scale(self, from_=-1.0, to=1.0,variable=coupling, resolution=0.1, orient=tk.HORIZONTAL, label="Coupling Constant", length=120, tickinterval=1.0, fg="purple")
		self.coupling_slider.place(relx = 0.5, rely = 0.2)
		self.coupling_slider.set(1.0)

		self.magnetic_slider = tk.Scale(self, from_=-3, to=3,variable=magnetic, resolution=1, orient=tk.HORIZONTAL, label="Magnetic Field", length=120, tickinterval=3,fg="green")
		self.magnetic_slider.place(relx = 0.75, rely = 0.2)
		self.magnetic_slider.set(0)
		
		fig = plt.figure()
		plt.title("Ising Model Animation")
		canvas = FigureCanvasTkAgg(fig,self)
		canvas.get_tk_widget().place(relx=0.1, rely=0.35, relwidth=0.8)
		self.ising_grid = self.random_grid()
		self.im = plt.imshow(self.ising_grid, animated=True)
		self.ani = animation.FuncAnimation(fig, self.updatefig,  blit=True)

class CritTempPage(tk.Frame):

	def exponential_dict(self, magnetic, temp, coupling):
		exp_dict = {}
		spins = [-1,1]
		neighbor_sums = [-4,-2,0,2,4]
		for spin in spins:
			for neighbor_sum in neighbor_sums:
				exp = np.exp(-2*spin*(coupling*neighbor_sum + magnetic)/temp)
				exp_dict[(spin, neighbor_sum)] = exp
		return exp_dict

	def random_grid_sized(self,rows,columns):
		return np.random.choice([-1,1], size=(rows, columns))

	def spin_flip_all(self, grid, magnetic, coupling, temp, exp_dict):
		for i in range(ROWS1):
			for j in range(COLUMNS1):
				neighbor_sum = grid[(i+1)%ROWS1,j]+grid[i-1,j]+grid[i,(j+1)%COLUMNS1]+grid[i,j-1]
				spin = grid[i,j]
				pr = exp_dict[(spin, neighbor_sum)]
				change = np.random.rand(1)
				if np.minimum(1,pr) > change[0]:
					grid[i,j] = -1*grid[i,j]
		return grid
	
	def critical_temperature(self):
		temp = 1.0
		magnetic = 0
		coupling = 1
		temps = []
		avgM = []
		grid = self.random_grid_sized(ROWS1,COLUMNS1)
		exp_dict = self.exponential_dict(magnetic, temp, coupling)
		for k in range(1000):
			self.spin_flip_all(grid, magnetic, coupling, temp, exp_dict)
		for i in range(20):
			temps.append(temp)
			exp_dict = self.exponential_dict(magnetic, temp, coupling)		
			for j in range(20):
				self.spin_flip_all(grid, magnetic, coupling, temp, exp_dict)
			temp += 0.1
			avgM.append(np.sum(grid)/(ROWS1*COLUMNS1))
		return temps, avgM
		
	def crit_temp_graph(self):
		fig = plt.figure()
		temps, avgM = self.critical_temperature()
		g = fig.add_subplot(111)
		g.plot(temps, avgM)
		plt.title('Temperature vs Average Magnetization')
		plt.ylabel('Average Magnetization')
		plt.xlabel('Temperature')
		canvas = FigureCanvasTkAgg(fig,self)
		canvas.get_tk_widget().place(relx=0.1, rely=0.35, relwidth=0.8)
		canvas.draw()

	def __init__(self, parent, controller):
			tk.Frame.__init__(self, parent,height=800, width=1000)
			label = ttk.Label(self, text="Critical Temperature Graph")
			label.place(relx = 0.5, rely=0)
			button1 = ttk.Button(self, text="Quit",command=lambda: quit())
			button1.place(relx = 0.2, rely=0.05)
			button2 = ttk.Button(self, text="Hysteresis Page",command=lambda: controller.show_frame(HysteresisPage))
			button2.place(relx = 0.4, rely=0.05)
			button3 = ttk.Button(self, text="Ising Animation Page",command=lambda: controller.show_frame(IsingAnimationPage))
			button3.place(relx = 0.6, rely=0.05)
			button4 = ttk.Button(self, text="Create Critical Temperature Graph", command=self.crit_temp_graph)
			button4.place(relx = 0.4, rely = 0.3)
					
class HysteresisPage(tk.Frame):

	def exponential_dict(self, magnetic, temp, coupling):
		exp_dict = {}
		spins = [-1,1]
		neighbor_sums = [-4,-2,0,2,4]
		for spin in spins:
			for neighbor_sum in neighbor_sums:
				exp = np.exp(-2*spin*(coupling*neighbor_sum + magnetic)/temp)
				exp_dict[(spin, neighbor_sum)] = exp
		return exp_dict

	def random_grid_sized(self,rows,columns):
		return np.random.choice([-1,1], size=(rows, columns))

	def spin_flip_all(self, grid, magnetic, coupling, temp, exp_dict):
		for i in range(ROWS1):
			for j in range(COLUMNS1):
				neighbor_sum = grid[(i+1)%ROWS1,j]+grid[i-1,j]+grid[i,(j+1)%COLUMNS1]+grid[i,j-1]
				spin = grid[i,j]
				pr = exp_dict[(spin, neighbor_sum)]
				change = np.random.rand(1)
				if np.minimum(1,pr) > change[0]:
					grid[i,j] = -1*grid[i,j]
		return grid

	def hysteresis(self, magnetic, temp, coupling):
		avgM = []
		mag_field = []
		grid = self.random_grid_sized(ROWS1,COLUMNS1)
		exp_dict = self.exponential_dict(magnetic, temp, coupling)
		avgM.append(np.sum(grid)/(ROWS1*COLUMNS1))
		mag_field.append(magnetic)

		for B in range(10):
			exp_dict = self.exponential_dict(magnetic, temp, coupling)
			for n in range(20):
				self.spin_flip_all(grid, magnetic, coupling, temp, exp_dict)
			avg_mag = np.sum(grid)/(ROWS1*COLUMNS1)
			avgM.append(avg_mag)
			mag_field.append(magnetic)
			magnetic += 0.3
		for B in range(20):
			exp_dict = self.exponential_dict(magnetic, temp, coupling)
			for n in range(20):
				self.spin_flip_all(grid, magnetic, coupling, temp, exp_dict)
			avg_mag = np.sum(grid)/(ROWS1*COLUMNS1)
			avgM.append(avg_mag)
			mag_field.append(magnetic)
			magnetic -= 0.3
		for B in range(20):
			exp_dict = self.exponential_dict(magnetic, temp, coupling)
			for n in range(20):
				self.spin_flip_all(grid, magnetic, coupling, temp, exp_dict)
			avg_mag = np.sum(grid)/(ROWS1*COLUMNS1)
			avgM.append(avg_mag)
			mag_field.append(magnetic)
			magnetic += 0.3
		return mag_field, avgM

	def create_graph(self):
		fig = plt.figure()
		mag_field, avgM = self.hysteresis(0, self.temperature_slider.get(), self.coupling_slider.get())
		g = fig.add_subplot(111)
		g.plot(mag_field, avgM)
		plt.title("Magnetic Hysteresis Curve for J= "+str(self.coupling_slider.get())+ " T= "+str(self.temperature_slider.get()))
		plt.ylabel('Average Magnetization')
		plt.xlabel('External Magnetic Field')
		canvas = FigureCanvasTkAgg(fig,self)
		canvas.get_tk_widget().place(relx=0.1, rely=0.35, relwidth=0.8)
		canvas.draw()

	def __init__(self, parent, controller):
			temp = 1.5
			coupling = 1
			tk.Frame.__init__(self, parent,height=800, width=1000)
			label = ttk.Label(self, text="Hysteresis Graph")
			label.place(relx = 0.5, rely=0)
			button1 = ttk.Button(self, text="Quit",
								command=lambda: quit())
			button1.place(relx = 0.2, rely=0.05)
			button2 = ttk.Button(self, text="Critical Temperature Page",
                            command=lambda: controller.show_frame(CritTempPage))
			button2.place(relx = 0.4, rely=0.05)
			button3 = ttk.Button(self, text="Ising Animation Page",
								command=lambda: controller.show_frame(IsingAnimationPage))
			button3.place(relx = 0.6, rely=0.05)
			button4 = ttk.Button(self, text="Create Magnetic Hysteresis Graph", command=self.create_graph)
			button4.place(relx = 0.4, rely = 0.3)
			self.temperature_slider = tk.Scale(self, from_=0.1, to=3.5,variable=temp, resolution=0.1, orient=tk.HORIZONTAL, label="Temperature", length=120, tickinterval=3.5, fg="blue")
			self.temperature_slider.place(relx = 0.35, rely = 0.15)
			self.temperature_slider.set(1.5)

			self.coupling_slider = tk.Scale(self, from_=-1.0, to=1.0,variable=coupling, resolution=0.1, orient=tk.HORIZONTAL, label="Coupling Constant", length=120, tickinterval=1.0, fg="purple")
			self.coupling_slider.place(relx = 0.55, rely = 0.15)
			self.coupling_slider.set(1.0)
		
ising = Ising()
ising.mainloop()