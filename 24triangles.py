#!/usr/bin/python

import re
import sys
import itertools
import collections
from optparse import OptionParser

# define the triangles
# orient the cube with triangles facing to the left, front, and down.
# then read the triangle on front face using this
#   A = |\  bottom left
#   B = |/  top left
#   C = \|  top right
#   D = /|  bottom right

# only A/C, C/A, B/B, D/D triangles can fit together
# mathematically this can be expressed using the complex plane
#       (0,i)
#         A
#
#    B         C
# (-1,0)     (0,1)
#         D
#       (0,-i)
# notice that only A dot C = C dot A = B dot B = D dot D = 1
# and any other combination does not equal one

A = 1j
B = 1
C = -1j
D = -1

# define the look ups and reverse lookups for displaying the puzzle
L = dict(A=A,B=B,C=C,D=D)
R = dict( (j,i) for (i,j) in L.items() )

# define the 8 unique cubes
#   there are 8 cubes because each cube doesn't have repeated triangles
#   4 * 3 * 2 / 3 = 8 ( divide by 3 to remove cyclically redundant cubes )
a = [A,B,C]
b = [A,C,B]
c = [B,C,D]
d = [B,D,C]
e = [C,D,A]
f = [C,A,D]
g = [D,A,B]
h = [D,B,A]

# define the home state of the cube
# top       # bottom
# a b       e f
# d c       g h
puzzle = [a,b,c,d,e,f,g,h]

def solution_string( x ):
    """print the solution as a string of 24 triangle letters"""
    return ''.join([R[k] for j in x for k in j])

def is_solution( x ):
    """is the puzzle vector a solution"""

    return ( x[0][0] * x[1][1] == 1 and
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
             x[3][2] * x[7][2] == 1 )

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
        x[0][2], x[0][0], x[1][1], x[1][2],           x[4][1], x[5][0],
        x[0][1],                   x[1][0],  x[4][0], x[4][2], x[5][2], x[5][1],
        x[3][0],                   x[2][1],  x[7][1], x[7][2], x[6][2], x[6][0],
        x[3][2], x[3][1], x[2][0], x[2][2],           x[7][0], x[6][1]
    )

def cycle( x, pos = 0, rel = 0 ):
    """
    This function will cyclically permute each array element
    within the puzzle vector and exhaust every combination
    Example:
        [ AB, CD ] -> [ AB, CD ], [ AB, DC ], [ BA, CD ], [ BA, DC ]
    """
    if pos == len( x ):
        # return the next puzzle vector variant
        yield x

    for i, j in enumerate(x):

        # don't repeat permutations of the same elements
        if i < rel: continue

        jdeque = collections.deque(j)
        for q in range(len(j)):

            # cyclically permute
            jdeque.rotate()

            # replace element with its cycled variant
            x[i] = list( jdeque )

            # control the depth of the recursion
            # to the length of the puzzle vector
            if pos < len( x ):
                # when using recursion within a generator
                # its necessary to iterate over the function
                for d in cycle( x, pos + 1, i + 1 ):
                    yield d

def orientation( j ):
    """return the cycle number and original cube order"""
    jdeque = collections.deque(j)
    for q in range(len(j)):
        
        # cyclically permute
        jdeque.rotate()

        k = list( jdeque )
        if k in puzzle:
            return (q+1) % len(j), k

def find_solutions( ):
    """find all solutions"""
    n = 0
    for p, x in enumerate( itertools.permutations( puzzle ) ):
        x = list(x)
        for c, s in enumerate( cycle( x ) ):
            if is_solution( s ):
                n += 1

                positions = []
                for j in s:
                    o = orientation( j )
                    positions.append( ( puzzle.index( o[1] ), o[0] ) )

                print 'Solution number = %d, permutation = %d, cycle = %d' %( n, p, c )
                print 'Positions = %s' % positions

                graph_solution( s )
    print n

################################################################################
# main
################################################################################

if __name__ == '__main__':

    parser = OptionParser()

    parser.add_option("-r", "--run", dest="run", action = "store_true",
                      help="search for solutions" )

    parser.add_option("-g", "--graph", dest="graph",
                      help="graph a solution in the form of DBCBDCDBABDABCACBADACADC" )

    options, args = parser.parse_args()

    if options.run:
        find_solutions()

    elif options.graph:
        graph_solution( options.graph )

    else:
        parser.print_help()

