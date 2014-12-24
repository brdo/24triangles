24triangles
===========

Script to find puzzle solutions for the 24 Triangles puzzle described here
http://mypuzzlecollection.blogspot.com/2012/07/24-triangles.html

# define the triangles
orient the cube with triangles facing to the left, front, and down.
then read the triangle on front face using this
  A = |\  bottom left
  B = |/  top left
  C = \|  top right
  D = /|  bottom right

# define the 8 unique cubes
    there are 8 cubes because each cube does not have repeated triangles
    4 * 3 * 2 / 3 = 8 ( divide by 3 to remove cyclically redundant cubes )
a = [A,B,C]
b = [A,C,B]
c = [B,C,D]
d = [B,D,C]
e = [C,D,A]
f = [C,A,D]
g = [D,A,B]
h = [D,B,A]

# define the default puzzle layout
  top       bottom
  a b       e f
  d c       h g

# triangle combinations
only A/C, C/A, B/B, D/D triangles can fit together
mathematically this can be expressed using the complex plane
      (0,i)
        A

   B         C
(-1,0)     (0,1)
        D
      (0,-i)
notice that only A dot C = C dot A = B dot B = D dot D = 1
and any other combination does not equal one
