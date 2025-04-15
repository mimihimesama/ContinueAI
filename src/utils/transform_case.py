import re
from typing import Any, Dict, List, Union

def string_to_camel_case(string: str) -> str:
    """
    문자열을 camelCase로 변환하는 함수
    
    Args:
        string (str): 변환할 문자열
        
    Returns:
        str: camelCase로 변환된 문자열, 문자열이 아닌 경우 원본 값
    """
    if isinstance(string, str):
        # 언더스코어나 공백으로 구분된 문자열을 camelCase로 변환
        words = re.split(r'[_\s]+', string)
        return words[0].lower() + ''.join(word.capitalize() for word in words[1:])
    return string

def string_to_pascal_case(string: str) -> str:
    """
    문자열을 PascalCase로 변환하는 함수
    
    Args:
        string (str): 변환할 문자열
        
    Returns:
        str: PascalCase로 변환된 문자열, 문자열이 아닌 경우 원본 값
    """
    if isinstance(string, str):
        # 언더스코어나 공백으로 구분된 문자열을 PascalCase로 변환
        words = re.split(r'[_\s]+', string)
        return ''.join(word.capitalize() for word in words)
    return string

def to_camel_case(obj: Union[Dict, List, Any]) -> Union[Dict, List, Any]:
    """
    객체의 키를 camelCase로 변환하는 함수
    
    Args:
        obj (Union[Dict, List, Any]): 변환할 객체
        
    Returns:
        Union[Dict, List, Any]: 키가 camelCase로 변환된 객체
    """
    if isinstance(obj, list):
        # 배열인 경우, 배열의 각 요소에 대해 재귀적으로 to_camel_case 함수를 호출
        return [to_camel_case(item) for item in obj]
    elif isinstance(obj, dict):
        # 객체인 경우, 객체의 키를 camelCase로 변환하고, 값에 대해서도 재귀적으로 to_camel_case 함수를 호출
        return {string_to_camel_case(key): to_camel_case(value) for key, value in obj.items()}
    # 객체도 배열도 아닌 경우, 원본 값을 반환
    return obj 