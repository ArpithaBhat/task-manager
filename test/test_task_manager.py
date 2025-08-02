import unittest
import sys
import os

# Add the parent directory to the path
# check if github ci triggered
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Services.task_manager import TaskManager
from Models.task import Task

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        # Use a test file instead of the main tasks.json
        self.test_filename = "test_tasks.json"
        self.manager = TaskManager(filename=self.test_filename)  # Changed from file_path
        # or simply: self.manager = TaskManager(self.test_filename)
    
    def test_add_task(self):
        task = self.manager.add_task("Test Task")
        self.assertIsNotNone(task)
        self.assertEqual(task.title, "Test Task")
        self.assertFalse(task.completed)
        self.assertEqual(len(self.manager.get_all_tasks()), 1)
    
    def test_get_all_tasks(self):
        self.manager.add_task("Task 1")
        self.manager.add_task("Task 2")
        tasks = self.manager.get_all_tasks()
        self.assertEqual(len(tasks), 2)
    
    def test_delete_task(self):
        task = self.manager.add_task("Task to delete")
        task_id = task.id
        
        # Verify task exists
        self.assertIsNotNone(self.manager.get_task_by_id(task_id))
        
        # Delete task
        result = self.manager.delete_task(task_id)
        self.assertTrue(result)
        
        # Verify task is deleted
        self.assertIsNone(self.manager.get_task_by_id(task_id))
    
    def test_mark_task_completed(self):
        task = self.manager.add_task("Task to complete")
        task_id = task.id
        
        # Mark as completed
        updated_task = self.manager.mark_task_complete(task_id)
        self.assertIsNotNone(updated_task)
        self.assertTrue(updated_task.completed)
    
    def test_get_task_by_id(self):
        task = self.manager.add_task("Find me")
        found_task = self.manager.get_task_by_id(task.id)
        self.assertIsNotNone(found_task)
        self.assertEqual(found_task.title, "Find me")
        
        # Test non-existent task
        not_found = self.manager.get_task_by_id(9999)
        self.assertIsNone(not_found)

    def tearDown(self):
        # Clean up test file
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

if __name__ == '__main__':
    unittest.main()