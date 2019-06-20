import aergen.core.direction as ds
import aergen.core.path      as ph

# Classes
ED = ds.EntityDirection; EP = ph.EntityPath
EI = ph.EntityDirectionItemPath
# Enum
N = ED.NORTH; S = ED.SOUTH
E = ED.EAST;  W = ED.WEST
J = ED.JUMP;  ST = ED.STATIC
# Fonctions
CC = EP.create_path_consecutive
CA = EP.create_path_absolute_rdm
CE = EP.create_path_equitable_rdm
