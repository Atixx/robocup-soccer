#!/usr/bin/env python

import threading
import time
import random
import sys
import multiprocessing as mp
import os
import pdb

# import agent types (positions)
from aigent.soccerpy.agent import Agent as A0
# strikers
from aigent.agent_1 import Agent as A1
# defenders
from aigent.agent_2 import Agent as A2
# goalie
from aigent.agent_3 import Agent as A3

# set team
TEAM_NAME = 'test'
NUM_PLAYERS = 1


if __name__ == "__main__":

    # return type of agent: midfield, striker etc.
    def agent_type(position):
    	return {
            2: A2,
            3: A3,
            4: A2,
            6: A2,
            7: A2,
    		8: A2,
    	}.get(position, A1)

    # spawn an agent of team_name, with position
    def spawn_agent(team_name, position):
        """
        Used to run an agent in a seperate physical process.
        """
        # return type of agent by position, construct
        a = A1() #@Atixx pruebo solo el agente A1
        #agent_type(position)()
        a.connect("192.168.0.103", 6000, team_name)
        a.play()

        # we wait until we're killed
        while 1:
            # we sleep for a good while since we can only exit if terminated.
            time.sleep(1)

    # spawn all agents as seperate processes for maximum processing efficiency
    agentthreads = []
    for position in xrange(1, NUM_PLAYERS+1):
        print "  Spawning agent %d..." % position

        at = mp.Process(target=spawn_agent, args=(TEAM_NAME, position))
        at.daemon = True
        at.start()

        agentthreads.append(at)

    print "Spawned %d agents." % len(agentthreads)
    print
    print "Playing soccer..."

    # wait until killed to terminate agent processes
    try:
        while 1:
            time.sleep(0.05)
    except KeyboardInterrupt:
        print
        print "Killing agent threads..."

        # terminate all agent processes
        count = 0
        for at in agentthreads:
            print "  Terminating agent %d..." % count
            at.terminate()
            count += 1
        print "Killed %d agent threads." % (count - 1)

        print
        print "Exiting."
        sys.exit()
