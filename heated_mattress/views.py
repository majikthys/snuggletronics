from flask import render_template
from heated_mattress import app
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from heated_mattress.models.heatedMattress import HeatedMattress


api = Api(app)


heated_mattress_fields = {
    'left_foot_power': fields.Integer,
    'left_middle_power': fields.Integer,
    'left_head_power': fields.Integer,
    'right_foot_power': fields.Integer,
    'right_middle_power': fields.Integer,
    'right_head_power': fields.Integer
}

mattress_parser = reqparse.RequestParser()
mattress_parser.add_argument('left_foot_power', type=int, help='0 to 10', required=True, choices=list(range(0, 11)))
mattress_parser.add_argument('left_middle_power', type=int, help='0 to 10', required=True, choices=list(range(0, 11)))
mattress_parser.add_argument('left_head_power', type=int, help='0 to 10', required=True, choices=list(range(0, 11)))
mattress_parser.add_argument('right_foot_power', type=int, help='0 to 10', required=True, choices=list(range(0, 11)))
mattress_parser.add_argument('right_middle_power', type=int, help='0 to 10', required=True, choices=list(range(0, 11)))
mattress_parser.add_argument('right_head_power', type=int, help='0 to 10', required=True, choices=list(range(0, 11)))
mattress_parser.add_argument('power_on', default=True, type=bool, help='True is on false is off, defaults to true')


class HeatedMattressREST(HeatedMattress, Resource):
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

api.add_resource(HeatedMattressREST, '/api/mattress')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
