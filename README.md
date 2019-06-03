# check_restart_process
check process existence and restarts

This function monitors a running process and if it stops for some reason, restarts it again.
I needed this to restart a outlook process in work which was terminated from remote.
So I decided to generalize it as my first project. Maybe someone has a similar need and can make use of it.
Some actions are logged in processRestart.log in same directory.#TODO make file path a input parameter for function
    :proc: process name to keep running
    :chk_time: time in seconds to wait until next check
    :startup_time: time in seconds to wait after process startup until next check is performed
    #TODO handle error
    Error if entered process is not running on start of process_mon_restart

=> process name, check time and wait after process startup until next check is performed can be provided at startup
=> it should work on windows and linux

Open Topics:
Make logging file path as parameter
What to do if process entered does not exist on startup.

