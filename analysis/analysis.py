## this file does all the magic
import os,sys ## sync the config because python is being dumb
fd = open('config.py','w');fd.write(open('../config.py','r').read());fd.close()

import sqlite3
from config import *
from pprint import pprint

'''
conn = sqlite3.connect(DATABASE)
c = conn.cursor()
c.execute('')
c.fetchall()

conn.commit()
conn.close()
'''

def pad(i,l):
	return str(i)+' '*(l-len(str(i)))

class team(object):
	def __init__(self,num):
		self.num = num
	def __repr__(self):
		ret = ""
		ret += "TEAM {}\n========\n".format(self.num)
		ret += "==== Offense stats: ====\n"
		ret += "==== Defense ratings: ====\n"
		for i in sorted(self.defense_speed_normalized, key=self.defense_speed_normalized.get, reverse=True):
			ret += pad(i,16)+pad(str(int(self.defense_speed_normalized[i]))+'%',5) + '#'*(int(self.defense_speed_normalized[i]/3)) + '\n'
		return ret

defs = ['portcullis','cheval','moat','ramparts','drawbridge','sallyport','rockwall','roughterrain','lowbar']

def analyzeteam(num):
	teamobj = team(num)
	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	c.execute('SELECT * FROM matches WHERE teamnum=?',(num,))
	matchdata = c.fetchall()
	matches = [{i:j for (i,j) in zip(DSCH_SHORT,k)} for k in matchdata]
	teamobj.matchdata = matches
	defense_speed_raw = {i:0 for i in defs}
	for i in matches:
		## win/loss count later once i figure out who won
		## figure out their best defenses
		for d in defs:
			count = i.get(d+'_crosscount',0)
			speed = i.get(d+'_def','what')
			sm = {u'slow':1,u'fast':2}.get(speed,0)
			defense_speed_raw[d] += count*sm
		## also think about auton defenses
		autondefense = i.get('autonbreach_ans','none')
		if str(autondefense) in defs:
			defense_speed_raw[str(autondefense)] += 5
	## find the prevalance of teleop defenses
	teamobj.defense_speed_raw = defense_speed_raw
	maxdef = sorted(defense_speed_raw.values())[-1]
	if maxdef != 0:
		defense_speed = {d:(i/float(maxdef))*100 for (d,i) in zip(defense_speed_raw.keys(),defense_speed_raw.values())}
	else:
		defense_speed = {i:0 for i in defs}
	team.defense_speed_normalized = defense_speed
	conn.close()
	return teamobj

def analyzealliance(alist):
	pass

def analyzematch(red,blue):
	pass

if __name__ == "__main__":
	print analyzeteam(3216)
