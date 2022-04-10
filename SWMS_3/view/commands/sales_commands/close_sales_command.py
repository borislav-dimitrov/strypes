class CloseSalesCommand:
    def __init__(self, controlelr):
        self.controlelr = controlelr

    def __call__(self, *args, **kwargs):
        self.controlelr.close_sales()