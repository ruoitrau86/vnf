#!/usr/bin/python

# a scales lattice vectors
a=1.0
m=9.7462664e-26

cell=[
  a,a,0,
  a,0,a,
  0,-a,-a
]

atoms=[
  [ "Ni", m ],
]

sites=[
  [ 0*a,0*a,0*a,             0 ],
]

bonds=[
  [ 0,0, 1*a,1*a,0*a,            17.319, 19.100,  0.000,
                                 19.100, 17.319,  0.000,
                                  0.000,  0.000, -0.436 ],
  [ 0,0, 2*a,0*a,0*a,             1.044,  0.000,  0.000,
                                  0.000, -0.780,  0.000,
                                  0.000,  0.000, -0.780 ],
  [ 0,0, 2*a,1*a,1*a,             0.842,  0.424,  0.424,
                                  0.424,  0.263, -0.109,
                                  0.424, -0.109,  0.263 ],
  [ 0,0, 2*a,2*a,0*a,             0.402,  0.660,  0.000,
                                  0.660,  0.402,  0.000,
                                  0.000,  0.000, -0.185 ],
  [ 0,0, 3*a,1*a,0*a,            -0.085, -0.035,  0.000,
                                 -0.035,  0.007,  0.000,
                                  0.000,  0.000,  0.018 ],
]

#System.write(cell,atoms,sites,bonds,"cubic")
