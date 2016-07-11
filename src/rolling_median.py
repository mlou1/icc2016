#-------------------------------------------------------------------------------
# Name:         rolling_median.py
# Purpose:      Calculate the median degree of a vertex in a graph and update this each time
#               a new Venmo payment appears. You will be calculating the median degree across
#               a 60-second sliding window.
#
#
# Author:      Muryadi Oey
#
#   The Logic of my code
#   1. Read the JSON file - line by line.
#   2. If it is the first line, when a user pays another user, it will create node, edge, record
#       how many neighbor(s) each node has and degree. The degree then calculate to get the median.
#   3. The degree itself will be used for next line as comparison.
#   4. For the next line, when a user pays another user, it will check whether it falls in 60-second
#       window or not. If it is in 60-second window, again, it will create node, edge, record how
#       many neighbor(s) each node has and new degree by compare with previous degree.
#       Before comparing, the code (the function you can see in <i>def entries</i>) will create a new
#       empty degree list and the comparison between current degree and previous degree by check each
#       number in previous degree against each number in current degree. If found, delete that number
#       in the current degree and that number will be added into new empty degree list and if unable
#       to found means it exists in previous degree but not current degree, it will add into new empty
#       degree and until all number in current degree has been compared, if it exists in current degree,
#       it will add into new empty degree. <b>Remember:</b> it will add numbers from previous degree first
#       before adding numbers from current degree. By doing so, we maintain the order of the degree.
#   5. However, if it is not in 60 second or if it is more than 60 second, it will check all previous lines
#       (records) up to the first sequence time (Not first line in the file; Each time the code create new
#       degree list, it will reset the first sequence time aka starting point). By that, we make sure that
#       no previous lines we miss in 60-second window. If found, add it into a temporary list. Later the
#       code will use this temporary list to gather information such as created_time, target and actor and
#       again the code will run to gather node, edge, record how many neighbor(s) each node has and create
#       new degree, based on point number 4.
#
#
# Created:     07/07/2016
# Copyright:   (c) MLOU1 2016
# Licence:     <muryadi oey>
#-------------------------------------------------------------------------------

import networkx as nx  #Need to install
import matplotlib.pyplot as plt    # Need to install


from collections import Counter
import json
import datetime
import time
import sys



# ------------------------------------------------------------------------------
# Define Function for Checking Degree
# This function is for checking current line against data that form into previous degree
# ------------------------------------------------------------------------------
def entries(n,degreeA,chk_small,G,data):
    actor = data[n]["actor"]
    target = data[n]["target"]
    ##print data[n]

    graph = [(actor, target)]
    G.add_node(actor)
    G.add_node(target)
    edge = (actor,target)
    G.add_edge(*edge)

    n += 1
    degreeB =[]
    degreeF = []

    if not degreeA:
        for node in G.nodes():
            degreeA.append(len(G.neighbors(node)))

    else:
        for node in G.nodes():
            degreeB.append(len(G.neighbors(node)))

    for i in degreeA:
        if i in degreeB:
            degreeF.append(i)
            degreeB.remove(i)
            chk_small = i

        else:
            if i > chk_small:
                degreeF.append(i)

    for i in degreeB:
        degreeF.append(i)

    degreeA = degreeF
    degreeF = []

    return degreeA
# ------------------------------------------------------------------------------
# End of Define Function for Checking Degree
# ------------------------------------------------------------------------------



# ------------------------------------------------------------------------------
# Define Function for Time Checking
# This function is to make sure that the new line is in 60-second window
# ------------------------------------------------------------------------------
def time_checking(delta_time,n,str_seq,latest_time,data):
    new_list_dict = []
    new_end = n
    first_entry_chk = 0

    if delta_time < 0 and delta_time > -60:         # Change within -60 second to positive
        delta_time = delta_time * -1

    while delta_time >= 0 and new_end > str_seq:
        new_end -= 1

        new_end_time = data[new_end]["created_time"]
        new_end_time_calc = datetime.datetime.strptime(new_end_time, "%Y-%m-%dT%H:%M:%SZ")

        delta_time = latest_time - new_end_time_calc

        delta_time = delta_time.total_seconds()
        if delta_time < 0 and delta_time > -60:         # Change within -60 second to positive
            delta_time = delta_time * -1

        if delta_time < 60 and delta_time > -1:

            if first_entry_chk == 0:                # Add first entry into new list
                new_list_dict.append(n)
                first_entry_chk = 1

            new_list_dict.append(new_end)

        ##print (new_list_dict)

    return new_list_dict

# ------------------------------------------------------------------------------
# End of Define Function for Time Checking
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Define Function for Median
# This funtion to check Median degree and make it as two digit after decimal place
# ------------------------------------------------------------------------------
def median(mylist):

    # It didnt say about the value of degree have to in sort list, however i include this below lines if it needs to be sorted
    sorts = sorted(mylist)
    length = len(sorts)
    if not length % 2:
        return format(((sorts[length / 2] + sorts[length / 2 - 1]) / 2.0),'.2f')
    return format(sorts[length / 2],'.2f')

##    # Unsorted version
##    length = len(mylist)
##    if not length % 2:
##        return format(((mylist[length / 2] + mylist[length / 2 - 1]) / 2.0),'.2f')
##    return format(mylist[length / 2],'.2f')


# ------------------------------------------------------------------------------
# End of Define Function for Median
# ------------------------------------------------------------------------------



# ------------------------------------------------------------------------------
# Define function for Main code
# ------------------------------------------------------------------------------


def main(argv):


    # Read JSON file

    # If would like to run from Python Editor
##    INPUT_FILE = r"C:\Users\kelep_000\Documents\Venmo\venmo-trans.txt"
##    OUTPUT_FILE = r"C:\Users\kelep_000\Documents\Venmo\output.txt"

    # If would like to run from terminal/command prompt
    INPUT_FILE = sys.argv[1] # file containing the venmo transcaction (venmo-trans.txt) in json format
    OUTPUT_FILE   = sys.argv[2] # file that records the median degree per line


    # Read the file
    dataObj = open(INPUT_FILE, 'r')
    data = json.load(dataObj)

    # Write the Output to Output.txt
    out_File = open(OUTPUT_FILE, 'w')

    G = nx.Graph()

    degreeA =[]
    degreeF = []

    n = 0
    chk_small = 0
    rst_start_time_calc = 0
    ii = 0


    for i in data:

        if n == 0:
            try:

                time = data[n]["created_time"]
                str_time = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")

                degreeA = entries(n,degreeA,chk_small,G,data)
                str_seq = n         # Start Sequence Time

            except:
                pass

        else:
            try:

                time = data[n]["created_time"]
                latest_time = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")

                if rst_start_time_calc != 0:            # check if the start time is not start from beginning
                    str_seq_time_calc = rst_start_time_calc

                else:

                    # Use start sequence time and later compare it with latest time
                    str_seq_time = data[str_seq]["created_time"]
                    str_seq_time_calc = datetime.datetime.strptime(str_seq_time, "%Y-%m-%dT%H:%M:%SZ")

                delta_time = latest_time - str_seq_time_calc

                delta_time = delta_time.total_seconds()   # Make it as variable to pass over to def time_checking
                new_list_dict = time_checking(delta_time,n,str_seq,latest_time,data)

                if new_list_dict:   # Check if it is empty if no, proceed
                    degreeA = []
                    G.clear()

                # Create new node
                for ii in new_list_dict:

                    degreeA = entries(ii,degreeA,chk_small,G,data)

                    # Reset the start time
                    rst_start_time = data[ii]["created_time"]

            except:
                pass

        str_seq = ii

        print "Final Degree: " +str(degreeA)

        if degreeA:

            print "Median: " + str(median(degreeA))
            out_File.write( median(degreeA)+'\n')

        n +=1
        print


        # Print out Nodes
        """ You may enable this to view Node names, Edges and number of edges"""
##        print("Nodes of graph: ")
##        print(G.nodes())
##        print("Edges of graph: ")
##        print(G.edges())
##        print (G.number_of_edges())
        """------------------------------------------------------------------"""


        # Start of draw the Graph
        """ You may enable this to view the graph, nodes, edges """
##        nx.draw(G)
##        plt.savefig("simple_path.png") # save as png
##        plt.show() # display
        """------------------------------------------------------------------"""


    out_File.close()

# ------------------------------------------------------------------------------
# End of Define function for Main code
# ------------------------------------------------------------------------------




if __name__ == "__main__":
     sys.exit(main(sys.argv))

