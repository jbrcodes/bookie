# app/cli.py

import os

from app import app, db



#
# Create a DB and add a few test records
#

@app.cli.command()
def debug():
    print( 'DEBUG! ' + os.path.dirname(__file__) )

    
@app.cli.command()
def dbcreate():
    db.create_all()
    print('DB created')
    

@app.cli.command()
def dbinit():
    import tests.common
    tests.common.addData()
    print('DB initialized')
