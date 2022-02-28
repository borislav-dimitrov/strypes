def counting(n, m):
    players = [i for i in range(1, n + 1)]
    current_index = m - 1

    while len(players) > 1:
        if len(players) == 2 and m % 2 == 0:
            players.remove(players[1])
        elif len(players) == 2 and m % 2 != 0:
            players.remove(players[0])
        else:
            # print(f"Removing player {players[current_index]}")
            players.remove(players[current_index])
            current_index += m - 1
        if current_index >= len(players):
            while current_index >= len(players):
                current_index -= len(players)

    return players[0]


if __name__ == '__main__':
    n = int(input("Input N:"))
    m = int(input("Input M:"))
    print(f"Winning Player is: {counting(n, m)}")
# Answer for 8, 3 => 7
