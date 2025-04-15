from datetime import datetime

def format_date(date: datetime) -> str:
    """
    날짜를 'YYYY-MM-DD HH:MM:SS' 형식의 문자열로 변환하는 함수
    
    Args:
        date (datetime): 변환할 날짜 객체
        
    Returns:
        str: 'YYYY-MM-DD HH:MM:SS' 형식의 문자열
    """
    year = date.year
    month = str(date.month).zfill(2)
    day = str(date.day).zfill(2)
    hours = str(date.hour).zfill(2)
    minutes = str(date.minute).zfill(2)
    seconds = str(date.second).zfill(2)
    
    return f'{year}-{month}-{day} {hours}:{minutes}:{seconds}' 