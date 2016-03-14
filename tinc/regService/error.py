class Error(Exception):
    pass

class AddressError(Error):
    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg
