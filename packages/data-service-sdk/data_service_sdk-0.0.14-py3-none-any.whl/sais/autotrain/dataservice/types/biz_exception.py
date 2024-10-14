class BizException(Exception):
    def __init__(self, code: int, msg: str):
        super().__init__(msg)
        self.code = code
        self.msg = msg

    def __str__(self):
        return f"Error Code: {self.code}, Message: {self.msg}"
