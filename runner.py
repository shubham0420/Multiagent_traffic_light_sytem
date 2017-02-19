"""
 This code is not working right now.
 This file first generates route file and then runs the simulation
 I have created a very basic route file right now, which can be modified later for complex route file.

"""



from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import subprocess
import random
#import sumolib

# we need to import python modules from the $SUMO_HOME/tools directory
try:
    sys.path.append(os.path.join(os.path.dirname(
        __file__), '..', '..', '..', '..', "tools"))  # tutorial in tests
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
        os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in docs
    from sumolib import checkBinary
except ImportError:
    sys.exit(
        "please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")

import traci


agents = {
		'0':['1'],
		'1':['0','2','4'],
		'2':['1'],
		'3':['4'],
		'4':['3','1','5','7'],
		'5':['4'],
		'6':['7'],
		'7':['6','4','8'],
		'8':['7']
	}

edges = {
		'e1':['1','0'],
		'e2':['2','1'],
		'e3':['3','4'],
		'e4':['5','4'],
		'e6':['6','7'],
		'e7':['8','7'],
		'e8':['4','1'],
		'e9':['7','4'],
		'e11':['0','1'],
		'e12':['1','2'],
		'e13':['4','3'],
		'e14':['4','5'],
		'e16':['7','6'],
		'e17':['7','8'],
		'e18':['1','6'],
		'e19':['4','7']
}

neighbour_edges = {}

for i in edges:
	print(type(i))
	print(i)
	neighbour_edges[i] = []
	for j in edges:
		if edges[i][1] == edges[j][0]:
			if edges[i][0] != edges[j][1]:
				neighbour_edges[i].append(j)


def algorithm3():

	'''
		for agent in agents:
			state[agent] = 1
			action[agent] = 1
			for neighbour in neighbour[agent]:
				#action[neighbour] = 1
				M[agent][neighbour] = 1/len(agents[agent])     ###  probability that neighbour takes action j is given by 1/(total number of actions neighbour can take ( which is the total number of partial states of the neighbour (what i think now)))
				Q[agent][neighour] = 0                  ###  Consedering starting Q zero for each agent neighbour.	
	'''

	for agnt in agents:
		maximum = -999
		best_action = 0
		agent = agents[agnt]
		for neighbour in agent:
			for state in range(4):
				for action in range(2):
					M[agent][neighbour][state][action] = V[state][action]/sum([a for action in state for state in V ])        ## (Count of visit to action a when both in state i and j)/ (sum of count of visit to all actions when in state i and j)

			
			br = max([[M[agent][neighbour][current_state][neighbour_action]*Q[agent][neighbour][current_state][agent_action][neighbour_action] for neighbour_action in range(2)] for agent_action in range(2)])  # find max of all the actions that agent can take. (We take each action of agent and find the sum of all Q*M for all actions that neighour can take and then find the max among all the sums)



			for state in range(4):
				for agent_action in range(2):
					for neighbour_action in range(2):
						Q[agent][neighbour][state][neighbour_action][agent_action] = (1-alpha)*Q[agent][neighour][state][neighbour_action][agent_action] + alpha*(reward + gamma*br)



			for state in range(4):
				for agent_action in range(2):
					for neighbour_action in range(2):
						value = M[agent][neighbour][current_state][neighbour_action]*Q[agent][neighour][state][neighbour_action][agent_action]   
						if value > maximum:
							maximum = value
							best_action = agent_action

			action_agent[i] = agent_action




'''
Algorithm 2 is wrong
I misunderstood few things
'''

"""
def algorithm2():
	for agent in agents:
		state[agent] = 1
		action[agent] = 1
		M[agent] = {}
		Q[agent] = {}
		#print(agent)
		#print('--------------------')
		for neighbour in agents[agent]:
			#action[neighbour] = 1
			#print(neighbour)
			M[agent][neighbour] = 1/len(agents[neighbour])      
			Q[agent][neighbour] = 0             

'''
I think we are defining 4 states for 2 neighbours . 00,04,40,44.
actions contains going from 00 to any of 04,40,44 and so on.
Structure of M is like first we go to agent then to one of its neighbour. 
Now, one by one we go to each possible joint state .
In each joint state we see the action that we can pick. 
Ex:-
We are in state 00. now we are going to pick action 1 which means we are going to state 04. next we see action 2 which means we are going to state 40 and so on.
					00
				   / | \
				  /  |  \
				04  40  44


'''

	for step in timestep:
		for agent in agents:
			for neighbour in agents[agent]:
				for state in states:
					for action in actions:
						M[agent][neighbour][state][action] = V[agent][neighbour][state][action]/sum([V[agent][neighbour][state][a] for a in actions])   ## (Count of visit to action a when both in state i and j)/ (sum of count of visit to all actions when in state i and j)

				
				br = max([sum([M[agent][neighbour][current_state][action]*Q[agent][neighbour][current_state][action] for a in actions) for ac in actions)  # find max of all the actions that agent can take. (We take each action of agent and find the sum of all Q*M for all actions that neighour can take and then find the max among all the sums)

				Q[agent][neighbour] = (1-alpha)*Q[agent][neighbour] + alpha*(r + gamma*br)

				actions[agent] = argmax([sum([Q[agent][n][a]*M[agent][n][a] for a in actions[n]]) for n in neighbours])



"""
def generate_routefile():
	random.seed(42)
	N= 3600
	a = 1./10
	b = 1./15
	c = 1./10
	d = 1./20
	with open('trafficRoutes.rou.xml','w') as routes:
		print(""" <routes>
		<vType id="typeWE" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="16.67" guiShape="passenger"/>
        <vType id="typeNS" accel="0.8" decel="4.5" sigma="0.5" length="7" minGap="3" maxSpeed="25" guiShape="bus"/>
		<route id="up" edges="e2 e1" />
        <route id="left" edges="e3 e8 e1" />
        <route id="right" edges="e4 e8 e1" />
        <route id = "down" edges = "e6 e9 e8 e1"/> """, file=routes)
				
		lastVehicle = 0
		vehicle_number = 0
		for i in range(N):
			if random.uniform(0,1) < a:
				print('	<vehicle id = "right_%i" type = "typeWE" route = "right" depart = "%i" />' %(vehicle_number,i),file = routes)
				vehicle_number +=1
				last_vechile = i
			if random.uniform(0,1) < b:
				print('	<vehicle id = "left_%i" type = "typeWE" route = "left" depart = "%i" />'%(vehicle_number,i),file = routes)
				vehicle_number +=1
				last_vechile = i
			if random.uniform(0, 1) < c:
				print('	<vehicle id="down_%i" type="typeNS" route="down" depart="%i" color="1,0,0" />' %(vehicle_number, i),file=routes)
				vehicle_number +=1
				last_vechile = i
			if random.uniform(0, 1) < d:
				print('	<vehicle id="up_%i" type="typeNS" route="up" depart="%i" color="1,0,0" />' %(vehicle_number, i),file=routes)
				vehicle_number +=1
				last_vechile = i
		print("</routes>", file=routes)
		

def run():
	flag = 0
	step = 0
	'''
	Alag se joda h
	'''
	M = []
	Q = []
	V = []
	for agent in agents:
		M.append({})
		Q.append({})
		V.append({})
	for agent in agents:
		for neighbour in agents[agent]:
			temp = {}
			temp2 = {}
			temp3 = {}
			for state in range(4):
				temp2[state] = 1
				temp[state] = [1/len(agents[agent]) for action in range(2)]
				temp3[state] = 1
			M[int(agent)][neighbour] = temp
			Q[int(agent)][neighbour] = temp2
			V[int(agent)][neighbour] = temp3
	'''	
	for agent in agents:
		state[agent] = 1
		action[agent] = 1
		for neighbour in agents[agent]:
			for state in range(4):
				for action in range(2):
				#action[neighbour] = 1
					M[agent][neighbour][state].append(1/len(agents[agent]))     ###  probability that neighbour takes action j is given by 1/(total number of actions neighbour can take ( which is the total number of partial states of the neighbour (what i think now)))
					Q[agent][neighour][state].append(0)                  ###  Consedering starting Q zero for each agent neighbour.	
	'''
	#traci.trafficlights.setPhase("5",1)
	while traci.simulation.getMinExpectedNumber() > 0:
		
		traci.simulationStep()
		for i in agents:


			if traci.trafficlights.getPhase(i) == 1 :
			    traci.trafficlights.setPhase(i,2)
			elif traci.trafficlights.getPhase(i) == 2:
			    traci.trafficlights.setPhase(i,3)
			elif traci.trafficlights.getPhase(i) == 3:
			    traci.trafficlights.setPhase(i,4)
			    flag = 0

			if traci.trafficlights.getPhase(i) == 5:
			    traci.trafficlights.setPhase(i,6)
			elif traci.trafficlights.getPhase(i) == 6:
			    traci.trafficlights.setPhase(i,7)
			elif traci.trafficlights.getPhase(i) == 7:
			    traci.trafficlights.setPhase(i,0)
			    flag = 0

			#current_state = str(2)
			maximum = -999
			best_action = 0
			agent = int(i)
			for neighbour in agents[i]:
				for state in range(4):
					for action in range(2):
						M[agent][neighbour][state][action] = V[agent][neighbour][state]/sum(V[int(agent)][neighbour].values())        ## (Count of visit to action a when both in state i and j)/ (sum of count of visit to all actions when in state i and j)

				
				br = max([[M[agent][neighbour][str(traci.trafficlights.getPhase(i))][neighbour_action]*Q[agent][neighbour][str(traci.trafficlights.getPhase(i))][agent_action][neighbour_action] for neighbour_action in range(2)] for agent_action in range(2)])  # find max of all the actions that agent can take. (We take each action of agent and find the sum of all Q*M for all actions that neighour can take and then find the max among all the sums)



				for state in range(4):
					for agent_action in range(2):
						for neighbour_action in range(2):
							Q[agent][neighbour][state][neighbour_action][agent_action] = (1-alpha)*Q[agent][neighour][state][neighbour_action][agent_action] + alpha*(reward + gamma*br)



				for state in range(4):
					for agent_action in range(2):
						for neighbour_action in range(2):
							value = M[agent][neighbour][current_state][neighbour_action]*Q[agent][neighour][state][neighbour_action][agent_action]   
							if value > maximum:
								maximum = value
								best_action = agent_action
			print('shubham')
			print('----------------------')
			action_agent[i] = agent_action
			traci.trafficlights.setPhase(5,best_action)

        step += 1
	traci.close()
	sys.stdout.flush()
						#print(traci.trafficlights.getPhase("5"))
	traci.close()
	sys.stdout.flush()

def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options

'''
agents has format :- [{'a':[neighbours of a]},{'b':[neighbours of b]}]
'''

def parse_edges():
	edge_ids = []
	for route in sumolib.output.parse_fast("myRoutes.rou.xml", 'route', ['edges']):
		edge_ids.append(route.edges.split())
	return edge_ids



'''
algorithm function is not upto the mark. So, see algorithm3 function
'''
'''
def algorithm():
	for agent in agents:
		state[agent] = 1
		action[agent] = 1
		for neighbour in neighbour[agent]:
			#action[neighbour] = 1
			M[agent][neighbour] = 1/len(A[neighbour])      ###  probability that neighbour takes action j is given by 1/(total number of actions neighbour can take ( which is the total number of partial states of the neighbour (what i think now)))
			Q[agent][neighour] = 0                  ###  Consedering starting Q zero for each agent neighbour.


	for step in timestep:
		for agent in agents:
			for neighbour in neighbours:
				M[agent][neighbour][action] = V[agent][neighbour][action]/sum([V[agent][neighbour][a] for a in actions])   ## (Count of visit to action a when both in state i and j)/ (sum of count of visit to all actions when in state i and j)

				br = max([sum([M[agent][neighbour][action]*Q[agent][neighbour][action] for a in actions[neighbour]]) for a in actions[agent]])  # find max of all the actions that agent can take. (We take each action of agent and find the sum of all Q*M for all actions that neighour can take and then find the max among all the sums)

				Q[agent][neighbour] = (1-alpha)*Q[agent][neighbour] + alpha*(r + gamma*br)

				actions[agent] = argmax([sum([Q[agent][n][a]*M[agent][n][a] for a in actions[n]]) for n in neighbours])

'''

if __name__ == "__main__":
    options = get_options()

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')
    
    # first, generate the route file for this simulation
    generate_routefile()

    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    traci.start([sumoBinary, "-c", "roadConfiguration.sumo.cfg",
                             "--tripinfo-output", "tripinfo.xml"])
    run()
