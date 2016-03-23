#### config, python syntax
# this is mostly for the server, but the analysis client needs to import it for a few things too

DATABASE = "data/data.db"

COLORS = True ## enable colored printing of output; disable if you see random characters

LOGFILE = "gather-server.log"

"""
stuff i took out:

team_alliance_ans text,
win_alliance_ans text,
ranking_red_count int,
ranking_blue_count int,
robot_work_ans text,
"""

DATASCHEMA = """(
matchnum int,
teamnum int,

score_red int,
score_blue int,

portcullis_crosscount int,
cheval_crosscount int,
moat_crosscount int,
ramparts_crosscount int,
drawbridge_crosscount int,
sallyport_crosscount int,
rockwall_crosscount int,
roughterrain_crosscount int,
lowbar_crosscount int,

portcullis_def text,
cheval_def text,
moat_def text,
ramparts_def text,
drawbridge_def text,
sallyport_def text,
rockwall_def text,
roughterrain_def text,
lowbar_def text,

lowshoot_count int,
highshoot_a_count int,
highshoot_m_count int,
pickball_ans text,
passball_count int,
upramp_ans text,
climb_ans text,
pushdefense_count int,

autonboulder_ans text,
autonreach_ans text,
autonbreach_ans text,
autonlow_count int,
autonhigh_count int,

notes text
)"""

DSCH_SHORT = []
for i in DATASCHEMA.split('\n'):
	a = i.split()
	if len(a) == 2:
		DSCH_SHORT.append(a[0])

class defense:
	def __init__(self,name,did,answers=['slow','fast']):
		self.name = name
		self.did = did
		self.answers = answers

DEFENSES = [
	defense("Portcullis",'portcullis',['assist','alone']),
	defense("Cheval de Frise",'cheval'),
	defense("Moat",'moat'),
	defense("Ramparts",'ramparts'),
	defense("Drawbridge",'drawbridge',['assist','alone']),
	defense("Sally Port",'sallyport',['assist','alone']),
	defense("Rock Wall",'rockwall'),
	defense("Rough Terrain",'roughterrain'),
	defense("Low Bar",'lowbar')
]

class question:
	def __init__(self,ques,qid,count=False,ans=['no','yes']):
		self.ques = ques
		self.qid = qid
		self.answers = ans
		self.count = count

QUESTIONS1 = [
	question("Low goal scores",'lowshoot',True,[]),
	question("High goal fails",'highshoot_a',True,[]),
	question("High goal scores",'highshoot_m',True,[]),
	question("Boulder pick up speed",'pickball',False,['slow','fast']),
	question("Passed boulders",'passball',True,[]), ## teamwork?
	question("Challenged tower",'upramp'),
	question("Climbed tower",'climb',False,['no','partial','full']),
	question("Defensive pushing",'pushdefense',True,[])
]

QUESTIONS2 = [
	question("(AUTON) started with a boulder",'autonboulder'),
	question("(AUTON) Reached a defense",'autonreach'),
	question("(AUTON) Crossed a defense",'autonbreach',False,['none','portcullis','cheval','moat','ramparts','drawbridge','sallyport','rockwall','roughterrain','lowbar']),
	question("(AUTON) Low goal scores",'autonlow',True,[]),
	question("(AUTON) High goal scores",'autonhigh',True,[])
]

### not included for now
QUESTIONS3 = [
	question("This robot's alliance",'team_alliance',False,['red','blue']),
	question("Winning alliance",'win_alliance',False,['red','blue']),
	question("Red RP (excluding winning bonus)",'ranking_red',True,[]),
	question("Blue RP (excluding winning bonus)",'ranking_blue',True,[]),
	question("Precentage of alliance's work",'robot_work',False,['0%','1-33%','33-66%','66-99%','basically all of it'])
]
