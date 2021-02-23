import dataprocessor


def main():
    while True:

        choice = input('Choose a menupoint!\nYour choices:\n0. Exit\n1. Get world data\n2. Get data by '
                       'country code\nYour choice: ')
        if choice == '0':
            break
        elif choice == '1':
            dataprocessor.get_total()
        elif choice == '2':
            dataprocessor.get_latest_country_data_by_code(input("Enter the country code of the country you are "
                                                                "interested in. Country code is in ISO 3166-1 "
                                                                "standard.\n"))
        else:
            print('No such option.')

    print("Goodbye!")
