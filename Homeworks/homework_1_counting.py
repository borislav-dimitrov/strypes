def counting(n, m):
    """

    :param n: Total players amount
    :param m: step on which the player is removed
    :return: winner
    """
    # Create list with all players
    players = [i for i in range(1, n + 1)]
    # Index is m-1 because it is 0 based
    current_index = m - 1

    # Loop until there is 1 player left
    while len(players) > 1:
        if len(players) == 2 and m % 2 == 0:
            players.remove(players[1])
        elif len(players) == 2 and m % 2 != 0:
            players.remove(players[0])
        else:
            # Remove the m-th player
            players.remove(players[current_index])
            # Incrementing the current index with m - 1 because we already removed one item
            # and the length of the list is - 1
            current_index += m - 1
            # If the index is higher than the list length
            # decrement it by the list length until it is smaller
            # that way we simulate cycling through the players m times
        if current_index >= len(players):
            while current_index >= len(players):
                current_index -= len(players)

    return players[0]


if __name__ == '__main__':
    n = int(input("Input N:"))
    m = int(input("Input M:"))
    print(f"Winning Player is: {counting(n, m)}")
