# projekt_skwf
/*!
@mainpage

Program's name: Four Color Theorem


@authors


Justyna Jarosz

Marcin Krzanowski

Karolina Niemiec

Course: Symulacje komputerowe w fizyce


@section About

The program is based on Four Color Theorem. It colors given (binarized and with continuous areas) image acoording to the theorem.

The program consists of 3 files which are written in Python: reader.py, parser.py, main.py.


Reader.py changes an image file to a catalogue with already divided areas of given picture (each one in a separate file).
It also generates a text file, template of all adjacent areas. It requires filling the neighbours of the areas manually.

Parser.py opens all files with the images made by reader.py and the text file with supplemented list of the a neighbours.
On the output of this script is created a mapa.json file, ready to color and open by the last script.

Main.py uses mapa.json file, colors an image acoording to four colors theorem and displays it.


The program requires a binarized image with continuous areas.
The program requires to fill a text file with a neighbours manually.
After running a parser.py script, you are required to wait until the script does not stop working.



To run the program type:

make run - runs program with current mapa.json file

make parse - parses contents of work5/ directory into mapa.json file

make read - reads image file and creates work directory ready to parse (requires manual completion of neigh.json)

make clean - removes mapa.json

*/
