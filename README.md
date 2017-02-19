# Multiagent_traffic_light_sytem
This file shows the method of making a traffic simulation

1. First create file roadNodes.nod.xml
Work :- This file create the nodes needed for making roads. We can define a node to be traffic node.

2. Second Create file roadEdge.edg.xml
Work :- This file uses the node id defined in the 1. to join the nodes and make road. We can define roadtypes in this file like 2 lane etc.


3. Now run command netconvert --node-files=roadNodes.nod.xml --edge-files=roadEdge.edg.xml --output-file=roads.net.xml
This helped in making roads.net.xml file.
or
Make netc.cfg file and run below command
netconvert –c roadsConnection.netc.cfg

4. Now create roadConnection.sumo.cfg file
This file contains the input fils such as .nod.xml and link them to other files helping to generate gui

Run sumo-gui -c roadConnection.sumo.cfg
This creates gui

4. Create python file that generates route of the cars.
