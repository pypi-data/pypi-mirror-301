from enum import Enum


class CodeEnum(Enum):
    SUCCESS = (0, "OK")
    RESULT_EMPTY = (1, "查询结果集为空")
    DATA_EMPTY = (2, "预报数据为空")
    VARIABLE_MISSING = (3, "预报数据不存在于查询结果中")
    LENGTH_MISMATCH = (4, "预报数据长度与预报时间点长度不一致")

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message