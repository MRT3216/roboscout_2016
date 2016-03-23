import sys
import analysis
import itertools

def pad(i,l):
	return str(i)+' '*(l-len(str(i)))

def printdata(teamnum):
	teamobj = analysis.analyzeteam(teamnum)

	print "TEAM {}".format(teamobj.num)

	print "==== Defense ratings: ===="
	defs_sorted = sorted(teamobj.defense_speed_normalized, key=teamobj.defense_speed_normalized.get)
	for i in reversed(defs_sorted):
		print pad(i,16) + pad(str(teamobj.defense_count[i]),5) + pad('('+str(int(teamobj.defense_speed_normalized[i]*10)/10.0)+'%)',9) + '#'*(int(teamobj.defense_speed_normalized[i]/2))

	print "==== Best choices for defense: ===="
	best_choices = []
	best_choice_class = []
	for i in defs_sorted:
		if not analysis.defs_class[i] in best_choice_class and not analysis.defs_class[i] == '-': # dash implies non-selectable
			best_choices.append(i)
			best_choice_class.append(analysis.defs_class[i])
			if len(best_choices) >= 4: ## only want the top 4 worst
				break
	for i in best_choices:
		print "Class {}: {} at {}%".format(analysis.defs_class[i].upper(),i,int(teamobj.defense_speed_normalized[i]*10)/10.0)

	print "==== Offense stats: ===="
	print "---- Low goal: ----"
	print "{} low goals made".format(teamobj.lowgoal_total + teamobj.auton_low)
	print "average of {} per match".format(teamobj.lowgoal_avg)
	print "{} in auton".format(teamobj.auton_low)
	print "---- High goal: ----"
	print "{} high goals made, {} missed ({} total)".format(teamobj.highgoal_total + teamobj.auton_high,teamobj.highgoal_miss,teamobj.highgoal_total+teamobj.highgoal_miss+teamobj.auton_high)
	print "average of {} per match".format(teamobj.highgoal_avg)
	print "successful {}% of the time".format(int(teamobj.highgoal_prec*1000)/10.0)
	print "{} in auton".format(teamobj.auton_high)

	print "==== Auton stats: ===="
	print "{} low goals, {} high gloals".format(teamobj.auton_low,teamobj.auton_high)
	print "started with a boulder {} times ({}% of matches)".format(teamobj.auton_boulders,teamobj.auton_boulders / float(teamobj.num_matches) * 100)
	print "reached {} times ({}% of matches)".format(teamobj.auton_reaches,teamobj.auton_reaches / float(teamobj.num_matches) * 100)
	print "crossed {} times ({}% of matches)".format(teamobj.auton_breaches,teamobj.auton_breaches / float(teamobj.num_matches) * 100)

	print "==== Tower stats: ===="
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
