import random as rd
import json

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

def evaluate_simulation(seats):
    evalualtion = []

    for seat, passenger in enumerate(seats):
        if seat+1 == passenger:
            evalualtion.append(True)
        else:
            evalualtion.append(False)

    return evalualtion

def run_single_simulation(seat_no, absent_no, absent_method="listed", consider_all_seats=False):
    seats = [0] * seat_no
    
    # Absent minded passenger
    absent_list = create_absent_minded_list(seat_no, absent_no, absent_method)

    for passenger_no in range(1, seat_no+1):
        if passenger_no in absent_list:
            seats = assign_seat(seats, passenger_no, absent_minded=True)
        else:
            seats = assign_seat(seats, passenger_no)

    #print(seats)  ## Temp

    evaluation = evaluate_simulation(seats)

    if consider_all_seats:
        return evaluation
    else:
        return evaluation[-1]


def run_multiple_simulations(run_no, seat_no, absent_no, absent_method="listed", consider_all_seats=False):
    results = []
    for _ in range(run_no):
        results.append(run_single_simulation(seat_no, absent_no, absent_method=absent_method, consider_all_seats=consider_all_seats))

       # print(results)  ## Temp

    if consider_all_seats:
        prob_list = []
        for seat in range(seat_no):
            prob_count = 0
            for run_eval in results:
                if run_eval[seat]:
                    prob_count += 1
                else:
                    prob_count += 0

            prob = prob_count / len(results)
            prob_list.append(prob)
        prob = prob_list[-1]
    else:
        prob = results.count(True) / len(results)

    if consider_all_seats:
        with open(".\Passenger_Probs.json", "w") as f:
            json.dump(prob_list, f, indent=4)

    print(f"Number of runs: {run_no},")
    print(f"Number of seats: {seat_no},")
    print(f"Prob of final passenger getting their seat: {prob},")

    if consider_all_seats:
        print(f"Summary is saved at {str(f.name)},")

if __name__ == '__main__':
    run_multiple_simulations(50000, 100, 1, consider_all_seats=True)

