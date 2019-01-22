#!/usr/bin/env python3

from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
import csv
from PIL import Image, ImageTk 

segROIs = ["Left-Lateral-Ventricle", "Right-Lateral-Ventricle", "Left-Inf-Lat-Vent", "Right-Inf-Lat-Vent", "Left-Cerebellum-White-Matter", "Right-Cerebellum-White-Matter", "Left-Cerebellum-Cortex", "Right-Cerebellum-Cortex", "Left-Thalamus-Proper", "Right-Thalamus-Proper", "Left-Caudate", "Right-Caudate", "Left-Putamen", "Right-Putamen", "Left-Pallidum", "Right-Pallidum", "3rd-Ventricle", "4th-Ventricle", "Brain-Stem", "Left-Hippocampus", "Right-Hippocampus", "Left-Amygdala", "Right-Amygdala", "CSF", "Left-Accumbens-area", "Right-Accumbens-area", "Left-VentralDC", "Right-VentralDC", "Left-vessel", "Right-vessel", "Left-choroid-plexus", "Right-choroid-plexus", "5th-Ventricle", "WM-hypointensities", "Left-WM-hypointensities", "Right-WM-hypointensities", "non-WM-hypointensities", "Left-non-WM-hypointensities", "Right-non-WM-hypointensities", "Optic-Chiasm", "CC_Posterior", "CC_Mid_Posterior", "CC_Central", "CC_Mid_Anterior", "CC_Anterior"]

parcROIs = ["Left-bankssts", "Right-bankssts", "Left-caudalanteriorcingulate", "Right-caudalanteriorcingulate", "Left-caudalmiddlefrontal", "Right-caudalmiddlefrontal", "Left-cuneus", "Right-cuneus", "Left-entorhinal", "Right-entorhinal", "Left-fusiform", "Right-fusiform", "Left-inferiorparietal", "Right-inferiorparietal", "Left-inferiortemporal", "Right-inferiortemporal", "Left-isthmuscingulate", "Right-isthmuscingulate", "Left-lateraloccipital", "Right-lateraloccipital", "Left-lateralorbitofrontal", "Right-lateralorbitofrontal", "Left-lingual", "Right-lingual", "Left-medialorbitofrontal", "Right-medialorbitofrontal", "Left-middletemporal", "Right-middletemporal", "Left-parahippocampal", "Right-parahippocampal", "Left-paracentral", "Right-paracentral", "Left-parsopercularis", "Right-parsopercularis", "Left-parsorbitalis", "Right-parsorbitalis", "Left-parstriangularis", "Right-parstriangularis", "Left-pericalcarine", "Right-pericalcarine", "Left-postcentral", "Right-postcentral", "Left-posteriorcingulate", "Right-posteriorcingulate", "Left-precentral", "Right-precentral", "Left-precuneus", "Right-precuneus", "Left-rostralanteriorcingulate", "Right-rostralanteriorcingulate", "Left-rostralmiddlefrontal", "Right-rostralmiddlefrontal", "Left-superiorfrontal", "Right-superiorfrontal", "Left-superiorparietal", "Right-superiorparietal", "Left-superiortemporal", "Right-superiortemporal", "Left-supramarginal", "Right-supramarginal", "Left-frontalpole", "Right-frontalpole", "Left-temporalpole", "Right-temporalpole", "Left-transversetemporal", "Right-transversetemporal", "Left-insula", "Right-insula"]

# Returned Lists
dirList = [0, 0]
segList = []
parcList = []

class FreeLearn(tk.Tk):
	def __init__(self,*args,**kwargs):
		tk.Tk.__init__(self, *args,**kwargs)
		self.title('FreeLearn')
		self.resizable(width=0, height=0)
		self.geometry('{}x{}'.format(700, 700))
		self.notebook = ttk.Notebook(width = 700, height = 650)
		self.add_tab()
		self.notebook.grid(row=0)
		self.RUN = ttk.Button(self, text="Run")
		self.RUN.grid(row=1, sticky='WE')
  
	def add_tab(self):
		tab1 = setupTab(self.notebook)
		self.notebook.add(tab1,text="Setup")

		tab2 = roiTab(self.notebook)
		self.notebook.add(tab2,text="ROI Selection")

		tab3 = classifierTab(self.notebook)
		self.notebook.add(tab3, text = "Classifier Options")

		tab4 = gridTab(self.notebook)
		self.notebook.add(tab4, text = "Grid Search", state = 'disabled')

	def checkGridStatus(self):
		if gridSet == 1:
			self.notebook.tab(3, state = 'normal')
		elif gridSet == 0:
			self.notebook.tab(3, state='disabled')

class setupTab(tk.Frame):
	def __init__(self, parent, *args, **kwargs):
		self.parent = parent
		tk.Frame.__init__(self,*args,**kwargs)
		
		# Logo
		self.image = Image.open('Logo.jpg')
		self.photo = ImageTk.PhotoImage(self.image)
		
		self.logo = tk.Label(self, image=self.photo)	
		self.logo.grid(row = 1, column = 0, padx=30, pady=30)

		self.title = tk.Label(self, font = "Helvetica 38 bold", text='FreeLearn')
		self.title.grid(row = 1, column = 1)
		
		# Configures recon dir row		
		self.label = tk.Label(self, text='Recon Parent Directory:')
		self.label.grid(row=2, column=0, sticky = 'W', padx=10, pady=10)
		self.reconEntry = tk.Entry(self, width = 45)
		self.reconEntry.grid(row = 2, column = 1, sticky = 'W', padx=10, pady=10)
		reconPath = self.reconEntry.get()
		self.reconSelect = tk.Button(self, text="Select", command= lambda: self.selectDir(rowIdx = 2, columnIdx = 1, idx=0))
		self.reconSelect.grid(row=2, column=2, sticky = 'W', padx=10, pady=10)

		# Configures output dir row
		self.outputLabel = tk.Label(self, text = 'Output Directory:')
		self.outputLabel.grid(row = 3, column = 0, sticky = 'W', padx=10, pady=10)
		self.outputEntry = tk.Entry(self, width = 45)
		self.outputEntry.grid(row = 3, column = 1, sticky = 'W', padx=10, pady=10)
		outputPath = self.outputEntry.get()
		self.outputSelect = tk.Button(self, text="Select", command= lambda: self.selectDir(rowIdx = 3, columnIdx = 1, idx=1))
		self.outputSelect.grid(row=3, column=2, sticky = 'W', padx=10, pady=10)

		# Configures csv row
		self.csvLabel = tk.Label(self, text = 'CSV File:')
		self.csvLabel.grid(row = 4, column = 0, sticky = "W", padx=10, pady=10)
		self.csvEntry = tk.Entry(self, width = 45)
		self.csvEntry.grid(row = 4, column = 1, sticky = "W", padx=10, pady=10)
		csvFile = self.csvEntry.get()
		self.csvSelect = tk.Button(self, text="Select", command= lambda: self.selectCSV(rowIdx = 4, columnIdx = 1))
		self.csvSelect.grid(row=4, column=2, sticky = "W", padx=10, pady=10)

	def selectDir(self, rowIdx, columnIdx, idx):
		self.dir_ask = filedialog.askdirectory()
		self.dir_path = tk.StringVar()
		self.dir_path.set(self.dir_ask)
		self.dirEntry = tk.Entry(self, width = 45, textvariable = self.dir_path)
		self.dirEntry.grid(row = rowIdx, column = columnIdx)
		dirPath = self.dirEntry.get()
		dirList[idx] = dirPath
		
	
	def selectCSV(self, rowIdx, columnIdx):
		#global csv_path
		#global fileEntryVar
		global idOut
		global lblOut	
		idOut = []
		lblOut = []	
		self.filename = filedialog.askopenfilename(filetypes = [("CSV File With Header", "*.csv")])
		self.csv_path = tk.StringVar()
		self.csv_path.set(self.filename)
		self.fileEntry = tk.Entry(self, width = 45, textvariable = self.csv_path)
		self.fileEntry.grid(row = rowIdx, column = columnIdx)
		self.fileEntryVar = self.fileEntry.get()

		# Reads in csv
		global csvArray
		csvArray = []
		with open(self.fileEntryVar) as f:
			self.reader = csv.reader(f, delimiter=',')
			for i in self.reader:
				csvArray.append(i)
		self.csvHeader = csvArray[0]

		# Select and return ID variable	
		self.idLabel = tk.Label(self, text = 'Subject ID Variable:')
		self.idLabel.grid(row = 5, column = 0, sticky = "W", padx=10, pady=10)
		self.idInit = tk.StringVar(self)
		self.idInit.set(self.csvHeader[0])
		self.idMenu = tk.OptionMenu(self, self.idInit, *self.csvHeader, command = lambda : self.getVar(self.idInit, idOut))
		self.idMenu.config(width=10)
		self.idMenu.grid(row = 5, column = 1, sticky = 'W', padx = 10, pady = 10)
		# Select and return classifier labels
		self.lblInit = tk.StringVar(self)
		self.lblInit.set(self.csvHeader[0])
		self.lblLabel = tk.Label(self, text = 'Classification Labels:')
		self.lblLabel.grid(row = 6, column = 0, sticky = "W", padx = 10, pady = 10)
		self.lblMenu = tk.OptionMenu(self, self.lblInit, *self.csvHeader, command = lambda : self.getVar(self.lblInit, lblOut))	
		self.lblMenu.config(width = 10)
		self.lblMenu.grid(row = 6, column = 1, sticky = 'W', padx = 10, pady = 10)

	def getVar(self, inVar, outVar):
		outVar.clear()
		outVar.append(inVar.get())
		return outVar
	
class roiTab(tk.Frame):
	def __init__(self, parent, *args, **kwargs):

		self.parent = parent
		tk.Frame.__init__(self,*args,**kwargs)
		
		# Configures segmentation row
		self.segLabel = tk.Label(self, text = "Segmentation ROIs:")
		self.segLabel.grid(row = 1, column = 0, sticky = 'W', padx=10, pady=10)

		self.segSelect = tk.Listbox(self, width = 25)
		self.segSelect.grid(row = 2, column = 0, padx = 10, pady = 10) 

		self.segArrows = tk.Label(self, text = ">>")
		self.segArrows.grid(row = 2, column = 1, padx = 10, pady = 10)
	
		self.segSelect2 = tk.Listbox(self, width=25)
		self.segSelect2.grid(row = 2, column = 2, padx = 10, pady = 10)

		# Configures parcellation row
		self.parcLabel = tk.Label(self, text = "Parcellation ROIs:")
		self.parcLabel.grid(row = 3, column = 0, sticky = 'W', padx=10, pady=10)

		self.parcSelect = tk.Listbox(self, width=25)
		self.parcSelect.grid(row = 4, column = 0, padx = 10, pady = 10)

		self.parcArrows = tk.Label(self, text = ">>")
		self.parcArrows.grid(row = 4, column = 1, padx = 10, pady = 10)
		
		self.parcSelect2 = tk.Listbox(self, width=25)
		self.parcSelect2.grid(row = 4, column = 2, padx = 10, pady = 10)
		
		# Inserts ROI names
		for idx,roi in enumerate(parcROIs):
		  self.parcSelect.insert(idx+1, roi)

		for idx,roi in enumerate(segROIs):
		  self.segSelect.insert(idx+1, roi)

		# Bind click to list movement
		self.segSelect.bind('<<ListboxSelect>>', lambda event: moveItem(self.segSelect, self.segSelect2, segROIs, segList, mode='right'))
		self.segSelect2.bind('<<ListboxSelect>>', lambda event: moveItem(self.segSelect2, self.segSelect, segROIs, segList, mode='left'))
		self.parcSelect.bind('<<ListboxSelect>>', lambda event: moveItem(self.parcSelect, self.parcSelect2, parcROIs, parcList, mode='right'))
		self.parcSelect2.bind('<<ListboxSelect>>', lambda event: moveItem(self.parcSelect2, self.parcSelect, parcROIs, parcList, mode='left'))
	
		# Configure Normalization Row
		self.normLabel = tk.Label(self, text = "ROI Normalization:")
		self.normLabel.grid(row = 5, column = 0, sticky = 'W', padx = 10, pady = 10)
		self.normOptions = ["Residual Normalization (all)",  "Residual Normalization (sub-group)", "ICV Division", "None"]
		self.normVar = tk.StringVar(self)
		self.normVar.set(self.normOptions[0])
		self.normW = tk.OptionMenu(self, self.normVar, *self.normOptions, command = self.getNorm)	
		self.normW.config(width=25, padx = 10, pady = 10)
		self.normW.grid(row = 6, column = 0)

	# Determines normalization option
	def getNorm(self, *args):
		global norm
		global varSelect
		norm = self.normVar.get()
		
		# Allows normalization by group or other variable
		if norm == 'Residual Normalization (sub-group)':
			self.varText = tk.Label(self, text = "Variable:", padx = 10, pady =10)
			self.varText.grid(row = 6, column = 1)
			self.varSelect = tk.StringVar(self)
			self.varSelect.set(csvArray[0][0])
			self.varMenu = tk.OptionMenu(self, self.varSelect, *csvArray[0], command = self.updateVar)
			self.varMenu.config(width=25, padx = 10, pady = 10)
			self.varMenu.grid(row = 6, column = 2)
					
			levelStart = []
			for subj in csvArray:
				for var in subj:
					levelStart.append(var)

			levelStart = list(set(levelStart))

			
			self.levelFirst = tk.StringVar(self)
			self.levelFirst.set(levelStart[0])
			self.levelText = tk.Label(self, text = "Level:")
			self.levelText.grid(row = 7, column = 1, padx = 10, pady = 10)
			self.levelMenu = tk.OptionMenu(self, self.levelFirst, *levelStart)
			self.levelMenu.config(width=25, padx = 10, pady = 10)
			self.levelMenu.grid(row = 7, column = 2)	
		else:
			try:
				self.varText.grid_forget()
				self.varMenu.grid_forget()
				self.levelText.grid_forget()
				self.levelMenu.grid_forget()
			except AttributeError:
				pass		
		return(norm)

	# Variable levels (only called if normalizing by sub-group)
	def updateVar(self, *args):
		global varLevels
		varLevels = []		
		selection = self.varSelect.get()	
		self.varSelect.set(selection)
		splitVar = self.varSelect.get()
		splitIdx = csvArray[0].index(splitVar)
		for idx,subj in enumerate(csvArray):
			if idx > 0:
				varLevels.append(subj[splitIdx])
		varLevels = list(set(varLevels))		
		
		if self.levelMenu is not None:
			self.levelMenu.grid_forget()

		self.levelText = tk.Label(self, text = "Level:", padx = 10, pady = 10)
		self.levelText.grid(row = 7, column = 1)
		self.levelSelect = tk.StringVar(self)
		self.levelSelect.set(varLevels[0])
		self.levelMenu = tk.OptionMenu(self, self.levelSelect, *varLevels)
		self.levelMenu.config(width=25, padx = 10, pady = 10)
		self.levelMenu.grid(row = 7, column = 2)

class classifierTab(tk.Frame):
	def __init__(self, parent, *args, **kwargs):
		self.parent = parent
		tk.Frame.__init__(self,*args,**kwargs)
		# Configures recon dir row		
		self.label = tk.Label(self, text='Classifier Type:')
		self.label.grid(row=1, column=0, sticky = 'W', padx=10, pady=10)
			
		# Classifier Type
		classTypes = ['SVM', 'Random Forest']
		self.classSelect = tk.StringVar(self)
		self.classSelect.set(classTypes[0])
		global classOut
		classOut = []
		self.classMenu = tk.OptionMenu(self, self.classSelect, *classTypes, command = lambda _: (classOut.clear(), classOut.append(self.classSelect.get())))
		self.classMenu.config(width=15)
		self.classMenu.grid(row = 1, column = 1, sticky = 'W', padx = 10, pady = 10)
	
		# Train row
		self.trainSize = tk.Label(self, text = 'Training Proportion:')
		self.trainSize.grid(row = 2, column = 0, sticky = 'W', padx=10, pady=10)
		self.trainInit = tk.StringVar(self)
		self.trainInit.set(0.5)
		self.trainEntry = tk.Entry(self, width = 5, textvariable = self.trainInit, justify = 'center')
		trainOut = self.trainEntry.get()
		self.trainEntry.grid(row = 2, column = 1, sticky = 'W', padx=10, pady=10)
		
		# Test row
		self.testSize = tk.Label(self, text = 'Testing Proportion:')
		self.testSize.grid(row = 3, column = 0, sticky = 'W', padx=10, pady=10)
		self.testInit = tk.StringVar(self)
		self.testInit.set(0.500)
		self.testEntry = tk.Entry(self, width = 5, textvariable = self.testInit, justify = 'center')
		self.testEntry.grid(row = 3, column = 1, sticky = 'W', padx=10, pady=10)
		
		# Update train and test entries
		self.trainInit.trace("w", lambda *_, var=self.trainInit: self.updateEntry(a='1'))
		self.testInit.trace("w", lambda *_, var=self.testInit: self.updateEntry(a='2'))

		# Mean and variance centering
		self.centerText = tk.Label(self, text = 'Mean and Variance Centering:')
		self.centerText.grid(row = 4, column = 0, sticky = 'W', padx = 10, pady = 10)
		
		self.centerYN = tk.IntVar(value = 1)
		self.centerCB = tk.Checkbutton(self, variable = self.centerYN, command = self.centerReturn)
		self.centerCB.grid(row = 4, column = 1, sticky = 'W', padx = 10, pady = 10)

		# Grid Search Yes/No
		self.gridText = tk.Label(self, text = 'Grid Search:')
		self.gridText.grid(row = 5, column = 0, sticky = 'W', padx = 10, pady = 10)

		self.gridYN = tk.IntVar(self)
		self.gridCB = tk.Checkbutton(self, variable = self.gridYN, command = self.gridReturn)
		self.gridCB.grid(row = 5, column = 1, sticky = 'W', padx = 10, pady = 10)

		# Kernel
		self.kernelLabel = tk.Label(self, text = "Kernel:")
		self.kernelLabel.grid(row = 6, column = 0, sticky = 'W', padx = 10, pady = 10)
		self.kernelOptions = ["Linear", "Radial Bias Function", "Poly", "Sigmoid"]
		self.kernelInit = tk.StringVar(self)
		self.kernelInit.set(self.kernelOptions[0])
		self.kernelMenu = tk.OptionMenu(self, self.kernelInit, *self.kernelOptions)	
		self.kernelMenu.config(width=15)
		self.kernelMenu.grid(row = 6, column = 1, sticky = 'W', padx = 10, pady = 10)

		# Cost
		self.costLabel = tk.Label(self, text = "Cost:")
		self.costLabel.grid(row = 7, column = 0, sticky = 'W', padx = 10, pady = 10)
		self.costInit = tk.StringVar(self)
		self.costInit.set(1)
		self.costEntry = tk.Entry(self, width = 10, textvariable = self.costInit, justify = 'center')
		self.costEntry.grid(row = 7, column = 1, sticky = 'W', padx = 10, pady = 10)

		# Gamma
		self.gammaLabel = tk.Label(self, text = "Gamma:")
		self.gammaLabel.grid(row = 8, column = 0, sticky = 'W', padx = 10, pady = 10)
		self.gammaInit = tk.StringVar(self)
		self.gammaInit.set(0.01)
		self.gammaEntry = tk.Entry(self, width = 10, textvariable = self.gammaInit, justify = 'center')
		self.gammaEntry.grid(row = 8, column = 1, sticky = 'W', padx = 10, pady = 10)

	# Needs updating to force train + test = 1
	def updateEntry(self, a, *args):
		global train
		global test
		try:
			train = round(float(self.trainEntry.get()),3)
			test = round(float(self.testEntry.get()),3)
		except ValueError:
			train = 0.500
			test = 0.500
			print('value error')
		self.trainInit.set(train)
		self.testInit.set(test)
		return train
		return test

	def centerReturn(self):
		global centerSet
		centerSet = self.centerYN.get()
		return centerSet
		
	def gridReturn(self):
		global gridSet
		gridSet = self.gridYN.get()
		run.checkGridStatus()
		if gridSet == 1:
			self.kernelMenu.config(state = "disabled")
			self.costEntry.config(state = "disabled")
			self.gammaEntry.config(state = "disabled")
		elif gridSet == 0:
			self.kernelMenu.config(state = "normal")
			self.costEntry.config(state = "normal")
			self.gammaEntry.config(state = "normal")
		return gridSet

	def classReturn(self, *args):
		global classOut
		classOut = self.classSelect.get()
		return classOut
		

class gridTab(tk.Frame):
	global kernelList
	kernelList = []
	def __init__(self, parent, *args, **kwargs):
		self.parent = parent
		tk.Frame.__init__(self,*args,**kwargs)
		# Configures kernel
		self.kernels = ["Linear", "Radial Bias Function", "Poly", "Sigmoid"]
	
		self.kernelLabel = tk.Label(self, text = "Kernels:")
		self.kernelLabel.grid(row = 1, column = 0, sticky = 'W', pady = 10)
		self.kernelFrame = tk.Frame(self)
		self.kernelFrame.grid(row = 1, column = 1, padx = 10, pady = 10, sticky = 'W')
		self.kernelSelect = tk.Listbox(self.kernelFrame, width = 25)
		self.kernelSelect.pack(side = 'left')
		self.kernelSelect.config(width = 20, height = 4) 
		self.kernelArrows = tk.Label(self.kernelFrame, text = ">>")
		self.kernelArrows.pack(side = 'left', padx = 10)
		self.kernelSelect2 = tk.Listbox(self.kernelFrame, width=25)
		self.kernelSelect2.pack(side = 'left')
		self.kernelSelect2.config(width = 20, height = 4)
		
		# Listbox item movement
		for idx,kern in enumerate(self.kernels):
			self.kernelSelect.insert(idx+1, kern)

		self.kernelSelect.bind('<<ListboxSelect>>', lambda event: moveItem(self.kernelList, self.kernelSelect2, self.kernels, kernelList, mode = 'right'))
		self.kernelSelect2.bind('<<ListboxSelect>>', lambda event: moveItem(self.kernelSelect2, self.kernelSelect, self.kernels, kernelList, mode = 'left')) 
		
		# Configures cost
		self.costLabel = tk.Label(self, text = "Cost:")
		self.costLabel.grid(row = 2, column = 0, sticky = 'W', pady = 1)

		self.costFrame = tk.Frame(self)
		self.costFrame.grid(row = 2, column = 1, sticky = 'W', padx = 10)
		
		self.minLabel = tk.Label(self.costFrame, text='Min = ')
		self.minLabel.pack(side='left')
		self.minDefault = tk.StringVar()
		self.minDefault.set(0)
		self.minEntry = tk.Entry(self.costFrame, textvariable = self.minDefault, width = 6, justify = 'center')
		self.minEntry.pack(side='left')
		
		self.maxFrame = tk.Frame(self)
		self.maxFrame.grid(row = 3, column = 2, sticky = 'W', padx = 10)
		self.maxLabel = tk.Label(self.costFrame, text='Max = ')
		self.maxLabel.pack(side='left')
		self.maxDefault = tk.StringVar()
		self.maxDefault.set(100)
		self.maxEntry = tk.Entry(self.costFrame, textvariable = self.maxDefault, width = 6, justify = 'center')
		self.maxEntry.pack(side='left')
		
		self.stepFrame = tk.Frame(self)
		self.stepFrame.grid(row = 3, column = 3, sticky = 'W', padx = 10)
		self.stepLabel = tk.Label(self.costFrame, text='Step = ')
		self.stepLabel.pack(side='left')
		self.stepDefault = tk.StringVar()
		self.stepDefault.set(10)
		self.stepEntry = tk.Entry(self.costFrame, textvariable = self.stepDefault, width = 6, justify = 'center')
		self.stepEntry.pack(side='left')
	
		# Configures gamma
		self.gammaLabel = tk.Label(self, text = "Gamma:")
		self.gammaLabel.grid(row = 3, column = 0, sticky = 'W', pady = 10)

		self.gammaFrame = tk.Frame(self)
		self.gammaFrame.grid(row = 3, column = 1, sticky = 'W', padx = 10)
		
		self.gammaMinLabel = tk.Label(self.gammaFrame, text='Min = ')
		self.gammaMinLabel.pack(side='left')
		self.gammaMinDefault = tk.StringVar()
		self.gammaMinDefault.set(0)
		self.gammaMinEntry = tk.Entry(self.gammaFrame, textvariable = self.minDefault, width = 6, justify = 'center')
		self.gammaMinEntry.pack(side='left')
		
		self.gammaMaxFrame = tk.Frame(self)
		self.gammaMaxFrame.grid(row = 4, column = 2, sticky = 'W', padx = 10)
		self.gammaMaxLabel = tk.Label(self.gammaFrame, text='Max = ')
		self.gammaMaxLabel.pack(side='left')
		self.gammaMaxDefault = tk.StringVar()
		self.gammaMaxDefault.set(100)
		self.gammaMaxEntry = tk.Entry(self.gammaFrame, textvariable = self.maxDefault, width = 6, justify = 'center')
		self.gammaMaxEntry.pack(side='left')
		
		self.gammaStepFrame = tk.Frame(self)
		self.gammaStepFrame.grid(row = 4, column = 3, sticky = 'W', padx = 10)
		self.gammaStepLabel = tk.Label(self.gammaFrame, text='Step = ')
		self.gammaStepLabel.pack(side='left')
		self.gammaStepDefault = tk.StringVar()
		self.gammaStepDefault.set(10)
		self.gammaStepEntry = tk.Entry(self.gammaFrame, textvariable = self.stepDefault, width = 6, justify = 'center')
		self.gammaStepEntry.pack(side='left')

		# Configure CPUs 
		self.jobsLabel = tk.Label(self, text = 'CPUs: ')
		self.jobsLabel.grid(row = 5, column = 0, sticky = 'W', pady = 10)
		self.jobsDefault = tk.StringVar()
		self.jobsDefault.set(1)
		self.jobsEntry = tk.Entry(self, textvariable = self.jobsDefault, width = 6, justify = 'center')
		self.jobsEntry.grid(row = 5, column = 1, sticky='W', padx = 10, pady = 10)

# Move items from one list to another, updating an output list
# Used in ROI and Grid Search tab
def moveItem(list1, list2, origList, selectList, mode):
	idx = int(list1.curselection()[0])
	value = list1.get(idx)
	origIdx = origList.index(value)
	list2.insert(origIdx,value)
	list1.delete(idx)

	selectList.clear()
	if mode == 'right':
		for idx in range(0,list2.size()):
			item = list2.get(idx)
			selectList.append(item)
	elif mode == 'left':
		for idx in range(0,list1.size()):
			item = list1.get(idx)
			selectList.append(item)
	return selectList	
	
'''
def getVar(inVar, outVar):
	outVar.clear()
	outVar.append(inVar.get())
	return outVar
'''

run = FreeLearn()
run.mainloop()

'''
Tab1
# Returns CSV
print(csvArray)
# Returns ID Variable
print(varSelect)
# Returns recon and output paths
print(dirList)
Tab2
# Returns ROIs
print(segList)
print(parcList)
# Returns normalization type
print(norm)
# Returns sub-group level
print(varLevels)
'''
#print(classOut)
print(dirList)

