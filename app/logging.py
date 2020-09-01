# Automatic testing log generation

# Import modules
import fnmatch
import logging
import os

## Log directory
logdir = 'testing/logs'

# Config file path
configfp = 'testing/config_name.txt'

# Start logging
def start_logging():
    
    # Check if config file exists,
    # and give appropriate message if it doesn't
    configfile = None
    try:
        # Open for reading
        configfile = open(configfp, "r")
    except IOError:
        # Notify
        message = "\nLogging did not occur! "
        message += "\nPlease create '"
        message += configfp + "' and add your name. "
        message += "\nThis will be used to create "
        message += "the folder which will store your logs."
        print(message)
        # Quit
        quit()
    
    # Get developer name from config file 
    name = configfile.read().replace('\n', '')
    
    # Create user log directory 
    userlogdir = logdir + '/' + name
    
    # If user log directory does not exist
    if not (os.path.isdir(userlogdir)):
        # Create it
        os.makedirs(userlogdir)
    
    # Look for an empty log 
    # (to log into instead of making new log file)
    emptylog = None
    for fpath in os.scandir(userlogdir):
        if (fpath.is_file()):
            if(os.path.getsize(fpath) == 0):
                emptylog = str(fpath)
            
    # New log path
    newlog = None

    # If no empty log was found
    if emptylog is None:
        # > Generate new log file name
        
        # >>> Get number of log files in folder
        num = len(fnmatch.filter(os.listdir(userlogdir), '*.log'))
        
        # >>> Use to generate name of log file
        newlog = userlogdir + '/test' + str(num) + '.log'
    else:
        # > Else if an empty log was found
        
        # >>> Refine empty log path
        emptylog = emptylog.replace("<DirEntry '", "")
        emptylog = emptylog.replace("'>", "")
        emptylog = emptylog.strip()
        
        # >>> Put new log into existing empty log
        newlog = userlogdir + '/' + emptylog

    # Log into new log file path
    logging.basicConfig(filename=newlog, level=logging.INFO)

    


