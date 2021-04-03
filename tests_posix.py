#!/usr/bin/env python3
from tests_base import Timing,randstr

from random import randrange
import crypt

def timings_mod(TIMINGS:Timing):
	#dynamically filling tests 5-char encryption and 20-char encryption
	for nr in (5,20):
		encrs=[
			(meth.name+" (crypt)",f"encrypt(randstr({nr}),meth)","",{"randstr":randstr,"meth":meth,"encrypt":crypt.crypt})
			for meth in crypt.methods
			]
		key=f"{nr}-char encryption"
		if key in TIMINGS:
			TIMINGS[key]+=encrs
		else:
			TIMINGS[key]=encrs