# Scripts for map statement management:
# close_demands.py  
# has_close_demands.py  
# similar_list.py  
# similar_map.py

import os
import sys

if os.path.dirname(__file__) not in sys.path:
    sys.path.append(os.path.dirname(__file__))

import close_demands

coords = close_demands.get_coords(vars())
if coords:
    result = any(close_demands.get_close_demands(form_objects.formdef, coords))
else:
    result = False
