from functools import wraps

from flask_restful import reqparse

request_parser = reqparse.RequestParser()

request_parser.add_argument('offset', type=int, location='args')
request_parser.add_argument('limit', type=int, location='args')

def parse_pagination_query(request_handler_function):

  @wraps(request_handler_function)
  def wrapped_parse_pagination_query(*args, **kwargs):
    request_args = request_parser.parse_args()

    offset = 0
    if 'offset' in request_args and request_args['offset'] != None:
      offset = request_args['offset']

    limit = 12
    if 'limit' in request_args and request_args['limit'] != None:
      limit = request_args['limit']

    kwargs['offset'] = offset
    kwargs['limit'] = limit
    
    return request_handler_function(*args, **kwargs)

  return wrapped_parse_pagination_query
