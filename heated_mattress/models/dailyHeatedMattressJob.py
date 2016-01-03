from .heatedMattress import HeatedMattress
from sqlalchemy import Column, Integer, Boolean
from heated_mattress.database import Base, db_session
import datetime


class DailyHeatedMattressJob(HeatedMattress):
    def __init__(self):
        self.run_minute = None

    def __repr__(self):
        return "<DailyHeatedMattressJob(run_minute='%s', left_foot_power='%s', left_middle_power='%s')>" % (
            self.run_minute, self.left_foot_power, self.left_middle_power)

    @property
    def minute(self):
        if self.run_minute is None:
            return -1
        else:
            return self.run_minute % 60

    @property
    def hour(self):
        if self.run_minute is None:
            return -1
        else:
            return int(self.run_minute / 60)



class DailyHeatedMattressJobDAO(DailyHeatedMattressJob, Base):
    __tablename__ = 'daily_heated_mattress_jobs'

    id = Column(Integer, primary_key=True)
    run_minute = Column(Integer, unique=True)
    left_foot_power = Column(Integer)
    left_middle_power = Column(Integer)
    left_head_power = Column(Integer)
    right_foot_power = Column(Integer)
    right_middle_power = Column(Integer)
    right_head_power = Column(Integer)
    _power_on = Column(Boolean, default=True)

    def __init__(self, left_foot_power, left_middle_power, left_head_power, right_foot_power,
                 right_middle_power, right_head_power, power_on):
        self.left_foot_power = left_foot_power
        self.left_middle_power = left_middle_power
        self.left_head_power = left_head_power
        self.right_foot_power = right_foot_power
        self.right_middle_power = right_middle_power
        self.right_head_power = right_head_power
        self._power_on = power_on

    def persist_job(self, hour, minute):
        print('persist job')
        query_minute = (hour * 60) + minute
        self.run_minute = query_minute
        DailyHeatedMattressJobDAO.delete_job(query_minute)
        db_session.add(self)
        print(db_session.query(DailyHeatedMattressJobDAO).count())
        print(db_session.query(DailyHeatedMattressJobDAO).all())
        for item in db_session.query(DailyHeatedMattressJobDAO).all():
            print(item)

    @staticmethod
    def list_jobs():
        return db_session.query(DailyHeatedMattressJobDAO).order_by("run_minute").all()

    @staticmethod
    def delete_job(query_minute):
        existing_job = DailyHeatedMattressJobDAO.get_job(query_minute)
        if existing_job is not None:
            db_session.delete(existing_job)
            db_session.flush()

    @staticmethod
    def get_job(query_minute):
        return db_session.query(DailyHeatedMattressJobDAO).filter_by(
                run_minute=query_minute).first()

    @staticmethod
    def execute_current_job():
        now = datetime.datetime.now()
        current_min = now.minute + (now.hour * 60)
        current_job = DailyHeatedMattressJobDAO.get_job(current_min)
        if current_job is not None:
            current_job.send_command()
