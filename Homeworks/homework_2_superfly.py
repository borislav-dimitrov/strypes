def super_fly(d, v, v1, v2, e):
    """
    s = v * t
    t = v / s

    The fly flies between the trains.
        1. Calculate the lengths flown by the fly when the distance between
            train A and B is == the fly size
        2. Total distance the fly has flown
    :param d: Distance between cities A and B
    :param v: Speed of the fly
    :param v1: The speed of the train from City A -> City B
    :param v2: The speed of the train from City B -> City A
    :param e: The size of the fly
    :return:
    """
    if d <= 0:
        return "Distance between cities must be positive!"
    if v <= 0:
        return "Fly speed must be positive!"
    if v1 == 0 and v2 == 0:
        return "At least one train must be moving!"
    if e <= 0:
        return "The fly size must be positive!"

    fly_lengths = []
    fly_size = float(f"{e:.6f}")
    fly_speed = v
    cities_distance = d
    train_1_speed = v1
    train_2_speed = v2

    # asset positions
    # lets say train 1 and the fly start from 0 and train 2 start from {d} space between the cities
    train1_start_point = 0
    fly_start_point = 0
    train2_start_point = cities_distance

    # set asset current positions
    fly_moving_towards_train2 = True

    # store asset moved km
    train_1_moved = 0
    train_2_moved = 0
    fly_moved = 0

    # time info
    ms = 0.0003
    # second = 1
    # minute = 60
    # hour = 3600
    step = ms
    passed_time = 0

    while True:
        # for {t} time each asset moved {s} kilometres
        train_1_moved += float(train_1_speed * (step / 3600))
        train_2_moved += float(train_2_speed * (step / 3600))
        fly_moved += float(fly_speed * (step / 3600))

        # track current position for each train
        train1_is_at = train1_start_point + train_1_moved
        train2_is_at = train2_start_point - train_2_moved

        # when trains meet exit
        if float(train2_is_at - train1_is_at) <= fly_size:
            break

        # track the current fly position
        if fly_moving_towards_train2:
            fly_is_at = fly_start_point + fly_moved
        else:
            fly_is_at = fly_start_point - fly_moved

        # if fly meet a train reverse the direction
        if fly_is_at >= train2_is_at:
            fly_moving_towards_train2 = False
            fly_lengths.append(fly_moved)
            fly_start_point = train2_is_at
            fly_moved = 0

        if fly_is_at <= train1_is_at:
            fly_moving_towards_train2 = True
            fly_lengths.append(fly_moved)
            fly_start_point = train1_is_at
            fly_moved = 0
        passed_time += step

    # calculate total km the fly flew
    fly_moved = 0
    for item in fly_lengths:
        fly_moved += item

    return f"{fly_lengths}\n{round(fly_moved, 5)}"


if __name__ == '__main__':
    d = int(input("Input the distance between City A and City B: "))
    v = int(input("Input the fly speed: "))
    v1 = int(input("Input train 1 speed: "))
    v2 = int(input("Input train 2 speed: "))
    e = float(input("Input the fly size: "))
    print(super_fly(d, v, v1, v2, e))
