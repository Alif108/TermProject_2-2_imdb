#!C:\Users\Asus\PycharmProjects\TermProject\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'IMDbPY==2020.9.29','console_scripts','imdbpy'
__requires__ = 'IMDbPY==2020.9.29'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('IMDbPY==2020.9.29', 'console_scripts', 'imdbpy')()
    )
