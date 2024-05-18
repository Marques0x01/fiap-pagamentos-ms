import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir.replace('tests\\automated\\steps', 'src'))
sys.path.append(src_dir)
sys.path.append(src_dir.replace('\\src', ''))
