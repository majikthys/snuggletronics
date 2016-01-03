from heated_mattress import app
from heated_mattress.database import db_session
from heated_mattress.database import init_db

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

init_db()
app.run(debug=True, host='0.0.0.0')


