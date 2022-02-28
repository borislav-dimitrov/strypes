class Transaction:
    def __init__(self, tr_id, tr_type, tr_date, tr_price, buyer_seller, assets_traded):
        self.tr_id = tr_id
        self.tr_type = tr_type
        self.tr_date = tr_date
        self.tr_price = tr_price
        self.buyer_seller = buyer_seller
        self.assets_traded = assets_traded

    def print_transaction_info(self):
        info = f"{self.tr_id} | {self.tr_type} | {self.tr_date} | " \
               f"{self.tr_price} | {self.buyer_seller} | {self.assets_traded}"
        return info
