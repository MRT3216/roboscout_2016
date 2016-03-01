import sys
import analysis

def pad(i,l):
	return str(i)+' '*(l-len(str(i)))

if len(sys.argv) != 2:
	print "usage: python {} <team_number>".format(sys.argv[0])
	sys.exit(1)

teamnum = sys.argv[1]

teamobj = analysis.analyzeteam(teamnum)

print "TEAM {}".format(teamobj.num)

print "==== Defense ratings: ===="
defs_sorted = sorted(teamobj.defense_speed_normalized, key=teamobj.defense_speed_normalized.get)
for i in reversed(defs_sorted):
	print pad(i,16)+pad(str(int(teamobj.defense_speed_normalized[i]*10)/10.0)+'%',7) + '#'*(int(teamobj.defense_speed_normalized[i]/2))

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
print "{} low goals made".format(teamobj.lowgoal_total)
print "average of {} per match".format(teamobj.lowgoal_avg)
print "---- High goal: ----"
print "{} high goals made, {} missed ({} total)".format(teamobj.highgoal_total,teamobj.highgoal_miss,teamobj.highgoal_total+teamobj.highgoal_miss)
print "average of {} per match".format(teamobj.highgoal_avg)
print "successful {}% of the time".format(int(teamobj.highgoal_prec*10)/10.0)
