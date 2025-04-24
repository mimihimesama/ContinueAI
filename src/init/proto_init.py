import sys
from pathlib import Path
import importlib
from typing import Dict, Any
from ..constants.packet_constants import packet_names

# ✅ 프로젝트 루트 (ContinueAI/) 기준으로 sys.path 추가
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

proto_messages: Dict[str, Dict[str, Any]] = {
    'packet': {},
    'payload': {}
}

async def load_proto_files() -> None:
    try:
        for key, full_path in packet_names.items():
            module_path, class_name = full_path.rsplit('.', 1)
            module = importlib.import_module(module_path)
            proto_messages['packet'][key] = getattr(module, class_name)
        print('[protobuf] 로드된 packet 메시지:', list(proto_messages['packet'].keys()))
    except Exception as err:
        print(f"[protobuf] 메시지 로드 오류: {err}")

def get_proto_messages() -> Dict[str, Dict[str, Any]]:
    return proto_messages
