from flask import Request

DEFAULT_ELEMENTS_PER_PAGE = 10

def paginate_result(request: Request, result: list, elements_per_page = DEFAULT_ELEMENTS_PER_PAGE) -> list:
    page = request.args.get(key='page', default=1, type=int)
    start = (page - 1) * elements_per_page
    end = start + elements_per_page
    
    return result[start:end]

def format_result(unformatted_result: list) -> list:
    return [entry.format() for entry in unformatted_result]