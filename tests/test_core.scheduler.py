import pytest
from src.core.scheduler import schedule_task

def test_cpu_aware_scheduling():
    tasks = [
        {'name': 'C', 'priority': 1, 'cpu_cost': 100},
        {'name': 'A', 'priority': 1, 'cpu_cost': 50},
        {'name': 'B', 'priority': 2, 'cpu_cost': 20},
    ]
    # Expected: A (p1, c50), then C (p1, c100), then B (p2, c20)
    expected_order = ['A', 'C', 'B']
    actual_order = [t['name'] for t in schedule_task(tasks)]
    assert actual_order == expected_order, 'Should sort by priority first, then CPU cost'
