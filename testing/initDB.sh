
# Run this once to initialize database files 
flask db init
flask db migrate -m "Creating tables"
flask db upgrade


