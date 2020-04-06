import matplotlib.pyplot as plt
import matplotlib
import time
import matplotlib.dates as mdates


def pretty_print_errors(path):
    # count, temp, light, sent_time, received_time

    first_count = 1
    second_count = 1

    error_count = 0
    other_error_count = 0

    single_error_lines = list()
    paired_error_lines = list()
    other_error_list = list()

    with open(path, "r") as file:
        header_row = True
        for line in file:
            if not header_row:
                stripped_line = line.replace("\n", "")
                split_string = stripped_line.split(",")
                if len(split_string) != 5:
                    try:
                        error_trigger = int(split_string[0])  # will trigger error if can't cast int
                        single_error_lines.append((first_count, stripped_line))
                        error_count += 1
                    except:
                        other_error_list.append(stripped_line)
                        other_error_count += 1
            else:
                header_row = False
            first_count += 1

    with open(path, "r") as file:
        header_row = True
        for line in file:
            if not header_row:
                stripped_line = line.replace("\n", "")
                for item in single_error_lines:
                    if (second_count-1) == item[0]:
                        paired_error_lines.append((item, (second_count,stripped_line)))
            else:
                header_row = False
            second_count += 1

    print("Errors:\t" + str(error_count))
    for item in paired_error_lines:
        line_one = item[0]
        line_two = item[1]
        print("")
        print(line_one[1])
        print(line_two[1])
    print("Other errors:\t" + str(other_error_count))
    for item in other_error_list:
        print(item)

def read_and_modify_file(path):
    # count, temp, light, sent_time, received_time
    data_good = []
    data_bad = []
    skip = True
    count = -1
    # ref = -1
    with open(path, "r") as file:
        for line in file:
            if not skip:
                count += 1
                stripped_line = line.replace("\n", "")
                mappy = {}
                splitted_string = stripped_line.split(",")
                if len(splitted_string) == 5:
                    mappy["count"] = int(splitted_string[0])
                    mappy["temp"] = float(splitted_string[1])
                    mappy["light"] = int(splitted_string[2])
                    mappy["sent_time"] = int(splitted_string[3])
                    mappy["received_time"] = float(splitted_string[4])
                    if count == 0:
                        count = mappy["count"]
                    elif count == mappy["count"]:
                        data_good.append(mappy)
                    else:
                        data_bad.append(mappy)
                        count = mappy["count"]
                else:
                    try:
                        int(splitted_string[0])
                        count += 1
                    except:
                        count -= 1
                    mappy["line_count"] = count
                    mappy["line"] = line
                    data_bad.append(mappy)
            else:
                skip = False
    return {"good": data_good, "bad": data_bad}


def prepare_data_for_graphs(path):
    print("CALLED")
    header_row = True
    fatty_boom_boom = list()
    count = -1
    with open(path, "r") as file:
        for line in file:
            if not header_row:
                count += 1
                stripped_line = line.replace("\n", "")
                split_string = stripped_line.split(",")
                if len(split_string) == 5:
                    if count == 0:
                        count = int(stripped_line[0])
                        fatty_boom_boom.append(stripped_line)
                    elif count == int(stripped_line[0]):
                        fatty_boom_boom.append(stripped_line)
                    else:
                        print("yikes")
                        print(count)
                        count = int(stripped_line[0])
            else:
                header_row = False
    with open("output.csv", "w") as file:
        for line in fatty_boom_boom:
            file.write(str(line) + "\n")
    return fatty_boom_boom


def time_checker(shitton_of_data):
    lowest = 20000000000000
    highest = -1
    average = 0
    oof = []
    count = 0
    for mapp in shitton_of_data:
        count += 1
        local_data = {}
        sent_time = mapp["sent_time"]
        received_time = mapp["received_time"]
        difference = received_time - float(sent_time)
        if lowest > difference:
            lowest = difference
        elif highest < difference:
            highest = difference
        average += difference
        local_data["difference"] = difference
        local_data["time_stamp"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(sent_time)/1000))
        oof.append(local_data)
    average = average / len(shitton_of_data)
    return {"lowest": lowest, "average": average, "highest": highest, "time_data": oof}


def create_file(data):
    with open("cheesedippers.csv", "w") as file:
        for line in data:
            file.write(line["time_stamp"] + ", ")
            file.write(str(line["difference"]) + "\n")


data = read_and_modify_file("log.csv")
# data = prepare_data_for_graphs("log.csv")
# temp = check_missing_count(data["good"])
# best_data = temp["good"]
# all_the_bad_data = []
# all_the_bad_data.extend(data["bad"])
# all_the_bad_data.extend(temp["bad"])
# data["bad"].extend(temp["bad"])
# print(len(all_the_bad_data))
# print(*all_the_bad_data, sep='\n')
print(len(data["bad"]))
print(*data["bad"], sep='\n')
pp = time_checker(data["good"])     # lowest, average, highest, time_data
print(pp["lowest"])
print(pp["average"])
print(pp["highest"])
time_data = pp["time_data"]
create_file(time_data)



