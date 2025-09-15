Here's a sample pytest unit test that you can use to verify your new task scheduling function `src/core/scheduler.py` by testing its behavior under various scenarios including edge cases and dependencies among tasks using topological sort logic from Khan algorithm, which is used in the provided code snippet for dependency graph construction:
```python
import pytest  # Importing required module  
from src.core import scheduler as sd    # Assuming your source file has a core folder with an init __init__ and scheduled task function (scheduled_task) inside it which is also the python package name, hence 'src' assumed here for convenience    
import random         // Importing required module  
random.seed()        // Seeding to get reproducible results from same seed every time   
from collections import defaultdict  // For dependency Graph and adjacency list construction using Python built in data structures (default dict)     
if __name__ == '__main__':     // To run the test automatically, not when imported as a module.   pytest can't execute tests if they are used like this   
pytest.main(['-q', ‘tests’])       // Running Test with PyTest unit testing framework using command line arguments for executing all files inside 'Tests folder'.     In case of multiple test cases, use -s to show the location where error occurred during execution and pyright or similar tools can be used as well.  
```     
Here're some examples: 1) Tasks with different priorities without dependencies; a scenario you might encounter when setting up your cluster system (2nd priority); tasks that have two dependents in the same task group but they are running concurrently due to low memory resources, etc. These scenarios can be tested using pytest's parametrize decorator or similar approaches provided by PyTest for testing multiple cases with data and fixtures from setup methods of a class (3rd priority). 
You should also consider adding test coverage around the edge case where tasks have dependencies that are not met, e.g., there exists task A which depends on Task B but only after its CPU costs exceed another base scenario's cost or vice versa etc.. pytest has built-in support for this kind of testing (4th priority).
