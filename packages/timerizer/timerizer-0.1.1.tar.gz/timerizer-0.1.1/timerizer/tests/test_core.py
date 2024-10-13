import time
from timerizer.core import timer

@timer
def dummy_func(x):
    time.sleep(x)  
    return x * 2

def test_timer_decorator(capsys):
    """
    Test to check if the timer decorator prints the correct runtime.
    """
    result = dummy_func(1)  
    
    # Capture the printed output
    captured = capsys.readouterr()
    
    # Check if the correct result is returned
    assert result == 2
    
    # Check if the function name and execution time are printed correctly
    assert "Function 'dummy_func' executed in" in captured.out


import unittest
from io import StringIO
import sys

@timer
def dummy_func(x):
    time.sleep(x)
    return x * 2

class TestTimerDecorator(unittest.TestCase):
    
    def test_timer_decorator(self):
        """
        Test if the timer decorator works as expected.
        """
        # Capture the print output using StringIO
        captured_output = StringIO()
        sys.stdout = captured_output
        
        # Call the function and check its return value
        result = dummy_func(1)
        self.assertEqual(result, 2)
        
        # Check if the correct message was printed
        sys.stdout = sys.__stdout__  # Reset stdout
        output = captured_output.getvalue()
        self.assertIn("Function 'dummy_func' executed in", output)

if __name__ == '__main__':
    unittest.main()
