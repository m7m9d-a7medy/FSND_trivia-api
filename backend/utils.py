from flask import Request

DEFAULT_ELEMENTS_PER_PAGE = 10


def paginate_result(
    request: Request,
    result: list,
    elements_per_page=DEFAULT_ELEMENTS_PER_PAGE
) -> list:
    page = request.args.get(key='page', default=1, type=int)
    start = (page - 1) * elements_per_page
    end = start + elements_per_page

    return result[start:end]


def format_questions(unformatted_result: list) -> list:
    return [entry.format() for entry in unformatted_result]


def list_to_keyed_object(input_list: list, key='id') -> dict:
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


def is_valid_question(request_data: dict) -> bool:
    return (
        request_data.get('question', None)
        and request_data.get('answer', None)
        and request_data.get('difficulty', None)
        and request_data.get('category', None)
    )


def is_valid_search(request_data: dict) -> bool:
    return (
        request_data.get('searchTerm', None)
    )


def is_valid_quiz(request_data: dict) -> bool:
    if (
        request_data.get('previous_questions', None)
        and isinstance(request_data['previous_questions'], list)
        and request_data.get('quiz_category')
    ):
        if (
            request_data['quiz_category'].get('id', None)
            and request_data['quiz_category'].get('type', None)
        ):
            return True
    else:
        return False
