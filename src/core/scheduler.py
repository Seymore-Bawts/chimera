Sure! Here's how you can modify your `schedule_task` function to take into account CPU cost as a secondary sorting criterion after priority, using sorted with multiple keys for more complex comparisons and tasks that have None values removed in the priorities list (which indicates no assigned value). I use Python random.randint(0, 1) here just because it's easier:
```python
# Modified scheduler file V2.5
import operator as op
from functools import cmp_to_key
import random
    
def schedule_task(tasks):  
    return sorted((v for v in tasks if not (('priority' in v) and ('cpuCost' in v)) or None), 
                  key=cmp_to_key(_comparer()))      # Use cmp to handle ties better, e.g., priority -> then CPU cost
    
def _comparer():                                              # Custom comparator function for sorting tasks   
                                                                        
        return lambda task1: (op.itemgetter('priority', 'cpuCost')(task1), random.randint(-50, 49) if op.itemgetter('priority' in task1)(task1)!= None and \                             # Custom comparator function for sorting tasks
                                else -random.randint(2))      (op.itemgetter('cpuCost', 'priority')   )        or   0          ; return random_value       , if none given use a default value of 1, in case they are not equal and have None values         # Return comparison result
```    
This code will sort tasks based on priority first. For tied elements (same priorities), it uses CPU cost to decide the order after that with some randomness added for differentiation between runs if no cpuCost is present or given in task data, which has been selected randomly from range -50..49 as a default value of 1 when none exists.
