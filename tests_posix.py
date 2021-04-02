#!/usr/bin/env python3
from tests_base import Timing

from random import randrange
import crypt

def randstr(size):
    return ''.join(chr(randrange(1,2048)) for x in range(size))

def timings_mod(TIMINGS:Timing):
	#dynamically filling tests 5-char encryption and 20-char encryption
	for nr in (5,20):
		encrs=[
			(meth.name,f"x=encrypt(randstr({nr}),meth)","",{"randstr":randstr,"meth":meth,"encrypt":crypt.crypt})
			for meth in crypt.methods
			]
		key=f"{nr}-char encryption"
		if key in TIMINGS:
			TIMINGS[key]+=encrs
		else:
			TIMINGS[key]=encrs