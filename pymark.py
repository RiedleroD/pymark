#!/usr/bin/env python3
#TODO: ah, this code is a mess. Cleanup crew, please!
import os,sys,random
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk

from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.figure import Figure

import timeit
from typing import Dict

from tests_base import TIMINGS
version=sys.version_info.minor
if(version>=10):
	print("enabled py>=3.10 tests:")
	from tests_3_10 import timings_mod as tmod
	tmod(TIMINGS)
else:
	print("disabled py>=3.10 tests:")
print(" - structural pattern matching")

del version#we don't want this as a global variable

class Timer:
	value:float
	rounds:int
	name:str
	def __init__(self,name:str,stmt:str,setup:str="pass",globals=None):
		self.name=name
		self._stmt=stmt
		self._setup=setup
		self._globals=globals
	def set_values(self,rounds:int,ms:float):
		"""MICROseconds, not milliseconds"""
		self.rounds=rounds
		self.value=ms
	def evaluate(self):
		_timer=timeit.Timer(stmt=self._stmt,setup=self._setup,globals=self._globals)
		self.set_values(*_timer.autorange())

class Main:
	going:bool=False
	iterc:int=5
	def __init__(self):
		self.win=Gtk.Window()
		self.win.connect("delete-event",Gtk.main_quit)
		self.fig=Figure(figsize=(10,10),dpi=100)
		self.ax=self.fig.add_subplot()
		self.canvas = FigureCanvas(self.fig)
		sw = Gtk.ScrolledWindow()
		sw.set_border_width(10)
		sw.add(self.canvas)
		upperside=Gtk.ButtonBox(orientation=Gtk.Orientation.VERTICAL)
		self.fill_btnbox(upperside,TIMINGS)
		lowerside=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.spin=Gtk.SpinButton()
		self.spin.set_range(1,2**16)#TODO: find out how to remove upper bound
		self.spin.set_increments(1,10)
		self.spin.set_value(self.iterc)
		self.spin.connect("value-changed",self._on_spin)
		lowerside.pack_end(self.spin,False,True,0)
		lowerside.pack_end(Gtk.Label.new("↓Iterations↓"),False,True,0)
		self.progr2=Gtk.ProgressBar()
		lowerside.pack_end(self.progr2,False,True,2)
		self.progr1=Gtk.ProgressBar()
		lowerside.pack_end(self.progr1,False,True,2)
		sidebar=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		sidebar.pack_start(upperside,False,True,10)
		sidebar.pack_start(lowerside,True,True,2)
		self.box=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		self.box.pack_start(sidebar,False,True,2)
		self.box.pack_start(sw,True,True,0)
		self.win.add(self.box)
		self.win.show_all()
		self.progr1.set_opacity(0)
		self.progr2.set_opacity(0)
	def measure(self,todos):
		self.set_progress(0)
		names=[]
		vals=[]
		todolen=len(todos)
		for i,todo in enumerate(reversed(todos)):
			self.set_progress(i/todolen)
			t=Timer(*todo)
			t.evaluate()
			names.append(t.name)
			vals.append(t.value)
		self.set_progress(1.0)
		return names,vals
	def fill_btnbox(self,btnbox,timings):
		for name in timings.keys():
			btn=Gtk.Button(label=name)
			btn.connect("button-press-event",self._on_start)
			btnbox.pack_start(btn,False,True,0)
	def set_progress(self,fraction:float,upper:bool=False):
		if upper:
			progr=self.progr1
		else:
			progr=self.progr2
		progr.set_fraction(fraction)
		if not upper:
			while Gtk.events_pending():
				Gtk.main_iteration_do(False)
	def _on_start(self,widget,event):
		if self.going:
			return True
		self.going=True
		self.spin.set_range(self.iterc,self.iterc)
		self.progr1.set_opacity(1)
		self.progr2.set_opacity(1)
		self.set_progress(0,True)
		self.set_progress(0,False)
		self.ax.clear()
		self.canvas.draw()
		timings=TIMINGS[widget.get_label()]
		names=[timing[0] for timing in timings]
		vals=[0]*len(timings)
		iterc=self.iterc
		for i in range(1,iterc+1):
			_names,_vals=self.measure(timings)
			for j in range(len(vals)):
				vals[j]+=_vals[j]
			self.ax.clear()
			self.ax.barh(_names,[val/i for val in vals])
			self.canvas.draw()
			self.set_progress(i/iterc,True)
		self.progr1.set_opacity(0)
		self.progr2.set_opacity(0)
		self.going=False
		self.spin.set_range(0,2**16)
		return True
	def _on_spin(self,widget):
		self.iterc=int(widget.get_value())
		return True

m=Main()

Gtk.main()