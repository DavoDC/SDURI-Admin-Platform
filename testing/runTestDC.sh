
# Disable
#echo "Disabled, use 'flask run'"
#exit 1

# Enable debugging (and automatic reloading of HTML)
export FLASK_ENV=development 
export FLASK_DEBUG=1

# Start testing server
cd "C:\Users\David\GitHub Repos\CITS3200 Code\SDURI-Admin-Platform"
flask run

# Go into testing
cd "testing"

# Make sure server is shut down
./forceStop.bat


