def get_id_for_new_transaction(all_transactions):
    highest_id = 0
    for transaction in all_transactions:
        if transaction.tr_id + 1 > highest_id:
            highest_id = transaction.tr_id

    return highest_id + 1
