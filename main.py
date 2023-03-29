import csv
import time

tpace = []
# Threshold Pace
lthr = []
# Lactate Threshold Heart Rate
css = []
# Critical Swim Speed
ftp = []
# Functional Threshold Power
lthr_bike = []
# Bike specific Lactate Threshold Heart Rate


"""GENERAL"""


def read_convert_time_to_seconds(in_file_name, in_time_column_name, time_list, in_hr_column_name=None, hr_list=None):
    with open(in_file_name) as file_csv:
        reader = csv.DictReader(file_csv, delimiter=',')
        for line in reader:
            out_time_value = str(line[in_time_column_name])
            # https://gist.github.com/bcooksey/90fc3409ca63c652dcfd9769b7cd0314
            hours_in, minutes_in, seconds_in = out_time_value.split(':')
            out_time_value = (int(hours_in)*3600) + (int(minutes_in)*60) + int(seconds_in)
            time_list.append(out_time_value)

            if in_hr_column_name is not None and hr_list is not None:
                out_hr_value = int(line[in_hr_column_name])
                hr_list.append(out_hr_value)


def read_power_hr(in_file_name, in_power_column_name, in_power_list, in_hr_column_name, hr_list):
    with open(in_file_name) as file_csv:
        reader = csv.DictReader(file_csv, delimiter=',')
        for line in reader:
            out_time_value = int(line[in_power_column_name])
            in_power_list.append(out_time_value)

            out_hr_value = int(line[in_hr_column_name])
            hr_list.append(out_hr_value)


def convert_seconds_in_formatted_str(sec):
    # https://www.askpython.com/python/examples/convert-seconds-hours-minutes
    ty_res = time.gmtime(sec)
    res = time.strftime("%H:%M:%S", ty_res)
    return res


"""PREDICTION METHODS"""


def prediction_pace_hr(writer, race, distance, pace, pace_ratio, heart_rate=None, hr_ratio=None):
    target_pace = convert_seconds_in_formatted_str(pace / pace_ratio)
    target_time = convert_seconds_in_formatted_str(pace * distance / pace_ratio)
    distance_km = [race, target_pace, target_time]
    if heart_rate is not None and hr_ratio is not None:
        target_hr = int(heart_rate*hr_ratio)
        distance_km.append(target_hr)

    writer.writerow(distance_km)


def prediction_power_hr(writer, race, power, power_ratio, heart_rate, hr_ratio):
    target_power = int(power * power_ratio)
    target_hr = int(heart_rate*hr_ratio)
    output = [race, target_power, target_hr]
    writer.writerow(output)


"""ZONES METHODS"""


def zone_pace_hr(writer, zone, pace, pace_ratio, heart_rate=None, hr_ratio=None):
    target_pace = convert_seconds_in_formatted_str(pace / pace_ratio)
    output = [zone, target_pace]
    if heart_rate is not None and hr_ratio is not None:
        target_hr = int(heart_rate*hr_ratio)
        output.append(target_hr)

    writer.writerow(output)


def zone_power_hr(writer, zone, power, power_ratio, heart_rate, hr_ratio):
    target_power = int(power * power_ratio)
    target_hr = int(heart_rate * hr_ratio)
    output = [zone, target_power, target_hr]

    writer.writerow(output)


""" SWIM """
# Swim predictions


def swim_predictions():
    read_convert_time_to_seconds('01 - Swim Entry.csv', 'CSS', css)
    header_swim_predictions = ["Distance", "Pace/100m", "Time"]
    with open('Swim predictions.csv', 'w', newline='') as file_output_csv:
        writer = csv.writer(file_output_csv, delimiter=',')
        writer.writerow(header_swim_predictions)

        prediction_pace_hr(writer, "XS - 400m", 4, css[0], 1)
        prediction_pace_hr(writer, "S - 750m", 7.5, css[0], 0.96)
        prediction_pace_hr(writer, "M - 1500m", 15, css[0], 0.93)
        prediction_pace_hr(writer, "L - 1900m", 19, css[0], 0.90)
        prediction_pace_hr(writer, "XL - 3800m", 38, css[0], 0.85)


# Swim zones
def swim_zones():
    read_convert_time_to_seconds('01 - Swim Entry.csv', 'CSS', css)
    header_swim_zones = ["Zone", "Pace"]
    with open('Swim zones.csv', 'w', newline='') as file_output_csv:
        writer = csv.writer(file_output_csv, delimiter=',')
        writer.writerow(header_swim_zones)

        zone_pace_hr(writer, "i1", css[0], 0.72)
        zone_pace_hr(writer, "i2", css[0], 0.76)
        zone_pace_hr(writer, "i3-", css[0], 0.88)
        zone_pace_hr(writer, "i3", css[0], 0.93)
        zone_pace_hr(writer, "i3+", css[0], 0.96)
        zone_pace_hr(writer, "i4-", css[0], 1)
        zone_pace_hr(writer, "i4+", css[0], 1.03)
        zone_pace_hr(writer, "i5", css[0], 1.10)
        zone_pace_hr(writer, "i6", css[0], 1.15)


""" BIKE """
# Bike predictions


def bike_predictions():
    read_power_hr('02 - Bike Entry.csv', 'FTP', ftp, 'LTHR', lthr_bike)
    header_bike_predictions = ["Distance", "Target Power", "Target HR"]
    with open('Bike predictions.csv', 'w', newline='') as file_output_csv:
        writer = csv.writer(file_output_csv, delimiter=',')
        writer.writerow(header_bike_predictions)

        prediction_power_hr(writer, "XS - 10km", ftp[0], 1.05, lthr_bike[0], 1.03)
        prediction_power_hr(writer, "S - 20km", ftp[0], 1, lthr_bike[0], 1)
        prediction_power_hr(writer, "M - 40km", ftp[0], 0.93, lthr_bike[0], 0.96)
        prediction_power_hr(writer, "L - 90km", ftp[0], 0.85, lthr_bike[0], 0.90)
        prediction_power_hr(writer, "XL - 180km", ftp[0], 0.75, lthr_bike[0], 0.85)


# Bike zones
def bike_zones():
    read_power_hr('02 - Bike Entry.csv', 'FTP', ftp, 'LTHR', lthr_bike)
    header_bike_zones = ["Zone", "Target Power", "Target HR"]
    with open('Bike zones.csv', 'w', newline='') as file_output_csv:
        writer = csv.writer(file_output_csv, delimiter=',')
        writer.writerow(header_bike_zones)

        zone_power_hr(writer, "i1", ftp[0], 0.50, lthr_bike[0], 0.60)
        zone_power_hr(writer, "i2", ftp[0], 0.65, lthr_bike[0], 0.75)
        zone_power_hr(writer, "i3-", ftp[0], 0.75, lthr_bike[0], 0.85)
        zone_power_hr(writer, "i3", ftp[0], 0.85, lthr_bike[0], 0.90)
        zone_power_hr(writer, "i3+", ftp[0], 0.93, lthr_bike[0], 0.96)
        zone_power_hr(writer, "i4-", ftp[0], 1, lthr_bike[0], 1)
        zone_power_hr(writer, "i4+", ftp[0], 1.05, lthr_bike[0], 1.03)
        zone_power_hr(writer, "i5", ftp[0], 1.23, lthr_bike[0], 1.05)
        zone_power_hr(writer, "i6", ftp[0], 1.35, lthr_bike[0], 1.07)


""" RUN """
# Run predictions


def run_predictions():
    read_convert_time_to_seconds('03 - Run Entry.csv', 'Threshold pace', tpace, 'LTHR', lthr)
    header_run_predictions = ["Distance", "Pace", "Time", "Target HR"]
    with open('Run predictions.csv', 'w', newline='') as file_output_csv:
        writer = csv.writer(file_output_csv, delimiter=',')
        writer.writerow(header_run_predictions)

        prediction_pace_hr(writer, "5 km", 5, tpace[0], 1.04, lthr[0], 1.02)
        prediction_pace_hr(writer, "10 km", 10, tpace[0], 1, lthr[0], 1)
        prediction_pace_hr(writer, "Half Marathon", 21.095, tpace[0], 0.94, lthr[0], 0.96)
        prediction_pace_hr(writer, "Marathon", 42.195, tpace[0], 0.90, lthr[0], 0.93)


# Run zones
def run_zones():
    read_convert_time_to_seconds('03 - Run Entry.csv', 'Threshold pace', tpace, 'LTHR', lthr)
    header_run_zones = ["Zone", "Target pace", "Target HR"]
    with open('Run zones.csv', 'w', newline='') as file_output_csv:
        writer = csv.writer(file_output_csv, delimiter=',')
        writer.writerow(header_run_zones)

        zone_pace_hr(writer, "i1", tpace[0], 0.60, lthr[0], 0.71)
        zone_pace_hr(writer, "i2", tpace[0], 0.65, lthr[0], 0.78)
        zone_pace_hr(writer, "i3-", tpace[0], 0.87, lthr[0], 0.89)
        zone_pace_hr(writer, "i3", tpace[0], 0.91, lthr[0], 0.94)
        zone_pace_hr(writer, "i3+", tpace[0], 0.94, lthr[0], 0.97)
        zone_pace_hr(writer, "i4-", tpace[0], 1, lthr[0], 1)
        zone_pace_hr(writer, "i4+", tpace[0], 1.03, lthr[0], 1.02)
        zone_pace_hr(writer, "i5", tpace[0], 1.10, lthr[0], 1.04)
        zone_pace_hr(writer, "i6", tpace[0], 1.15, lthr[0], 1.07)


"""MENUS"""


def menu_main():
    menu = input("\nMain Menu (Type the corresponding number):\n"
                 "1. Swim\n2. Bike\n3. Run\n9. Exit program\n")
    if menu == "1":
        menu_swim()

    elif menu == "2":
        menu_bike()

    elif menu == "3":
        menu_run()

    elif menu == "9":
        exit()

    else:
        print("This is not a suitable answer.\n")
        menu_main()


def menu_swim():
    menu = input("\nYou selected the SWIM section.\n\n"
                 "What would you like to know? (Type the corresponding number):\n"
                 "0. Back\n1. Race predictions\n2. Training zones\n9. Exit program\n")
    if menu == "0":
        menu_main()

    elif menu == "1":
        swim_predictions()
        print("The file 'Swim predictions.csv' is ready.")

    elif menu == "2":
        swim_zones()
        print("The file 'Swim zones.csv' is ready.")

    elif menu == "9":
        exit()

    else:
        print("This is not a suitable answer.\n")
        menu_swim()
        return

    menu_main()


def menu_bike():
    menu = input("\nYou selected the BIKE section.\n\n"
                 "What would you like to know? (Type the corresponding number):\n"
                 "0. Back\n1. Race predictions\n2. Training zones\n9. Exit program\n")
    if menu == "0":
        menu_main()
        return

    elif menu == "1":
        bike_predictions()
        print("The file 'Bike predictions.csv' is ready.")

    elif menu == "2":
        bike_zones()
        print("The file 'Bike zones.csv' is ready.")

    elif menu == "9":
        exit()

    else:
        print("This is not a suitable answer.\n")
        menu_bike()
        return

    menu_main()


def menu_run():
    menu = input("\nYou selected the RUN section.\n\n"
                 "What would you like to know? (Type the corresponding number):\n"
                 "0. Back\n1. Race predictions\n2. Training zones\n9. Exit program\n")
    if menu == "0":
        menu_main()
        return

    elif menu == "1":
        run_predictions()
        print("The file 'Running predictions.csv' is ready.")

    elif menu == "2":
        run_zones()
        print("The file 'Running zones.csv' is ready.")

    elif menu == "9":
        exit()

    else:
        print("This is not a suitable answer.\n")
        menu_run()
        return

    menu_main()


menu_main()
