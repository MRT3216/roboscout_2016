import sys
import analysis
import team
import itertools
from config import *

if COLORS:
	from termcolor import colored
else:
	def colored(a,*_):
		return a

def pad(i,l):
	return str(i)+' '*(l-len(str(i)))

def printdata(teams):
	allianceobj = analysis.analyzealliance(teams)

	print colored("\nALLIANCE {}".format(','.join(teams)),'red','on_green',attrs=['bold'])

	print colored("==== Defense ratings: ====",'red')
	defs_sorted = sorted(allianceobj.defense_speed_normalized, key=allianceobj.defense_speed_normalized.get)
	for i in reversed(defs_sorted):
		print colored(pad(i,16),'blue') + colored(pad(str(allianceobj.defense_count[i]),5),'cyan') + colored(pad('('+str(int(allianceobj.defense_speed_normalized[i]*10)/10.0)+'%)',9),'green') + '#'*(int(allianceobj.defense_speed_normalized[i]/2))

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
		print "Class {}: {} at {}%".format(colored(analysis.defs_class[i].upper(),'red'),colored(i,'blue'),colored(int(allianceobj.defense_speed_normalized[i]*10)/10.0,'cyan'))


if len(sys.argv) != 2 and __name__ == '__main__':
	print "usage: python {} <team1>,<team2>,<team3>".format(sys.argv[0])
	sys.exit(1)
elif __name__ == '__main__':
	teams = sys.argv[1].split(',')
	print colored("\nBEGIN DATA PRINTOUT",'blue','on_red',attrs=['bold'])
	for i in teams:
		team.printdata(int(i))
	printdata(teams)
	print colored("\nEND DATA PRINTOUT",'blue','on_red',attrs=['bold'])
