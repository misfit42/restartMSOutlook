#! python3
import logging
import pathlib
import psutil
import subprocess
import time

logging.basicConfig(filename='processRestart.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# to disable logging uncomment next line
# logging.disable(logging.CRITICAL)


def process_mon_restart(proc: str, chk_time: int = 300, startup_time: int = 30):
    """
    This function monitors a running process and if it stops for some reason, restarts it again.
    This actions are logged in processRestart.log in same directory.#TODO make file path a input parameter for function
    :proc: process name to keep running
    :chk_time: time in seconds to wait until next check
    :startup_time: time in seconds to wait after process startup until next check is performed
    #TODO return error
    :return: Error if entered process is not running on start of process_mon_restart
    """

    logging.info('Start')

    # run 4-ever
    while True:
        # check if process running, use casefold to compensate for mixed case executable names.
        # Save as list to preserve info for later useage.
        proc_info = [ p.info for p in psutil.process_iter(attrs=[ 'name', 'exe' ]) if
                      proc.casefold() in p.info[ 'name' ].casefold() ]
        logging.info(f'Content of procInfo:  {proc_info}; '
                     f'this should contain the entered executable')
        while (proc_info[ 0 ][ "name" ] in (p.name() for p in psutil.process_iter())):
            time.sleep(chk_time)
        # example: proc_info[0]
        # {'exe': 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe', 'name': 'chrome.exe'}
        # proc_info[0]['exe']
        # 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'

        logging.info(f'{proc_info[ 0 ][ "exe" ]} will try to be restarted')
        # uses pathlib.Path which makes it OS independent object.
        # pass it to str() to pass the string of the path and not the pathlib.Path object.
        subprocess.run(str(pathlib.Path(proc_info[ 0 ][ 'exe' ])))
        logging.info(f'{proc_info[ 0 ][ "name" ]} has been restarted successfully')
        # give process time to start up
        time.sleep(startup_time)


if __name__ == '__main__':
    process = str(input('Please enter process to monitor and automatic restart:'))
    process_mon_restart(process)
