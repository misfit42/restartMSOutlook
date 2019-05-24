#! python3
import psutil,time,subprocess,logging

logging.basicConfig(filename='processRestart.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# to disable logging uncomment next line
# logging.disable(logging.CRITICAL)
# TODO: rewrite so that this works cross platform and takes process name, time, sleep, debugging as arguments
def process_mon_restart():
    '''
    This function monitors a process and if it stops for some reason, restarts it again.
    currently this function takes no arguments.
    :return: no return value
    '''
    logging.info('Start')
    # run 4-ever
    while True:
        # check if outlook is still running
        while ('OUTLOOK.EXE' in (p.name() for p in psutil.process_iter())):
            # check every 10 minutes if outlook is still running.
            time.sleep(10)
        subprocess.run(r'"C:\Program Files (x86)\Microsoft Office\root\Office16\OUTLOOK.EXE"')
        logging.info('Outlook EXE has been restarted')
        # older way:
        # os.system(r'"C:\Program Files (x86)\Microsoft Office\root\Office16\OUTLOOK.EXE"')
        # give outlook time to start up
        time.sleep(30)


if __name__ == '__main__':
    process_mon_restart()



