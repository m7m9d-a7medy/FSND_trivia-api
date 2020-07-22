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
        request_data['question']
        and request_data['answer']
        and request_data['difficulty']
        and request_data['category']
    )


def is_valid_search(request_data: dict) -> bool:
    return (
        request_data['searchTerm']
    )


def is_valid_quiz(request_data: dict) -> bool:
    if (
        isinstance(request_data['previous_questions'], list)
        and request_data['quiz_category']
    ):
        print('found')
        if (
            request_data['quiz_category']['id']
            and request_data['quiz_category']['type']
        ):
            return True
    else:
        return False
