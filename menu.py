import dataprocessor


def main():
    while True:

        choice = input('Choose a menupoint!\nYour choices:\n0. Exit\n1. Get world total\nYour choice: ')
        if choice == '0':
            break
        elif choice == '1':
            dataprocessor.get_total()
        else:
            print('in the menu')

    print("Goodbye!")
