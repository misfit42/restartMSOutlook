#! python3
import logging
import pathlib
import psutil
import subprocess
import time

logging.basicConfig(filename='processRestart.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# to disable logging uncomment next line
# logging.disable(logging.CRITICAL)
# TODO: rewrite so that this works cross platform and takes process name, time, sleep, debugging as arguments
def process_mon_restart(proc: str, chk_time: int = 300, startup_time: int = 30):
    '''
    This function monitors a process and if it stops for some reason, restarts it again.
    :proc: process name to check
    :chk_time: time in seconds to wait until next check
    :startup_time: time in seconds to wait after process startup until next check is performed

    :return: no return value
    '''
    logging.info('Start')
    # run 4-ever
    while True:
        # check if proc running
        proc_info = [p.info for p in psutil.process_iter(attrs=['name', 'exe']) if proc in p.info['name']]
        try:
            while (proc_info[0]["name"] in (p.name() for p in psutil.process_iter())):
                time.sleep(chk_time)
            # example: proc_info[0]
            # {'exe': 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe', 'name': 'chrome.exe'}
            # proc_info[0]['exe']
            # 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
        except IndexError:
            logging.info(f'{proc}: is not running on startup')
            proc = str(input('Process you entered does not exist, please enter a valid process name:'))
            continue
        subprocess.run(pathlib.Path(proc_info[0]['exe'])) # uses pathlib.Path which makes it OS independant
        logging.info(f'{proc_info[0]["name"]} has been restarted')
        # give process time to start up
        time.sleep(startup_time)


if __name__ == '__main__':
    process = str(input('Please enter process to monitor and automatic restart:'))
    process_mon_restart(process)



