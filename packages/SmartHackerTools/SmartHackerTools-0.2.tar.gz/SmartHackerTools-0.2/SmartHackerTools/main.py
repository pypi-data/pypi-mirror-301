import time
import sys

class Main:
    def __init__(self):
        pass
    def type_writer(self,text, delay=0.08, after=""):
        """
        Simulates typing on the console by printing the given text character by
        character with a delay in between. The delay can be specified with the
        delay argument. The default delay is 0.08 seconds.

        Parameters:
            text (str): The text to be typed
            delay (float): The time in seconds to wait after each character
            after (str): The text to print after the text has been typed
        """
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print(after)

def version():
    """
    Returns the current version of the SmartHackerTools.
    
    Returns:
        str: The version of the SmartHackerTools
    """
    return "v_001"

