import sys
import os

executable_dir = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(os.path.abspath(__file__))
css_file_path = os.path.join(executable_dir, 'styling.css')

print(css_file_path)