from fastapi import APIRouter, HTTPException, status

from app.service import process_string, read_string, search_strings, remove_string, search_strings_by_nlp
from app.schemas import StringAnalysed, StringRaw

router = APIRouter()

@router.post('/strings')
def create_string(payload: dict):

    try:
        string = payload["value"]
        print(string)
    except Exception:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid request body or missing 'value' field")

    if not isinstance(string, str):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid data type for 'value' (must be string)")

    response = process_string(string)
    return response

@router.get('/strings/filter-by-natural-language')
def filter_by_nlp(query: str):

    response = search_strings_by_nlp(query)

    return response


@router.get('/strings/{string_value}')
def get_string(string_value: str):
    response = read_string(string_value)

    return response

@router.get('/strings')
def filter_strings(is_palindrome: bool= None, min_length: int = None, max_length: int = None, word_count: int = None, contains_character: str = None):
    query = {
        'is_palindrome': is_palindrome,
        'min_length': min_length,
        'max_length': max_length,
        'word_count': word_count,
        'contains_character': contains_character
    }
    response = search_strings(query)

    return response


@router.delete('/strings/{string_value}')
def delete_string(string_value: str):
    response = remove_string(string_value)

    return