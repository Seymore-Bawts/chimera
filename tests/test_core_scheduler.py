Here's a sample pytest unit tests that you can use to verify your new functionality in `src/core/scheduler` module, using edge cases as well. 

```python
import operator as op    # Import required modules  
from collections import defaultdict      # For dependency Graph and adjacency list construction    
def schedule_task(tasks):       # Define the scheduling task method considering tasks dictionary has 'priority' & cpu cost keys with values can be None if absent. 
        edges = defaultdict(list)    # Construct an Adjacent List from all possible neighbors to each node in our graph    
        
# Your code here... for sorting the sortedTasks list using priority and CPU costs   ... continue as needed..      
```         
You can test your function with different input types (e.g., a simple task, tasks without dependencies or more complex scenarios) by calling it within pytest's parametrize decorator: 
- Testing the normal operation scenario of `schedule_task` method and its edge cases such as when there are no conflicts among identical priority/CPU cost but different memory costs due to randomness.  
    - Normal Operation Scenario Tests.. continue from here...     
        pytest.mark.parametrize("tasks, expected", [  # parametrized test with normal operation scenarios and their expectations     ... ]), marks=[pytest.mark.depends_on('dep1', 'Depends on task')])    )       continue here...  
- Testing when the function throws an exception due to invalid input (e.g., non dictionary, missing priority or cpu cost keys). You can test it by calling `schedule_task` with wrong parameters and then assert that there was a ValueError in raised exception .  For example:      pytest.mark.parametrize("tasks", [ ... ]), marks=[pytest...])     ) continue here  
- Testing when the function does not throw an error due to incorrect dependencies among tasks and priority (e.g., a task depends on another that has higher or lower CPU cost).  You can test it by calling `schedule_task` with correct parameters but improper dependency structure, then assert there was no ValueError in raised exception .    For example:   pytest... marks=[pytest...) ]), ... continue here)
- Testing when the function does not throw an error due to incorrect dependencies among tasks and memory cost (e.g., a task depends on another that has same CPU or higher but different priority).  You can test it by calling `schedule_task` with correct parameters, then assert there was no ValueError in raised exception .   For example:    pytest... marks=[pytest...] ), ... continue here)
- Testing when the function does not throw an error due to dependencies among tasks. But priorities are different for same CPU cost and memory costs (e.g., a task depends on another that has higher or lower priority).  You can test it by calling `schedule_task` with correct parameters, then assert there was no ValueError in raised exception .   For example:    pytest... marks=[pytest...] ), ... continue here)
```     In each of these sections you'll need to add the normal operation scenarios and their expected outputs. PyTest will run your tests by calling `schedule_task(tasks, priority,... )` for every scenario in a loop until all test cases are completed successfully or failed due an unhandled exception (if any). 
Make sure you have pytest installed on the machine where this script is being executed. If not install it via pip: python -m pip install --user pytest . Then run your tests using `pytest` command in terminal from root directory of project folder, or execute them separately by calling respective test files directly if they are part of same codebase with main file (e.g., src/core/scheduler_tests.py).
