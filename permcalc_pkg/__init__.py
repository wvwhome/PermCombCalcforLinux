#   __init__.py   
# 
#  03/07/2019  Warren Van Wyck
#  03/04/2019 WVW: Unique names.  use login_f  
#  03/05/2019 WVW: Switch from SQLite to MySQL
#  03/09/2019 WVW: Remove any DB code.  Just log to stdout.

from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['WTF_CSRF_ENABLED'] = False       #  This is NOT a high security application.
                                           
from permcalc_pkg import routes
