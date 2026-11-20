import subprocess
import sys
import time
from pathlib import Path
from urllib.request import urlopen
import webbrowser

HERE = Path(__file__).resolve().parent
URL = 'http://127.0.0.1:37848/'


def serving():
    try:
        with urlopen(URL,timeout=.7) as page:
            return b'LEVEL TOOL / HTML5' in page.read(16384)
    except OSError:
        return False


def main():
    if not serving():
        log = HERE / 'server.log'
        creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
        with log.open('ab') as output:
            process = subprocess.Popen([sys.executable,str(HERE/'server.py')], cwd=HERE, stdin=subprocess.DEVNULL,
                stdout=output, stderr=output, creationflags=creationflags)
        for _ in range(35):
            if serving(): break
            if process.poll() is not None:
                print(f'Level Tool could not start. See {log}.')
                return 1
            time.sleep(.2)
        else:
            print(f'Level Tool did not respond. See {log}.')
            return 1
    webbrowser.open(URL)
    print(URL)
    return 0


if __name__=='__main__':
    sys.exit(main())
