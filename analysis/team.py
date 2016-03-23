import sys
import analysis
import itertools
from config import *

if COLORS:
	from termcolor import colored
else:
	def colored(a,*_):
		return a

def pad(i,l):
	return str(i)+' '*(l-len(str(i)))

def printdata(teamnum):
	teamobj = analysis.analyzeteam(teamnum)

	print colored("\nTEAM {}".format(teamobj.num),'red','on_green',attrs=['bold'])

	print colored("==== Defense ratings: ====",'red')
	defs_sorted = sorted(teamobj.defense_speed_normalized, key=teamobj.defense_speed_normalized.get)
	for i in reversed(defs_sorted):
		print colored(pad(i,16),'blue') + colored(pad(str(teamobj.defense_count[i]),5),'cyan') + colored(pad('('+str(int(teamobj.defense_speed_normalized[i]*10)/10.0)+'%)',9),'green') + '#'*(int(teamobj.defense_speed_normalized[i]/2))

	print colored("==== Best choices for defense: ====",'red')
	best_choices = []
	best_choice_class = []
	for i in defs_sorted:
		if not analysis.defs_class[i] in best_choice_class and not analysis.defs_class[i] == '-': # dash implies non-selectable
			best_choices.append(i)
			best_choice_class.append(analysis.defs_class[i])
			if len(best_choices) >= 4: ## only want the top 4 worst
				break
	for i in best_choices:
		print "Class {}: {} at {}%".format(colored(analysis.defs_class[i].upper(),'red'),colored(i,'blue'),colored(int(teamobj.defense_speed_normalized[i]*10)/10.0,'green'))

	print colored("==== Offense stats: ====",'red')
	print "---- Low goal: ----"
	print "{} low goals made".format(colored(teamobj.lowgoal_total + teamobj.auton_low,'magenta'))
	print "average of {} per match".format(colored(teamobj.lowgoal_avg,'magenta'))
	print "{} in auton".format(colored(teamobj.auton_low,'magenta'))
	print "---- High goal: ----"
	print "{} high goals made, {} missed ({} total)".format(colored(teamobj.highgoal_total + teamobj.auton_high,'magenta'),colored(teamobj.highgoal_miss,'magenta'),colored(teamobj.highgoal_total+teamobj.highgoal_miss+teamobj.auton_high,'magenta'))
	print "average of {} per match".format(colored(teamobj.highgoal_avg,'magenta'))
	print "successful {}% of the time".format(colored(int(teamobj.highgoal_prec*1000)/10.0,'magenta'))
	print "{} in auton".format(colored(teamobj.auton_high,'magenta'))

	print colored("==== Auton stats: ====",'red')
	print "{} low goals, {} high gloals".format(teamobj.auton_low,teamobj.auton_high)
	print "started with a boulder {} times ({}% of matches)".format(teamobj.auton_boulders,teamobj.auton_boulders / float(teamobj.num_matches) * 100)
	print "reached {} times ({}% of matches)".format(teamobj.auton_reaches,teamobj.auton_reaches / float(teamobj.num_matches) * 100)
	print "crossed {} times ({}% of matches)".format(teamobj.auton_breaches,teamobj.auton_breaches / float(teamobj.num_matches) * 100)

	print colored("==== Tower stats: ====",'red')
	print "challenged tower {} times ({}% of matches)".format(teamobj.tower_challenge,teamobj.tower_challenge/float(teamobj.num_matches) * 100)
	print "climbed tower {} times ({}% of matches)".format(teamobj.tower_scale,teamobj.tower_scale/float(teamobj.num_matches) * 100)
	print "partially climbed tower {} times ({}% of matches)".format(teamobj.tower_scale_partial,teamobj.tower_scale_partial/float(teamobj.num_matches) * 100)
	print "succeeded climbing tower {}% of attempts".format(teamobj.tower_scale_prec)

if len(sys.argv) != 2 and  __name__ == '__main__':
	print "usage: python {} <team_number>".format(sys.argv[0])
	sys.exit(1)
elif __name__ == '__main__':
	teamnum = sys.argv[1]
	printdata(teamnum)
