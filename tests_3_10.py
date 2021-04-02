#!/usr/bin/env python3
from tests_base import poss_maybe

def t_sb_match(num):
	match num:
		case 1:
			return "Sehr Gut"
		case 2:
			return "Gut"
		case 3:
			return "Befriedigend"
		case 4:
			return "Genügend"
		case 5:
			return "Nicht Genügend"

def t_mb_match(maybe):
	match maybe.lower():
		case "j"|"ja"|"y"|"yes":
			return True
		case "n"|"nein"|"no":
			return False
		case _:
			return None

def timings_mod(timings):
	timings["single-value branching"].append(
		("match case","x=branch(randint(1,5))","from random import randint",{"branch":t_sb_match})
		)
	timings["multiple-value branching"].append(
		("match case","branch(choice(poss))","from random import choice",{"branch":t_mb_match,"poss":poss_maybe})
		)
