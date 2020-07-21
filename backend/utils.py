from flask import Request

DEFAULT_ELEMENTS_PER_PAGE = 10

def paginate_result(request: Request, result: list, elements_per_page = DEFAULT_ELEMENTS_PER_PAGE) -> list:
    page = request.args.get(key='page', default=1, type=int)
    start = (page - 1) * elements_per_page
    end = start + elements_per_page
    
    return result[start:end]

def format_questions(unformatted_result: list) -> list:
    return [entry.format() for entry in unformatted_result]

def list_to_keyed_object(input_list: list, key = 'id') -> dict:
    output_object = {}
    for entry in input_list:
        output_object[getattr(entry, key)] = entry
    
    return output_object

def format_categories(category_list: list) -> dict:
    output_object = {}
    keyed_object = list_to_keyed_object(category_list)
    for (key, value) in keyed_object.items():
        output_object[key] = value.type
    return output_object