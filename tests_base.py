#!/usr/bin/env python3
from random import randrange
import hashlib

from typing import Generator,Union,Dict,List,Tuple,Any

#I checked, this is the best possible way to do this annotation
Timing=Dict[str,List[Union[Tuple[str,str],Tuple[str,str,str],Tuple[str,str,str,Dict[str,Any]]]]]

def randiter(amount:int,min:int,max:int)->Generator[int,None,None]:
	return (randrange(min,max) for i in range(amount))

def randstr(size):
    return str(bytes(randrange(1,256) for x in range(size)))

def randbytes(size):
	return bytes(randrange(1,256) for x in range(size))

def t_func():
	return None

def t_sb_elif_is(num:int)->str:
	if num==1:
		return "Sehr Gut"
	elif num==2:
		return "Gut"
	elif num==3:
		return "Befriedigend"
	elif num==4:
		return "Genügend"
	elif num==5:
		return "Nicht Genügend"

def t_mb_elif_is(maybe:str)->Union[bool,None]:
	m=maybe.lower()
	if m=="j" or m=="ja" or m=="y" or m=="yes":
		return True
	elif m=="n" or m=="nein" or m=="no":
		return False
	else:
		return None

def t_mb_elif_in(maybe:str)->Union[bool,None]:
	m=maybe.lower()
	if m in ("j","ja","y","yes"):
		return True
	elif m in ("n","nein","no"):
		return False
	else:
		return None

def t_sb_keys(num:int)->str:
	return keys_noten[num]

keys_noten={1:"Sehr Gut",2:"Gut",3:"Befriedigend",4:"Genügend",5:"Nicht Genügend"}
keys_maybe=dict(ja=True,nein=True,j=True,n=False,yes=False,no=False,y=False)

poss_maybe=['ja','nein','j','n','yes','no','y','aa','bb']

TIMINGS={
"pass":[
	("pass","pass"),
	("x=0","x=0"),
	("x=None","x=None")
	],
"arithmetics":[#TODO: see issue #8
	("x+=1","x+=1","x=0"),
	("x=x+1","x=x+1","x=0"),
	("x-=1","x-=1","x=0"),
	("x=x-1","x=x-1","x=0"),
	("x*=2","x*=2","x=1"),
	("x=x*2","x=x*2","x=1"),
	("x+=x","x+=x","x=1"),
	("x=x+x","x=x+x","x=1"),
	("x/=2","x/=2","x=1"),
	("x=x/2","x=x/2","x=1")
	],
"boundary checking":[
	("a<b<c","x=2<b<6","b=randrange(0,10)",{"randrange":randrange}),
	("a<b and b<c","x=2<b and b<6","b=randrange(0,10)",{"randrange":randrange})
	],
"call overhead":[
	("lambda","func()","",{"func":lambda:None}),
	("method","func()","",{"func":t_func}),
	],
"empty arrays":[
	("()","x=()"),
	("tuple()","x=tuple()"),
	("[]","x=[]"),
	("list()","x=list()"),
	("{}","x={}"),
	("dict()","x=dict()"),
	("deque()","x=deque()","from collections import deque")
	],
"filled arrays":[
	("[0,1,2,…,19,20]","x=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]"),
	("list(range(20))","x=list(range(20))"),
	("[x for x in range(20)]","x=[y for y in range(20)]"),
	("(0,1,2,…,19,20)","x=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20)"),
	("tuple(range(20))","x=tuple(range(20))"),
	("{0,1,2,…,19,20}","x={0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20}"),
	("deque(range(20))","x=deque(range(20))","from collections import deque")
	],
"formatting strings":[
	("f\"a{x}\"","x=f\"num={num:n}\"","num=randrange(0,99)",{"randrange":randrange}),
	("\"a{}\".format(x)","x=\"num={0:n}\".format(num)","num=randrange(0,99)",{"randrange":randrange}),
	("\"a%i\"%x","x=\"num=%i\"%num","num=randrange(0,99)",{"randrange":randrange}),
	("\"a\"+str(x)","x=\"num=\"+str(num)","num=randrange(0,99)",{"randrange":randrange})
	],
"Double String concatenation":[
	("f\"{a}{b}\"","x=f\"{a:s}{b:s}\"","a=randstr(20)\nb=randstr(20)",{"randstr":randstr}),
	("\"{}{}\".format(a,b)","x=\"{:s}{:s}\".format(a,b)","a=randstr(20)\nb=randstr(20)",{"randstr":randstr}),
	("\"%s%s\"%(a,b)","x=\"%s%s\"%(a,b)","a=randstr(20)\nb=randstr(20)",{"randstr":randstr}),
	("\"\".join((a,b))","x=\"\".join((a,b))","a=randstr(20)\nb=randstr(20)",{"randstr":randstr}),
	("a+b","x=a+b","a=randstr(20)\nb=randstr(20)",{"randstr":randstr})
	],
"Triple String concatenation":[
	("f\"{a}{b}{c}\"","x=f\"{a:s}{b:s}{c:s}\"","a=randstr(20)\nb=randstr(20)\nc=randstr(20)",{"randstr":randstr}),
	("\"{}{}{}\".format(a,b,c)","x=\"{:s}{:s}{:s}\".format(a,b,c)","a=randstr(20)\nb=randstr(20)\nc=randstr(20)",{"randstr":randstr}),
	("\"%s%s%s\"%(a,b,c)","x=\"%s%s%s\"%(a,b,c)","a=randstr(20)\nb=randstr(20)\nc=randstr(20)",{"randstr":randstr}),
	("\"\".join((a,b,c))","x=\"\".join((a,b,c))","a=randstr(20)\nb=randstr(20)\nc=randstr(20)",{"randstr":randstr}),
	("a+b+c","x=a+b+c","a=randstr(20)\nb=randstr(20)\nc=randstr(20)",{"randstr":randstr})
	],
"single-value branching":[
	("elif equal","branch(randint(1,5))","from random import randint",{"branch":t_sb_elif_is}),
	("mapping","branch(randint(1,5))","from random import randint",{"branch":t_sb_keys})
	],
"multiple-value branching":[
	("elif equal","branch(choice(poss))","from random import choice",{"branch":t_mb_elif_is,"poss":poss_maybe}),
	("elif in","branch(choice(poss))","from random import choice",{"branch":t_mb_elif_in,"poss":poss_maybe}),
	#note: keys.get because that returns None when the key doesn't exist in the dict
	#not sure why that is so slow tbh - maybe dict size? idk
	("mapping","keys.get(choice(poss))","from random import choice",{"keys":keys_maybe,"poss":poss_maybe})
	],
"double array concatenation":[
	("(*a,*b)","x=(*a,*b)","a=rands()\nb=rands()",{"rands":(lambda:tuple(randiter(20,0,100)))}),
	("a+b (tuple)","x=a+b","a=rands()\nb=rands()",{"rands":(lambda:tuple(randiter(20,0,100)))}),
	("[*a,*b]","x=[*a,*b]","a=rands()\nb=rands()",{"rands":(lambda:list(randiter(20,0,100)))}),
	("a+b (list)","x=a+b","a=rands()\nb=rands()",{"rands":(lambda:list(randiter(20,0,100)))})
	],
"triple array concatenation":[
	("(*a,*b,*c)","x=(*a,*b,*c)","b=rands()\na=rands()\nc=rands()",{"rands":(lambda:tuple(randiter(20,0,100)))}),
	("a+b+c (tuple)","x=a+b+c","b=rands()\na=rands()\nc=rands()",{"rands":(lambda:tuple(randiter(20,0,100)))}),
	("[*a,*b,*c]","x=[*a,*b,*c]","b=rands()\na=rands()\nc=rands()",{"rands":(lambda:list(randiter(20,0,100)))}),
	("a+b+c (list)","x=a+b+c","b=rands()\na=rands()\nc=rands()",{"rands":(lambda:list(randiter(20,0,100)))})
	]
}

for nr in (5,20):
	TIMINGS[f"{nr}-char encryption"]=[
		(alg.upper()+" (hashlib)",f"hash(alg,randbytes({nr}))","",{"randbytes":randbytes,"hash":hashlib.new,"alg":alg})
		for alg in hashlib.algorithms_available
		]