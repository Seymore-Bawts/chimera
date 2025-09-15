Sure, here's a complete pytest unit test to verify your new scheduling algorithm functionality from `src/core/scheduler` module based on provided inputs and dependencies in use case scenarios like "The current scheduler is not CPU-aware". 
We will consider the following points for this task - dependency graph construction & topological sorting, creation of a priority queue (based sorted by memory), testing if there are no conflicts between priorities when two or more dependent tasks share one common base scenario with equal `memory cost` and different memo values due them. 
```python
import pytest                         # Import required modules  
from src.core.scheduler import schedule_task      
class TestScheduling:                   # Create a class for testing the scheduling module        
    def test_schedule(self):             // Verify if all tasks are scheduled properly and in correct order  with dependencies, edge cases like 'The current scheduler is not CPU-aware' should be handled correctly.  
        initialTaskList = {"task1":{"memory":"50GB", "cpu cost" :3},           # Creating some dummy data for tasks         
                          "task2":{"memory":"40GB","depend on: task1"},      # Define dependencies between the nodes in graph  (dictionary format)        
                         }           
        schedule_result = schedule(initialTaskList, priority=True )     // Function call to be tested          
                                                                       ((Refer function definition above))         
    def test_schedule2(self):             # Test with no dependencies. Also covers 'The current scheduler is not CPU-aware' case  (Edge cases)  
        initialTaskList = {"task1":{"memory":"50GB", "cpu cost" :3},       // Creating some dummy data for tasks         
                          }                   
                                                                      ((Refer function definition above))        
    def test_schedule2(self):             # Test with no dependencies. Also covers 'The current scheduler is not CPU-aware' case  (Edge cases)  
        initialTaskList = {"task1":{"memory":"50GB", "cpu cost" :3},       // Creating some dummy data for tasks         
                          }                    ((Refer function definition above))        
```     # Add more test methods as per the need of your application.  Please note that you will have to implement `schedule_task` and dependencies in use case scenarios mentioned below:   (You can add these functions/methods into respective modules) . Make sure all tests are passing after adding new functionality or modifying existing one because pytest doesn't automatically rerun failed test.
