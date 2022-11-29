import random as rd

def assign_seat(seats, passenger_no, absent_minded=False):
    availible_seats = [i for i,passenger in enumerate(seats) if passenger == 0]

    if absent_minded == True:
       taken_seat = rd.choice(availible_seats)
       seats[taken_seat] = passenger_no
    else:
        if seats[passenger_no-1] == 0:
            seats[passenger_no-1] = passenger_no
        else:
            taken_seat = rd.choice(availible_seats)
            seats[taken_seat] = passenger_no

    return seats

def create_absent_minded_list(seat_no, number_of_passengers, method="listed"): ## Should be number of absent minded passengers
    absent_list = []

    if method == "listed":
        for i in range(number_of_passengers):
            absent_list.append(i+1)
    if method == "prime":
        prime_list = [i for i in range(2, seat_no) if 0 not in [i%n for n in range(2,i)]]

        for i in range(seat_no):
            if i+1 in prime_list:
                absent_list.append(i+1)
    
    return absent_list

def run_single_simulation(seat_no, absent_no, absent_method="listed"):
    seats = [0] * seat_no
    
    # Absent minded passenger
    absent_list = create_absent_minded_list(seat_no, absent_no, absent_method)

    for passenger_no in range(1, seat_no+1):
        if passenger_no in absent_list:
            seats = assign_seat(seats, passenger_no, absent_minded=True)
        else:
            seats = assign_seat(seats, passenger_no)

    #print(seats)  ## Temp

    if seats[-1] == seat_no:
        return True
    else:
        return False

def run_multiple_simulations(run_no, seat_no, absent_no, absent_method="listed"):
    results = []
    for _ in range(run_no):
        results.append(run_single_simulation(seat_no, absent_no, absent_method))

       # print(results)  ## Temp

    prob = results.count(True)/len(results)

    print(f"Number of runs: {run_no},")
    print(f"Number of seats: {seat_no},")
    print(f"Prob of final passenger getting their seat: {prob},")

if __name__ == '__main__':
    run_multiple_simulations(500, 100, 1)
