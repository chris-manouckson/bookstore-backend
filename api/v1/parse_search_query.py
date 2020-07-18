from functools import wraps

from flask_restful import reqparse

request_parser = reqparse.RequestParser()

request_parser.add_argument('search', type=str, location='args')

def parse_search_query(request_handler_function):

  @wraps(request_handler_function)
  def wrapped_parse_search_query(*args, **kwargs):
    request_args = request_parser.parse_args()

    if 'search' in request_args and request_args['search']:
      search = request_args['search']

      kwargs['search'] = search
    
    return request_handler_function(*args, **kwargs)

  return wrapped_parse_search_query
