Here's a pytest unit test to verify your new functionality in `src/core/scheduler` module using mock objects and dependencies from other modules that you haven't included here (i.e., only one method). 
Please note, the actual implementation details of this function would depend on many factors such as how tasks are represented inside a scheduler object or any external services it uses like file I/O for example if your task data is stored in database etc... You need to mock those dependencies and handle cases where they fail. This test will not cover all possible edge-cases but should give you an idea of what tests can be written with pytest:
```python
import sys, os  # needed by the scheduler module for file I/O operations (randomness included)  
sys.path.append(os.path.dirname(__file__))    # add parent dir to path so we could import src in tests    
from unittest.mock import Mock
import pytest  # needed by all test functions below for mocking dependencies, see http://doc.pytest.org/en/latest/how-to/mocking.html  
    from collections import defaultdict         
try:                   // Assume src has been imported and available globally in other modules    
        tasks = {'task1': { 'priority' : 5, }, }               # Simulate task dependencies (depend_on is a mocked function)      
except NameError as e:             print('No module named',e), sys.exit(1);          // This will fail if the above imports were not successful    
try:                  
        schedule = src.core.scheduler                # Assume scheduler has been imported and available globally in other modules   
except NameError as e :            print('No module named',e), sys.exit(1);           // This will fail if the above imports were not successful    
     
def test_task():                 
        tasks = {'t': { 'memory' ∈ [5,6]}}               # Simulate a task with memory between min and max (randomness included)    result  =  schedule.scheduleTask(tasks,'priority')           // Call the scheduler function to test if it works correctly      
        assert tasks == expected_result                     // Assert that your code is correct, update as needed          .catch((e: exception => consolelog("Error in task ", e))      )                      }   catch (exception){}};  endtry    pass     # Test passes and no exceptions were thrown. Update this message if necessary
```      `test_task() `should return a string, the expected result should be compared with returned value from schedule function to see it matches or not as per requirement of unit test framework chosen (pytest in above snippet).  Also add more tests for other edge cases such error handling and randomness included.
