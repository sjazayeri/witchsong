# witchsong
A Shazam clone written in python
This system only accepts wav files sampled at 44.1KHz as input

INSTALLATION:
You need numpy and scipy installed for this to work:
$ sudo pip install numpy scipy

USAGE:
You can index your music using the index.py program thusly:
$ ./index.py [dbfile] [file1] [file2] ... [fileN]
this will index the files 1 through N and append the result to
[dbfile] (or create it if it doesn't exist)

For identifying a piece of music:
$ ./search.py [dbfile] [input file]