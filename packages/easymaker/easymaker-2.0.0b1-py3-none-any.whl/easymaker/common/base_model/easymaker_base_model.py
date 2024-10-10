import json
from typing import Any, List, Optional, Union, get_args, get_origin

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from easymaker.common.utils.status_code_utils import replace_status_code


class EasyMakerBaseModel(BaseModel):
    # camelCase의 API 응답을 snake_case 형태의 필드값에 셋팅할 수 있도록 camel 형태의 alias 일괄 추가 및 snake_case 입력도 처리하도록 설정
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        protected_namespaces=(),  # model_ 로 시작하는 필드명은 Pydantic에서 예약된 이름이라 충돌 가능성이 있어 발생하는 경고 끄는 옵션 (model_name은 충돌나는 이름)
    )

    description: Optional[str] = None
    tag_list: Optional[List[Any]] = None
    app_key: Optional[str] = None
    created_datetime: Optional[str] = None

    def __init__(self, **data):
        fields = self.__class__.__annotations__
        # 모든 Optional 필드에 기본값으로 None 설정
        default_data = {field: None for field in fields if get_origin(fields[field]) is Union and type(None) in get_args(fields[field])}
        default_data.update(data)

        for field_name in default_data:  # 모든 status_code 필드에 대해 replace_status_code 함수 적용
            if "_status_code" in field_name or "StatusCode" in field_name:
                default_data[field_name] = replace_status_code(default_data[field_name])
        super().__init__(**default_data)

    def print_info(self):
        print(json.dumps(self.model_dump(), indent=4, ensure_ascii=False))

    def model_dump(self, **kwargs):
        return super().model_dump(by_alias=True, **kwargs)

    def __setattr__(self, key: str, value: Any) -> None:
        read_only_fields = set(attribute_name for attribute_name, model_field in self.model_fields.items() if model_field.repr is False)
        if key in read_only_fields:
            return
        super().__setattr__(key, value)
