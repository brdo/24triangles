#!/usr/bin/python

import re
import itertools
import collections

# define the triangles
#       (0,i)
#         A
#
#    B         C
# (-1,0)     (0,1)
#         D
#       (0,-i)

A = 1j
B = 1
C = -1j
D = -1

# define the look ups
L = dict(A=A,B=B,C=C,D=D)
R = dict( (j,i) for (i,j) in L.items() )

# define the cubes
a = [A,B,C]
b = [A,C,B]
c = [B,C,D]
d = [B,D,C]
e = [C,D,A]
f = [C,A,D]
g = [D,A,B]
h = [D,B,A]

# define the home state of the cube
puzzle = [a,b,c,d,e,f,g,h]

def solution_string( x ):
    """print the solution as a string of 24 triangle letters"""
    return ''.join([R[k] for j in s for k in j])

def is_solution( x ):
    """is the puzzle vector a solution"""

    if ( x[0][0] * x[1][1] == 1 and
         x[1][0] * x[2][1] == 1 and
         x[2][0] * x[3][1] == 1 and
         x[3][0] * x[0][1] == 1 and

         x[4][1] * x[5][0] == 1 and
         x[5][1] * x[6][0] == 1 and
         x[6][1] * x[7][0] == 1 and
         x[7][1] * x[4][0] == 1 and

         x[0][2] * x[4][2] == 1 and
         x[1][2] * x[5][2] == 1 and
         x[2][2] * x[6][2] == 1 and
         x[3][2] * x[7][2] == 1 ):
        return True
    else:
        return False

def graph_solution( x ):
    """
    DBC BDC DBA BDA BCA CBA DAC ADC

      C D  D C    B  B
      B      B  C A  A C

      A      B  A C  C A
      D C  D A    D  D
    """
    if not isinstance( x, str ):
        x = solution_string( x )

    print x
    x = [ i for i in re.split( r'(...)', x ) if i ]

    print """
      {0} {1}   {2} {3}    {4}   {5}
      {6}       {7}  {8} {9}   {10} {11}

      {12}       {13}  {14} {15}   {16} {17}
      {18} {19}   {20} {21}    {22}   {23}
    """.format(
        x[0][2], x[0][0], x[1][1], x[1][2],           x[4][0], x[5][1],
        x[0][1],                   x[1][0],  x[4][1], x[4][2], x[5][2], x[5][0],
        x[3][0],                   x[2][1],  x[7][0], x[7][2], x[6][2], x[6][1],
        x[3][2], x[3][1], x[2][0], x[2][2],           x[7][1], x[6][0]
    )

def cycle( x, pos = 0, rel = 0 ):

    if pos == len( x ):
        yield x

    for i, j in enumerate(x):
        if i < rel: continue
        jdeque = collections.deque(j)
        for q in range(len(j)):
            jdeque.rotate()
            x[i] = list( jdeque )
            if pos < len( x ):
                for d in cycle( x, pos + 1, i + 1 ):
                    yield d

if __name__ == '__main__':

    import sys

    if '-r' in sys.argv:
        n = 0
        for p, x in enumerate( itertools.permutations( puzzle ) ):
            for s in cycle( list(x) ):
                if is_solution( s ):
                    print p
                    graph_solution( s )
                    n += 1
        print n

    if '-g' in sys.argv:
        graph_solution( sys.argv[sys.argv.index('-g')+1] )

