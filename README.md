roboscout
-------

I don't really have time to document this right now much...

Data acquisition:

![data acquisition screen](https://github.com/red-green/roboscout_2016/blob/master/gathering/templates/layout.png?raw=true)

Team analysis (sample random data) [not even close to done yet]:

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
