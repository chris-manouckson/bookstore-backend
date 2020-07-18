from functools import wraps

from flask_restful import reqparse

request_parser = reqparse.RequestParser()

request_parser.add_argument('order', type=str, location='args', action='append')

def parse_order_query(request_handler_function):

  @wraps(request_handler_function)
  def wrapped_parse_order_query(*args, **kwargs):
    request_args = request_parser.parse_args()

    if 'order' in request_args and request_args['order'] and len(request_args['order']) >= 1:
      order = request_args['order']

      if len(order) < 2:
        order.append('asc')

      kwargs['order'] = tuple(order)
    
    return request_handler_function(*args, **kwargs)

  return wrapped_parse_order_query
