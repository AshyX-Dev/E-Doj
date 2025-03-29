class Includes(object):
    def __init__(self, res: dict = {}):
        self.exists: bool = res.get("exists", False)
        self.phone: str = res.get("phone", "")
        self.codeStep: bool = res.get("codeStep", False)
