def get_id_for_new_client(all_clients):
    highest_id = 0
    for client in all_clients:
        if client.client_id + 1 > highest_id:
            highest_id = client.client_id

    return highest_id + 1


def get_client_by_id(client_id, all_clients):
    for client in all_clients:
        if client.client_id == int(client_id):
            return client


def get_client_index_by_id(client_id, all_clients):
    for client in range(len(all_clients)):
        if all_clients[client].client_id == int(client_id):
            return client
