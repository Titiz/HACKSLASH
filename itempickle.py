import pickle
from items import *

a = [Sword(50, 100, 20, 50), Gun(50, 1, 100, 20, 100)]

pickle.dump( a, open( "save.p", "wb" ) )