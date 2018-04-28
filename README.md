Telephone Network Project
=========================
Python code used for the fourth Mathematics and Data modelling 1 Project.

EMAT10008
---------
https://www.bris.ac.uk/unit-programme-catalogue/UnitDetails.jsa?ayrCode=16%2F17&unitCode=EMAT10008

Project task
------------
"A telephone company has the major hub in a particular town and additional hubs in N other villages. All additional hubs need to be connected with the main hub either directly or through other hubs. Propose at least two methods/algorithms to connect all additional hubs to the major hub and determine the one that minimises the total length of cable. How do the performances of the methods depends on the number and the position of the hubs?"

Project overview
----------------
The python was created to create pictures of networks/graphs. The sun method, Prims and our own 'Quasi-Steiner' algorithm have been implemented. With some funky saving of images we also managed to create some even funkier GIFs

Quasi-Steiner algorithm
-----------------------
Steiner points are 'imaginary' nodes that you create to shorten the distance required to connect other nodes. Our algorithn estimates these steiner points by adding the midpoint from the power set of current nodes that reduces the total length of the network the most while any midpoint is capable of shortening the network.

Contents
--------
 * Makefile
 * README.md
 * network.py
 * list.py
 * graphPlotting directory
 * directories for GIFs

network.py
----------
Uses lots of functions, currently configured to run Prim's algorithm and our own. It also saves images of these as PNGs, taking the nodelist from a csv file.

list.py
-------
Used to create a random list of nodes

Makefile
--------
Only used to produce GIFs
