#!/usr/bin/python
import System
    
# a scales lattice vectors
a=1.0
m=1.76718698107e-25   # mass in kg of one atom
    
lattice_type = 'fcc'
temperature = 120
reference = 'Miller, A.P., Brockhouse, B.N.: Can. J. Phys. 49 (1971) 704'

cell=[
  a,a,0,
  a,0,a,
  0,-a,-a
]

atoms=[
  [ "Pd", m ],
]

sites=[
  [ 0*a,0*a,0*a,             0 ],
]

bonds=[
[ 0,0,1.0*a,1.0*a,0.0*a,19.76, 23.194, 0.0, 
                         23.194, 19.76, 0.0, 
                         0.0, 0.0, -2.511 ],
[ 0,0,2.0*a,0.0*a,0.0*a,0.919, 0.0, 0.0, 
                         0.0, 0.416, 0.0, 
                         0.0, 0.0, 0.416 ],
[ 0,0,2.0*a,1.0*a,1.0*a,0.907, 0.912, 0.912, 
                         0.912, 0.134, 0.609, 
                         0.912, 0.609, 0.134 ],
[ 0,0,2.0*a,2.0*a,0.0*a,-1.041, -1.865, 0.0, 
                         -1.865, -1.041, 0.0, 
                         0.0, 0.0, -0.128 ],
[ 0,0,3.0*a,1.0*a,0.0*a,0.086, 0.118, 0.0, 
                         0.118, -0.227, 0.0, 
                         0.0, 0.0, -0.266 ],
[ 0,0,2.0*a,2.0*a,2.0*a,0.219, 0.154, 0.154, 
                      0.154, 0.219, 0.154, 
                      0.154, 0.154, 0.219 ],
[ 0,0,3.0*a,2.0*a,1.0*a,-0.094, -0.066, -0.033, 
                      -0.066, -0.051, -0.022, 
                      -0.033, -0.022, 0.041 ],
[ 0,0,4.0*a,0.0*a,0.0*a,0.528, 0.0, 0.0, 
                      0.0, -0.113, 0.0, 
                      0.0, 0.0, -0.113 ],
]
        
System.write(cell,atoms,sites,bonds,"cubic")
