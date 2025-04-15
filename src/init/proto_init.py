import os
from pathlib import Path
from typing import List, Dict, Any
import json
from google.protobuf import descriptor_pool
from google.protobuf import message_factory
from ..constants.packet_constants import packet_names

# 프로토콜 버퍼 파일 디렉토리 경로
proto_dirname = Path(__file__).parent.parent / 'protobuf'

def get_all_proto_file_paths(directory: Path, file_list: List[Path] = None) -> List[Path]:
    """
    디렉토리 내의 모든 .proto 파일 경로를 반환하는 함수
    
    Args:
        directory (Path): 검색할 디렉토리 경로
        file_list (List[Path], optional): 파일 경로 목록. 기본값은 None.
        
    Returns:
        List[Path]: .proto 파일 경로 목록
    """
    if file_list is None:
        file_list = []
    
    for item in directory.iterdir():
        if item.is_dir():
            get_all_proto_file_paths(item, file_list)
        elif item.suffix == '.proto':
            file_list.append(item)
    
    return file_list

# 프로토콜 버퍼 파일 목록
proto_files = get_all_proto_file_paths(proto_dirname)
proto_messages: Dict[str, Dict[str, Any]] = {
    'packet': {},
    'payload': {}
}

async def load_proto_files() -> None:
    """
    프로토콜 버퍼 파일을 로드하는 함수
    """
    try:
        # 프로토콜 버퍼 파일이 없는 경우 더미 메시지 생성
        if not proto_files:
            print("프로토콜 버퍼 파일이 없습니다. 더미 메시지를 생성합니다.")
            for key, value in packet_names.items():
                # 더미 메시지 클래스 생성
                message_class = type(
                    value,
                    (message_factory.Message,),
                    {
                        '__init__': lambda self, **kwargs: super(self.__class__, self).__init__(**kwargs),
                        'SerializeToString': lambda self: json.dumps(kwargs).encode('utf-8'),
                        'ParseFromString': lambda self, data: self.__dict__.update(json.loads(data.decode('utf-8'))),
                    }
                )
                proto_messages['packet'][key] = message_class
        
        print('Successfully loaded protobuf files.')
        print([name for name in proto_messages['packet'].keys()])
    except Exception as err:
        print(f"프로토콜 버퍼 파일 로드 중 오류 발생: {err}")

def get_proto_messages() -> Dict[str, Dict[str, Any]]:
    """
    프로토콜 버퍼 메시지를 반환하는 함수
    
    Returns:
        Dict[str, Dict[str, Any]]: 프로토콜 버퍼 메시지
    """
    return proto_messages 