import json 
import copy
import jsonref
from openapi_core.spec.paths import Spec
from copy import deepcopy
from typing import Any, Dict, List
from jsonref import JsonRefError

# $ref 해소 함수
def resolve_refs_op(spec: Dict[str, Any], base_path: str = '#/components/schemas/') -> Dict[str, Any]:
    def resolve(ref: str) -> Any:
        ref_path = ref[len(base_path):].split('/')
        current = spec
        for part in ref_path:
            current = current.get(part, {})
        return current

    def recurse(data: Any) -> Any:
        if isinstance(data, dict):
            if '$ref' in data:
                resolved = resolve(data['$ref'])
                # Merge resolved properties with defaults if they exist
                if 'default' in resolved:
                    for key, value in resolved['properties'].items():
                        if 'default' in value:
                            resolved['properties'][key]['default'] = value['default']
                return resolved
            else:
                for key, value in data.items():
                    data[key] = recurse(value)
        elif isinstance(data, list):
            for i in range(len(data)):
                data[i] = recurse(data[i])
        return data

    return recurse(spec)

# JSON 파일을 로드하는 함수
def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_json_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

# ref를 해소하고 속성을 병합하는 함수
# ref를 해소하는 함수
def resolve_refs(json_data):
    resolved_json = jsonref.JsonRef.replace_refs(json_data)
    return resolved_json

def resolve_refs(json_data):
    # 참조를 푼 후, 기본값을 주입하기 위한 깊은 복사본 생성
    resolved_json = jsonref.JsonRef.replace_refs(json_data)

    # 기본값 주입
    if "properties" in resolved_json:
        for key, value in resolved_json["properties"].items():
            # 각 속성의 default 값을 확인하고 주입
            if "default" in value:
                value["value"] = value["default"]
                del value["default"]  # 기본값 키 삭제

    return resolved_json

# JSON 파일 로드
file_path = r'C:\MIDAS\MOAPY_main\schemas\managed\moapy\dgnengine\alu_beamcolumn\report_aluminum_beam_column.json'
json_data = load_json_file(file_path)

# def resolve_refs_and_merge(json_data):
#     # 원본 데이터를 깊은 복사하여 변경되지 않도록 함
#     resolved_json = copy.deepcopy(json_data)
    
#     # jsonref로 참조를 해소함
#     resolved_json = jsonref.JsonRef.replace_refs(resolved_json)
    
#     # 원본 데이터를 순회하면서 $ref가 있던 곳의 추가 정보를 복사하여 병합
#     def merge_refs(original, resolved):
#         if isinstance(original, dict):
#             for key, value in original.items():
#                 if isinstance(value, dict):
#                     # $ref가 있던 객체는 resolved에서 덮어쓰기
#                     if "$ref" in value:
#                         resolved[key] = {**value, **resolved.get(key, {})}
#                     else:
#                         merge_refs(value, resolved.get(key, {}))
#         elif isinstance(original, list):
#             for index, item in enumerate(original):
#                 merge_refs(item, resolved[index])

#     merge_refs(json_data, resolved_json)
#     return resolved_json

# def resolve_refs_and_merge(json_data):
#     # 원본 데이터를 깊은 복사하여 변경되지 않도록 함
#     resolved_json = copy.deepcopy(json_data)
    
#     # jsonref로 참조를 해소함
#     resolved_json = jsonref.JsonRef.replace_refs(resolved_json)
    
#     # 원본 데이터를 순회하면서 $ref가 있던 곳의 추가 정보를 복사하여 병합
#     def merge_refs(original, resolved):
#         if isinstance(original, dict):
#             for key, value in original.items():
#                 if isinstance(value, dict):
#                     # $ref가 있는 경우
#                     if "$ref" in value:
#                         # 원본의 title과 description을 유지
#                         original_title = original[key].get("title", key)  # original에서 title 가져오기
#                         original_description = original[key].get("description", "")  # original에서 description 가져오기
                        
#                         # resolved에서 병합
#                         resolved_value = resolved.get(key, {})
#                         resolved_value["title"] = original_title  # 원본 title로 설정
#                         resolved_value["description"] = original_description  # 원본 description으로 설정
#                         resolved[key] = {**resolved_value, **value}  # 추가 정보 병합
#                         resolved[key].pop("$ref", None)  # $ref 제거
#                     else:
#                         merge_refs(value, resolved.get(key, {}))
#         elif isinstance(original, list):
#             for index, item in enumerate(original):
#                 merge_refs(item, resolved[index])

#     merge_refs(json_data, resolved_json)
#     return resolved_json

# def resolve_refs_and_merge(json_data):
#     # 원본 데이터를 깊은 복사하여 변경되지 않도록 함
#     resolved_json = copy.deepcopy(json_data)
    
#     # jsonref로 참조를 해소함
#     resolved_json = jsonref.JsonRef.replace_refs(resolved_json)
    
#     # 원본 데이터를 순회하면서 $ref가 있던 곳의 추가 정보를 복사하여 병합
#     def merge_refs(original, resolved):
#         if isinstance(original, dict):
#             for key, value in original.items():
#                 if isinstance(value, dict):
#                     # $ref가 있는 경우
#                     if "$ref" in value:
#                         # resolved에서 병합
#                         resolved_value = resolved.get(key, {})
#                         # 모든 key-value 쌍을 병합
#                         resolved[key] = {**resolved_value, **value}
#                         # original에서 키를 가져와 병합
#                         for k, v in original[key].items():
#                             if k != "$ref":  # $ref는 제외
#                                 resolved[key][k] = v
#                         resolved[key].pop("$ref", None)  # $ref 제거
#                     else:
#                         merge_refs(value, resolved.get(key, {}))
#         elif isinstance(original, list):
#             for index, item in enumerate(original):
#                 merge_refs(item, resolved[index])

#     merge_refs(json_data, resolved_json)
#     return resolved_json

import jsonref
import copy

import jsonref
import copy

def resolve_refs_and_merge(json_data):
    # 원본 데이터를 깊은 복사하여 변경되지 않도록 함
    resolved_json = copy.deepcopy(json_data)
    
    # jsonref로 참조를 해소함
    resolved_json = jsonref.JsonRef.replace_refs(resolved_json)
    
    # 원본 데이터를 순회하면서 $ref가 있던 곳의 추가 정보를 복사하여 병합
    def merge_refs(original, resolved):
        if isinstance(original, dict):
            for key, value in original.items():
                if isinstance(value, dict):
                    # $ref가 있는 경우
                    if "$ref" in value:
                        # resolved에서 병합
                        resolved_value = resolved.get(key, {})
                        # 모든 key-value 쌍을 병합
                        resolved[key] = {**resolved_value, **value}
                        # original에서 키를 가져와 병합
                        for k, v in original[key].items():
                            if k != "$ref":  # $ref는 제외
                                resolved[key][k] = v

                        # default가 있는 경우 특별 처리
                        if "default" in original[key] and isinstance(original[key]["default"], dict):
                            # original의 default에서 value와 unit을 가져와 병합
                            default_value = original[key]["default"].get("value")
                            default_unit = original[key]["default"].get("unit")

                            if default_value is not None:
                                # value를 properties에 추가
                                resolved[key]["properties"]["value"]["default"] = default_value
                            
                            if default_unit is not None:
                                # unit을 properties에 추가
                                resolved[key]["properties"]["unit"]["default"] = default_unit

                        resolved[key].pop("$ref", None)  # $ref 제거
                    else:
                        merge_refs(value, resolved.get(key, {}))
        elif isinstance(original, list):
            for index, item in enumerate(original):
                merge_refs(item, resolved[index])

    merge_refs(json_data, resolved_json)
    return resolved_json



# $ref 해제 및 메타데이터 유지 적용
resolved_schema = resolve_refs_and_merge(json_data)

# $ref 해소
#resolved_json = resolve_refs(json_data)

# 결과를 파일로 저장
save_json_file("schema_j.json", resolved_schema)
