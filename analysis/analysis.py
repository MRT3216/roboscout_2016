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

class team(object):
	def __init__(self,num):
		self.num = num

class alliance(object):
	def __init__(self,teams):
		self.teams = teams

class match(object):
	def __init__(self,alliance1,alliance2):
		self.alliance1 = alliance1
		self.alliance2 = alliance2

#defs = ['portcullis','cheval','moat','ramparts','drawbridge','sallyport','rockwall','roughterrain','lowbar']
defs_class = {'portcullis':'a','cheval':'a','moat':'b','ramparts':'b','drawbridge':'c','sallyport':'c','rockwall':'d','roughterrain':'d','lowbar':'-'}
defs = defs_class.keys()

def analyzeteam(num):
	teamobj = team(num)
	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	c.execute('SELECT * FROM matches WHERE teamnum=?',(num,))
	matchdata = c.fetchall() # raw
	matches = [{i:j for (i,j) in zip(DSCH_SHORT,k)} for k in matchdata]
	teamobj.matchdata = matches
	defense_speed_raw = {i:0 for i in defs}
	autondefenses = {i:0 for i in defs}
	teamobj.num_matches = len(matches)
	lowgoal_total = 0
	highgoal_total = 0
	highgoal_miss = 0
	for i in matches:
		## figure out their best defenses
		for d in defs:
			count = i.get(d+'_crosscount',0)
			speed = i.get(d+'_def','what')
			sm = {u'slow':1,u'fast':2}.get(speed,0) # speed multiplier
			defense_speed_raw[d] += count*sm
		## also think about auton defenses
		autondefense = i.get('autonbreach_ans','none')
		if str(autondefense) in defs:
			defense_speed_raw[str(autondefense)] += 5
			autondefenses[str(autondefense)] += 1
		### Offense
		lowgoal_total += i.get('lowshoot_count',0)
		highgoal_total += i.get('highshoot_a_count',0)
		highgoal_miss += i.get('highshoot_m_count',0)
	teamobj.lowgoal_total = lowgoal_total
	if len(matches) != 0:
		teamobj.lowgoal_avg = lowgoal_total / float(len(matches))
		teamobj.highgoal_avg = highgoal_total / float(len(matches))
	else:
		teamobj.lowgoal_avg = 0
		teamobj.highgoal_avg = 0
	teamobj.highgoal_total = highgoal_total
	teamobj.highgoal_miss = highgoal_miss
	if highgoal_total + highgoal_miss != 0:
		teamobj.highgoal_prec = highgoal_total / float(highgoal_total + highgoal_miss)
	else:
		teamobj.highgoal_prec = 0
	## find the prevalance of teleop defenses
	teamobj.defense_speed_raw = defense_speed_raw
	teamobj.defenses_auton = autondefenses
	maxdef = sorted(defense_speed_raw.values())[-1]
	if maxdef != 0:
		defense_speed = {d:(i/float(maxdef))*100 for (d,i) in zip(defense_speed_raw.keys(),defense_speed_raw.values())}
	else:
		defense_speed = {i:0 for i in defs}
	team.defense_speed_normalized = defense_speed
	conn.close()
	return teamobj

def analyzealliance(alist):
	teams = []
	for i in alist:
		teams.append(analyzeteam(i))
	allianceobj = alliance(alist)
	allianceobj.teamobjs = teams
	return allianceobj

def analyzematch(ared,ablue):
	red = analyzealliance(ared)
	blue = analyzealliance(ablue)
	matchobj = match(ared,ablue)
	matchobj.redobjs = red
	matchobj.blueobjs = blue
	return matchobj

if __name__ == "__main__":
	print "look in README for info on the right script to use"
