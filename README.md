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

__Team analysis:__

![colored output of team analysis](https://github.com/red-green/roboscout_2016/blob/master/analysis/templates/example-colored.png?raw=true)

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

also a full(ish) printout (with actual data)

```
$ python match.py 539,1719,1123 5587,623,1418

BEGIN DATA PRINTOUT

TEAM 539
==== Defense ratings: ====
lowbar          12   (100.0%) ##################################################
portcullis      5    (41.6%)  ####################
cheval          3    (20.0%)  ##########
sallyport       2    (11.6%)  #####
roughterrain    0    (0.0%)   
moat            0    (0.0%)   
drawbridge      0    (0.0%)   
ramparts        0    (0.0%)   
rockwall        0    (0.0%)   
==== Best choices for defense: ====
Class D: rockwall at 0.0%
Class B: ramparts at 0.0%
Class C: drawbridge at 0.0%
Class A: cheval at 20.0%
==== Offense stats: ====
---- Low goal: ----
11 low goals made
average of 1.22222222222 per match
0 in auton
---- High goal: ----
0 high goals made, 0 missed (0 total)
average of 0.0 per match
successful 0.0% of the time
0 in auton
==== Auton stats: ====
0 low goals, 0 high gloals
started with a boulder 5 times (55.5555555556% of matches)
reached 6 times (66.6666666667% of matches)
crossed 3 times (33.3333333333% of matches)
==== Tower stats: ====
challenged tower 2 times (22.2222222222% of matches)
climbed tower 0 times (0.0% of matches)
partially climbed tower 0 times (0.0% of matches)
succeeded climbing tower 0% of attempts

TEAM 1719
==== Defense ratings: ====
rockwall        11   (100.0%) ##################################################
sallyport       6    (81.8%)  ########################################
cheval          6    (54.5%)  ###########################
lowbar          5    (45.4%)  ######################
ramparts        5    (40.9%)  ####################
roughterrain    3    (27.2%)  #############
moat            2    (18.1%)  #########
portcullis      0    (0.0%)   
drawbridge      0    (0.0%)   
==== Best choices for defense: ====
Class C: drawbridge at 0.0%
Class A: portcullis at 0.0%
Class B: moat at 18.1%
Class D: roughterrain at 27.2%
==== Offense stats: ====
---- Low goal: ----
0 low goals made
average of 0.0 per match
0 in auton
---- High goal: ----
0 high goals made, 0 missed (0 total)
average of 0.0 per match
successful 0.0% of the time
0 in auton
==== Auton stats: ====
0 low goals, 0 high gloals
started with a boulder 1 times (12.5% of matches)
reached 1 times (12.5% of matches)
crossed 0 times (0.0% of matches)
==== Tower stats: ====
challenged tower 1 times (12.5% of matches)
climbed tower 0 times (0.0% of matches)
partially climbed tower 0 times (0.0% of matches)
succeeded climbing tower 0% of attempts

TEAM 1123
==== Defense ratings: ====
lowbar          9    (100.0%) ##################################################
moat            8    (90.4%)  #############################################
roughterrain    7    (66.6%)  #################################
rockwall        6    (57.1%)  ############################
portcullis      2    (28.5%)  ##############
sallyport       1    (14.2%)  #######
ramparts        1    (4.7%)   ##
drawbridge      0    (0.0%)   
cheval          0    (0.0%)   
==== Best choices for defense: ====
Class A: cheval at 0.0%
Class C: drawbridge at 0.0%
Class B: ramparts at 4.7%
Class D: rockwall at 57.1%
==== Offense stats: ====
---- Low goal: ----
0 low goals made
average of 0.0 per match
0 in auton
---- High goal: ----
0 high goals made, 0 missed (0 total)
average of 0.0 per match
successful 0.0% of the time
0 in auton
==== Auton stats: ====
0 low goals, 0 high gloals
started with a boulder 1 times (12.5% of matches)
reached 2 times (25.0% of matches)
crossed 2 times (25.0% of matches)
==== Tower stats: ====
challenged tower 2 times (25.0% of matches)
climbed tower 0 times (0.0% of matches)
partially climbed tower 0 times (0.0% of matches)
succeeded climbing tower 0% of attempts

TEAM 5587
==== Defense ratings: ====
rockwall        9    (100.0%) ##################################################
portcullis      6    (66.6%)  #################################
drawbridge      4    (44.4%)  ######################
roughterrain    3    (33.3%)  ################
lowbar          1    (3.7%)   #
moat            0    (0.0%)   
cheval          0    (0.0%)   
ramparts        0    (0.0%)   
sallyport       0    (0.0%)   
==== Best choices for defense: ====
Class C: sallyport at 0.0%
Class B: ramparts at 0.0%
Class A: cheval at 0.0%
Class D: roughterrain at 33.3%
==== Offense stats: ====
---- Low goal: ----
0 low goals made
average of 0.0 per match
0 in auton
---- High goal: ----
0 high goals made, 0 missed (0 total)
average of 0.0 per match
successful 0.0% of the time
0 in auton
==== Auton stats: ====
0 low goals, 0 high gloals
started with a boulder 3 times (37.5% of matches)
reached 5 times (62.5% of matches)
crossed 4 times (50.0% of matches)
==== Tower stats: ====
challenged tower 1 times (12.5% of matches)
climbed tower 0 times (0.0% of matches)
partially climbed tower 0 times (0.0% of matches)
succeeded climbing tower 0% of attempts

TEAM 623
==== Defense ratings: ====
rockwall        18   (100.0%) ##################################################
portcullis      3    (25.7%)  ############
moat            4    (22.8%)  ###########
drawbridge      2    (17.1%)  ########
lowbar          3    (11.4%)  #####
ramparts        1    (2.8%)   #
sallyport       1    (1.4%)   
roughterrain    0    (0.0%)   
cheval          0    (0.0%)   
==== Best choices for defense: ====
Class A: cheval at 0.0%
Class D: roughterrain at 0.0%
Class C: sallyport at 1.4%
Class B: ramparts at 2.8%
==== Offense stats: ====
---- Low goal: ----
2 low goals made
average of 0.285714285714 per match
0 in auton
---- High goal: ----
0 high goals made, 0 missed (0 total)
average of 0.0 per match
successful 0.0% of the time
0 in auton
==== Auton stats: ====
0 low goals, 0 high gloals
started with a boulder 4 times (57.1428571429% of matches)
reached 0 times (0.0% of matches)
crossed 0 times (0.0% of matches)
==== Tower stats: ====
challenged tower 6 times (85.7142857143% of matches)
climbed tower 2 times (28.5714285714% of matches)
partially climbed tower 0 times (0.0% of matches)
succeeded climbing tower 100.0% of attempts

TEAM 1418
==== Defense ratings: ====
lowbar          13   (100.0%) ##################################################
portcullis      9    (62.8%)  ###############################
ramparts        4    (31.4%)  ###############
cheval          5    (25.7%)  ############
sallyport       7    (17.1%)  ########
roughterrain    1    (14.2%)  #######
rockwall        1    (5.7%)   ##
moat            0    (0.0%)   
drawbridge      0    (0.0%)   
==== Best choices for defense: ====
Class C: drawbridge at 0.0%
Class B: moat at 0.0%
Class D: rockwall at 5.7%
Class A: cheval at 25.7%
==== Offense stats: ====
---- Low goal: ----
11 low goals made
average of 1.0 per match
4 in auton
---- High goal: ----
6 high goals made, 2 missed (8 total)
average of 0.857142857143 per match
successful 75.0% of the time
0 in auton
==== Auton stats: ====
4 low goals, 0 high gloals
started with a boulder 4 times (57.1428571429% of matches)
reached 4 times (57.1428571429% of matches)
crossed 5 times (71.4285714286% of matches)
==== Tower stats: ====
challenged tower 1 times (14.2857142857% of matches)
climbed tower 1 times (14.2857142857% of matches)
partially climbed tower 0 times (0.0% of matches)
succeeded climbing tower 100.0% of attempts

ALLIANCE 539,1719,1123
==== Defense ratings: ====
lowbar          26   (100.0%) ##################################################
rockwall        17   (55.7%)  ###########################
sallyport       9    (40.1%)  ####################
moat            10   (37.7%)  ##################
roughterrain    10   (32.7%)  ################
portcullis      7    (30.3%)  ###############
cheval          9    (29.5%)  ##############
ramparts        6    (16.3%)  ########
drawbridge      0    (0.0%)   
==== Best choices for defense: ====
Class C: drawbridge at 0.0%
Class B: ramparts at 16.3%
Class A: cheval at 29.5%
Class D: roughterrain at 32.7%

ALLIANCE 5587,623,1418
==== Defense ratings: ====
rockwall        28   (100.0%) ##################################################
portcullis      18   (76.5%)  ######################################
lowbar          17   (62.5%)  ###############################
drawbridge      6    (28.1%)  ##############
roughterrain    4    (21.8%)  ##########
ramparts        5    (18.7%)  #########
cheval          5    (14.0%)  #######
moat            4    (12.5%)  ######
sallyport       8    (10.1%)  #####
==== Best choices for defense: ====
Class C: sallyport at 10.1%
Class B: moat at 12.5%
Class A: cheval at 14.0%
Class D: roughterrain at 21.8%

MATCH 539,1719,1123 vs 5587,623,1418

.........

END DATA PRINTOUT
```
