from heated_mattress import app
from heated_mattress.database import db_session
from heated_mattress.database import init_db
from heated_mattress.models.dailyHeatedMattressJob import DailyHeatedMattressJobDAO


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
    DailyHeatedMattressJobDAO.end_poller()

init_db()  # kick off DB, or create if it doesn't exist

DailyHeatedMattressJobDAO.initialize_poller()  # kick off job polling thread

app.run(debug=True, host='0.0.0.0')  # Note: poller will double run if you have reloading enabled (debug=True)


