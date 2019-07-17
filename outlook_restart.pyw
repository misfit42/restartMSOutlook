import psutil, time,subprocess,logging, winreg

logging.basicConfig(filename='processRestart.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# to disable logging uncomment next line
# logging.disable(logging.CRITICAL)


def set_outlook_macro_level():
    """
    This function makes sure macro level is set to allow all macros.
    make sure user executing the script has write access to registry key.
    (reg edit got to security right click and check privileges)
    """
    # open Outlook security registry key
    subkey = r'Software\Policies\Microsoft\Office\16.0\outlook\security'
    try:
        reg_key_security = winreg.OpenKey(winreg.HKEY_CURRENT_USER, subkey, 0, winreg.KEY_ALL_ACCESS)

        # retrieve sub key "level" value and type
        subkey_level = winreg.QueryValueEx(reg_key_security, r'level')

        # if value of subkey  is not equal to 1 or 3 update subkey to 3
        # (3 is ok if .vba code is locally signed if not 1 is required.)
        if subkey_level[0] not in [1, 3]:
            winreg.SetValueEx(reg_key_security, r'level',0,winreg.REG_DWORD, 3)
            logging.info(f' Registry: Outlook\security "level" set')
        else:
            logging.info(f' Registry: Outlook\security "level" set is still set correctly')
    except PermissionError:
        logging.info(f'Access denied to windows registry, security level cannot be set')
        #TODO due something senseful in this case
        # like inform somebody per mail that manual intervention is required


def start_outlook():
    '''
    starts outlook and logs return code
    '''
    outlook = r'"C:\Program Files (x86)\Microsoft Office\root\Office16\OUTLOOK.EXE" /restore'
    proc_started = subprocess.run(outlook)
    logging.info(f'Outlook has been restarted: {proc_started.args}, {proc_started.returncode}')
    # TODO if return code (proc_started.returncode) is not 0 or 1 then send mail so somebody for manual checking


def process_mon_restart():
    '''
    This function monitors Outlook and if it stops for some reason, restarts it again.
    It also makes sure that macro security is set correctly to execute the .vba code in the CSC mailbox,
    currently this function takes no arguments.
    :return: no return value
    '''
    logging.info('Start')
    # run 4-ever
    while True:
        # check if outlook is still running
        while ('OUTLOOK.EXE' in (p.name() for p in psutil.process_iter())):
            # check every 5 minutes if outlook is still running.
            time.sleep(300)
        # make sure macros are allowed
        set_outlook_macro_level()
        #just in case there is a timing issue with registry check/write operation, wait 5 sec.
        time.sleep(5)
        start_outlook()
        #just in case there is a timing issue with restart
        time.sleep(40)


if __name__ == '__main__':
    process_mon_restart()


