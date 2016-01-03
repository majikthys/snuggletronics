from flask import render_template
from heated_mattress import app
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from heated_mattress.models.heatedMattress import HeatedMattress
from heated_mattress.models.dailyHeatedMattressJob import DailyHeatedMattressJobDAO, DailyHeatedMattressJob

api = Api(app)

api_version_path = "/api/v1/"

heated_mattress_fields = {
    'left_foot_power': fields.Integer,
    'left_middle_power': fields.Integer,
    'left_head_power': fields.Integer,
    'right_foot_power': fields.Integer,
    'right_middle_power': fields.Integer,
    'right_head_power': fields.Integer
}

daily_job_fields = {
    'hour': fields.Integer,
    'minute': fields.Integer
}

power_on_field = {'power_on': fields.Boolean}

heated_mattress_daily_runnable_fields = heated_mattress_fields.copy()
heated_mattress_daily_runnable_fields.update(daily_job_fields)
heated_mattress_daily_runnable_fields.update(power_on_field)



mattress_parser = reqparse.RequestParser()
mattress_parser.add_argument('left_foot_power', type=int, help='0 to 10', required=True, choices=list(range(0, 11)))
mattress_parser.add_argument('left_middle_power', type=int, help='0 to 10', required=True, choices=list(range(0, 11)))
mattress_parser.add_argument('left_head_power', type=int, help='0 to 10', required=True, choices=list(range(0, 11)))
mattress_parser.add_argument('right_foot_power', type=int, help='0 to 10', required=True, choices=list(range(0, 11)))
mattress_parser.add_argument('right_middle_power', type=int, help='0 to 10', required=True, choices=list(range(0, 11)))
mattress_parser.add_argument('right_head_power', type=int, help='0 to 10', required=True, choices=list(range(0, 11)))
mattress_parser.add_argument('power_on', default=True, type=bool, help='true is on false is off, defaults to true')

mattress_parser_daily_runnable_parser = mattress_parser.copy()
mattress_parser_daily_runnable_parser.add_argument('hour', type=int, help='0 to 24', required=True,
                                                   choices=list(range(0, 25)))
mattress_parser_daily_runnable_parser.add_argument('minute', type=int, help='0 to 59', required=True,
                                                   choices=list(range(0, 60)))

daily_jobs_parser = reqparse.RequestParser()
daily_jobs_parser.add_argument('hour', type=int, help='0 to 24', required=True, choices=list(range(0, 25)))
daily_jobs_parser.add_argument('minute', type=int, help='0 to 60', required=True, choices=list(range(0, 61)))


class DailyHeatedMattressJobsREST(DailyHeatedMattressJob, Resource):
    @marshal_with(heated_mattress_daily_runnable_fields)
    def get(self):
        return DailyHeatedMattressJobDAO.list_jobs()

    def delete(self):
        args = daily_jobs_parser.parse_args()
        DailyHeatedMattressJobDAO.delete_job((args['hour'] * 60) + args['minute'])
        return '', 204

    def post(self):
        print('this is post')
        args = mattress_parser_daily_runnable_parser.parse_args()
        dao = DailyHeatedMattressJobDAO(
                args['left_foot_power'],
                args['left_middle_power'],
                args['left_head_power'],
                args['right_foot_power'],
                args['right_middle_power'],
                args['right_head_power'],
                args['power_on']
        )
        dao.persist_job(args['hour'], args['minute'])
        return '', 200


class HeatedMattressREST(HeatedMattress, Resource):
    # singleton REST instance (we don't force base object to be a singleton)
    __instance = None

    def __init__(self):
        if not HeatedMattressREST.__instance:
            HeatedMattressREST.__instance = HeatedMattress()

    def __getattr__(self, name):
        return getattr(self.__instance, name)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)

    @marshal_with(heated_mattress_fields)
    def get(self):
        return self

    @marshal_with(heated_mattress_fields)
    def put(self):
        args = mattress_parser.parse_args()
        if not args['power_on']:
            self.power_off()
            return self
        self.left_foot_power = args['left_foot_power'];
        self.left_middle_power = args['left_middle_power'];
        self.left_head_power = args['left_head_power'];
        self.right_foot_power = args['right_foot_power'];
        self.right_middle_power = args['right_middle_power'];
        self.right_head_power = args['right_head_power'];
        self.set_power()
        return self


@app.route('/', methods=['GET'])
def get_index():
    return render_template('index.html', mattress=HeatedMattressREST(), headers={'Content-Type': 'application/json'})


api.add_resource(HeatedMattressREST, api_version_path + 'mattress')


api.add_resource(DailyHeatedMattressJobsREST, api_version_path + 'mattress/jobs')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
