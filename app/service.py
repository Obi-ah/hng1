import hashlib

from fastapi import HTTPException, status

from app.schemas import StringAnalysed
from app.storage import all_strings


def is_palindrome(string):
    return string == string[::-1]

def freq_counter(string):
    counter = {}
    for char in string:
        counter[char] = counter.get(char, 0) + 1

    return counter

def get_hash(input):
    return hashlib.sha256(input.encode('utf-8')).hexdigest()

def save(data):
    data = StringAnalysed(**data)
    all_strings[f'{data.id}'] = data

    return data


def process_string(string: str):
    sha_hash = get_hash(string)

    if sha_hash in all_strings:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="String already exists in the system")

    properties = {'length': len(string),
                  'is_palindrome': is_palindrome(string),
                  'unique_characters': len(set(string)),
                  'word_count': len(string.split()),
                  'sha256_hash': sha_hash,
                  'character_frequency_map': freq_counter(string)
                  }

    data = {'id': sha_hash,
            'value': string,
            'properties': properties,
            }

    save(data)

    return save(data)


def read_string(string: str):
    string_id = get_hash(string)
    if string_id in all_strings:
        return all_strings[string_id]

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="String does not exist in the system")


def search_strings(params: dict):
    filtered = []
    if not isinstance(params.get('is_palindrome', None), (bool, type(None))) or not isinstance(params.get('min_length', None), (int, type(None))) or not isinstance(params.get('max_length', None), (int, type(None))) or not isinstance(params.get('word_count', None), (int, type(None))) or not isinstance(params.get('contains_character', None), (str, type(None))):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid query parameter values or types")

    min_length = 0 if params.get('min_length', None) is None else params.get('min_length')
    max_length = float('inf') if params.get('max_length', None) is None else params.get('max_length')


    for string_id, string in all_strings.items():
        if (params.get('is_palindrome', None) is not None) and not params.get('is_palindrome', None) == string.properties.is_palindrome:
            continue
        if ((params.get('min_length', None) is not None) or (params.get('max_length', None) is not None)) and not (min_length <= string.properties.length <= max_length):
            continue
        if (params.get('word_count', None) is not None) and not params.get('word_count', None) == string.properties.word_count:
            continue
        if (params.get('contains_character', None) is not None) and not params.get('contains_character', None) in string.properties.character_frequency_map:
            continue

        filtered.append(string)


    data = {
        'data': filtered,
        'count': len(filtered),
        'filters_applied': params

    }

    return data

def interpret_nlp_query(query: str) -> dict:
    query_lower = query.lower()
    filters = {}

    if "palindrome" in query_lower or "palindromic" in query_lower:
        filters["is_palindrome"] = True

    if "single word" in query_lower or "one word" in query_lower:
        filters["word_count"] = 1

    if "longer than" in query_lower:
        try:
            num = int(query_lower.split("longer than")[1].split()[0])
            filters["min_length"] = num + 1
        except Exception:
            pass

    if "shorter than" in query_lower:
        try:
            num = int(query_lower.split("shorter than")[1].split()[0])
            filters["max_length"] = num - 1
        except Exception:
            pass

    if "containing the letter" in query_lower:
        char = query_lower.split("containing the letter")[1].strip().split()[0]
        filters["contains_character"] = char
    elif "contain the first vowel" in query_lower:
        filters["contains_character"] = "a"

    return filters


def search_strings_by_nlp(nlp_query):
    query = interpret_nlp_query(nlp_query)
    result = search_strings(query)['data']

    data = {'data': result,
            'count': len(result),
            'interpreted_query': {
                "original": nlp_query,
                "parsed_filters": query
                }
            }

    return data


def remove_string(string: str):
    string_id = get_hash(string)
    deleted = all_strings.pop(string_id, None)

    if deleted:
        raise HTTPException(status_code = status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="String does not exist in the system")
