roboscout
-------

Requirements:
- Flask https://flask.pocoo.org/
- termcolor https://pypi.python.org/pypi/termcolor
- and of course Python 2.7


How to use it:

- go to the `gathering` folder and run `python main.py` to start the gathering server.
- any computer that connects to the IP address of the machine running that server on port 5000 will see the data gathering screen below (if the ip is `10.0.1.25`, then type `10.0.1.25:5000` into your browser)
- use the gathering page to submit data on each team (you can safely ignore final score for now)
- once you have gathered data and want to analyze it, copy `gathering/data/data.db` into `analysis/data/data.db` using whatever method you see fit: airsync, rsync, just manual copying, symlinking, etc.
- then in the analysis folder, there are several scripts (only one of them works however):
- to analyze a team: `python team.py ####` where __####__ is the number of a team you want to analyze. a bunch of data will be printed out, similar to the output below.


__Data acquisition:__

![data acquisition screen](https://github.com/red-green/roboscout_2016/blob/master/gathering/templates/layout.png?raw=true)

__Team analysis__ (sample random data) [not even close to done yet]:

```
$ python team.py 4334
TEAM 4334
==== Defense ratings: ====
portcullis      4    (100.0%) ##################################################
drawbridge      4    (95.8%)  ###############################################
roughterrain    4    (91.6%)  #############################################
sallyport       2    (50.0%)  #########################
rockwall        2    (33.3%)  ################
ramparts        1    (8.3%)   ####
moat            0    (0.0%)   
lowbar          0    (0.0%)   
cheval          0    (0.0%)   
==== Best choices for defense: ====
Class A: cheval at 0.0%
Class B: moat at 0.0%
Class D: rockwall at 33.3%
Class C: sallyport at 50.0%
==== Offense stats: ====
---- Low goal: ----
3 low goals made
average of 1.5 per match
0 in auton
---- High goal: ----
6 high goals made, 5 missed (11 total)
average of 2.0 per match
successful 44.4% of the time
2 in auton
==== Auton stats: ====
0 low goals, 2 high gloals
started with a boulder 2 times (100.0% of matches)
reached 2 times (100.0% of matches)
crossed 2 times (100.0% of matches)
==== Tower stats: ====
challenged tower 2 times (100.0% of matches)
climbed tower 1 times (50.0% of matches)
partially climbed tower 1 times (50.0% of matches)
succeeded climbing tower 50.0% of attempts
```

Some planning I did a while ago about this app:

- gets data like number of goal crossings, crossing speed, boulder stats, challenge and capture of tower, auton stats, and final game score
- run on a raspberry pi
- backpack in the stands with several ethernets coming out of it:
- contains raspberry pi, router, power source, and some communication method back to pit area
- maybe we can run an ac power cord, if not, big multirotor batteries with a switching power supply
- need to find an 8-port router for linking the laptops together
- so there are 6 laptops linked to this hub, all accessing the raspberry pi’s webserver
- the webserver serves a page to enter various data about the specific bot
- each scouter will fill out one form per match, with 6 computers being able to fill out the data on the whole alliance (including our own bot when we’re there)
- the raspberry pi will then periodically sync the database back to the pit area computer (a more powerful one), which will do a bunch of analysis on it
- alternately, there is a 7th laptop at the scouting camp that does all the analysis, and the drive team confers with it before the match (no long-distance syncing needed)
- Match-based data for planning:
	- {opposing, partner} alliance strengths and weaknesses: outer works defense crossing ablilties, defense, offense low and high
	- suggested roles for us and our teammates’ bots (defense, offense low, offense high, supply), best opposing strategy
	- suggested outerworks defense selections
	- suggested robot placement for auton
	- match history overview for each bot
	- estimated outcome
- Robot-based data:
	- strengths and weaknesses, best and worst roles
	- best opposing strategy
	- past match preformance
- Finals selection suggestion data:
	- (this could take a while to compute, we’d run this analysis between quals and final selections, need to figure out how fast it can be done)
	- top teams in general
	- top teams that pair with our skills (or the skills of any given bot)
	- top alliances (selected for most skills)
	- what the computer will do is run every single possible combination of teams in alliances of 3, and compare these results numerically
- easy way to view and edit historic data in case a scouter makes a mistake
- possibility of sharing this data with other teams?
- of course we’d share upcoming match analysis with our alliance mates
- maybe share finalist selection suggestions?
- pit scouting is better suited for another app or paper
- use pit scouting and practice field scouting until we have enough of this data to go off of
