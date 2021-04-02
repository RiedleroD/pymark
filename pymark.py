#!/usr/bin/env python3
#TODO: ah, this code is a mess. Cleanup crew, please!
import os,sys,random
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk,Gdk

from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import FormatStrFormatter as MPLFormatter

from typing import Union,Any,Optional,Tuple,List,Dict,Iterable
from tests_base import Timing

import timeit
from statistics import mean

from tests_base import TIMINGS

version=sys.version_info.minor
if version>=10:
	print("enabled python>=3.10 tests:")
	from tests_3_10 import timings_mod as tmod
	tmod(TIMINGS)
else:
	print("disabled python>=3.10 tests:")
print(" - structural pattern matching")
del version#we don't want this as a global variable

#possible: 'posix', 'nt', 'os2', 'ce', 'java', and 'riscos'
if os.name=="posix":
	print("enabled posix-specific tests:")
	print(" - cryptography (unix)")
	from tests_posix import timings_mod as tmod
	tmod(TIMINGS)

class Timer:
	__slots__=["name","rounds","value","_stmt","_setup","_globals"]
	def __init__(self,name:str,stmt:str,setup:str="pass",globals:Optional[Dict[str,Any]]=None):
		self.name=name
		self._stmt=stmt
		self._setup=setup
		self._globals=globals
	def evaluate(self):
		_timer=timeit.Timer(stmt=self._stmt,setup=self._setup,globals=self._globals)
		self.rounds,self.value=_timer.autorange()

class Main:
	going=False
	iterc=5
	bars=None
	def __init__(self):
		self.win=Gtk.Window()
		self.win.connect("delete-event",Gtk.main_quit)
		self.win.set_default_size(720,480)
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
	def measure(self,todos:Iterable[Timing])->Tuple[List[str],List[float]]:
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
	def fill_btnbox(self,btnbox:Gtk.ButtonBox,timings:Dict[str,Timing]):
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
	def set_bars(self,cache:Dict[str,List[float]]):
		names=tuple(cache.keys())
		means=[]
		errs=([],[])
		for samples in cache.values():
			m=mean(samples)
			errs[0].append(m-min(samples))
			errs[1].append(max(samples)-m)
			means.append(m)
		if self.bars:
			self.ax.clear()
		self.ax.xaxis.set_major_formatter(MPLFormatter("%0.2fµs"))
		self.bars=self.ax.barh(names,means,xerr=errs,capsize=10)
		self.fig.tight_layout()
	def _on_start(self,widget:Gtk.Button,event:Gdk.EventButton)->bool:
		if self.going:
			return True
		self.going=True
		self.spin.set_range(self.iterc,self.iterc)
		self.progr1.set_opacity(1)
		self.progr2.set_opacity(1)
		self.set_progress(0,True)
		self.set_progress(0,False)
		self.canvas.draw()
		timings=TIMINGS[widget.get_label()]
		cache={timing[0]:[] for timing in timings}
		iterc=self.iterc
		for i in range(1,iterc+1):
			for name,val in zip(*self.measure(timings)):
				cache[name].append(val)
			self.set_bars(cache)
			self.canvas.draw()
			self.set_progress(i/iterc,True)
		self.progr1.set_opacity(0)
		self.progr2.set_opacity(0)
		self.going=False
		self.spin.set_range(1,2**16)
		return True
	def _on_spin(self,widget:Gtk.SpinButton)->bool:
		self.iterc=int(widget.get_value())
		return True

m=Main()

Gtk.main()