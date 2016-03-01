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
	if len(matchdata) == 0:
		print "ERROR: team {} has no match data".format(num)
	matches = [{i:j for (i,j) in zip(DSCH_SHORT,k)} for k in matchdata]
	teamobj.matchdata = matches
	defense_speed_raw = {i:0 for i in defs}
	defense_count = {i:0 for i in defs}
	autondefenses = {i:0 for i in defs}
	teamobj.num_matches = len(matches)
	lowgoal_total = 0
	highgoal_total = 0
	highgoal_miss = 0

	auton_high = 0
	auton_low = 0
	auton_boulders = 0
	auton_reaches = 0
	auton_breaches = 0

	tower_challenge = 0
	tower_scale_partial = 0
	tower_scale = 0

	for i in matches:
		## figure out their best defenses
		for d in defs:
			count = i.get(d+'_crosscount',0)
			speed = i.get(d+'_def','what')
			sm = {u'slow':1,u'fast':2,u'assist':0.5,u'alone':3}.get(speed,0) # speed multiplier
			defense_speed_raw[d] += count*sm
			defense_count[d] += count
		## also think about auton defenses
		autondefense = i.get('autonbreach_ans','none')
		if str(autondefense) in defs:
			defense_speed_raw[str(autondefense)] += 5
			autondefenses[str(autondefense)] += 1
			defense_count[str(autondefense)] += 1
		## offense
		lowgoal_total += i.get('lowshoot_count',0)
		highgoal_total += i.get('highshoot_a_count',0)
		highgoal_miss += i.get('highshoot_m_count',0)
		## auton
		if i.get('autonboulder_ans','no') == 'yes':
			auton_boulders += 1
		if i.get('autonreach_ans','no') == 'yes':
			auton_reaches += 1
		if i.get('autonbreach_ans','none') != 'none':
			auton_breaches += 1
		auton_high += i.get('autonhigh_count',0)
		auton_low += i.get('autonlow_count',0)
		## endgame stuff
		if i.get('upramp_ans','no') == 'yes':
			tower_challenge += 1
		if i.get('climb_ans','no') == 'partial':
			tower_scale_partial += 1
		elif i.get('climb_ans','no') == 'full':
			tower_scale += 1

	teamobj.auton_boulders = auton_boulders
	teamobj.auton_reaches = auton_reaches
	teamobj.auton_breaches = auton_breaches
	teamobj.auton_low = auton_low
	teamobj.auton_high = auton_high

	teamobj.tower_challenge = tower_challenge
	teamobj.tower_scale_partial = tower_scale_partial
	teamobj.tower_scale = tower_scale
	if tower_scale + tower_scale_partial != 0:
		teamobj.tower_scale_prec = tower_scale / float(tower_scale + tower_scale_partial) * 100
	else:
		teamobj.tower_scale_prec = 0

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
	teamobj.defense_count = defense_count
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
