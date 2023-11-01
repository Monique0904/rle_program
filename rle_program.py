from console_gfx import ConsoleGfx


# defines a function that when called displays the menu
def menu_display():

    print("\nRLE Menu\n--------\n0. Exit\n1. Load File\n2. Load Test Image\n3. Read RLE String\n"
          "4. Read RLE Hex String\n5. Read Data Hex String\n6. Display Image\n7. Display RLE String\n"
          "8. Display Hex RLE Data\n9. Display Hex Flat Data\n")


# translates data to hex string
def to_hex_string(data):

    hex_string = []
    mysep = ''

    # checks the value of every item in i and replaces it with its hex string equivalent and adds it to the list
    for i in data:

        if i < 10:
            hex_string.append(str(i))

        if i == 10:
            hex_string.append('a')

        if i == 11:
            hex_string.append('b')

        if i == 12:
            hex_string.append('c')

        if i == 13:
            hex_string.append('d')

        if i == 14:
            hex_string.append('e')

        if i == 15:
            hex_string.append('f')

    # the joined list is returned
    return mysep.join(hex_string)


# returns number of runs of data in an image data set
def count_runs(flat_data):

    encoded = []
    count = 1

    # loops through every value in the list and checks if the previous one is equivalent
    for i in range(1, len(flat_data)):

        # if the item in the previous index is equal to the one at I increase count by 1
        if flat_data[i - 1] == flat_data[i]:
            count += 1

            if count >= 15:
                encoded.extend([count, flat_data[i]])      # adds the number of consecutive digits and digit to list
                count = 0

        # if the previous number isn't equal to i then the count will be resent to 1
        else:
            encoded.extend([count, flat_data[i - 1]])     # adds the number of consecutive digits and digit to list
            count = 1

    # makes sure that the last digits are added to the list once the loop is broken out of
    encoded.extend([count, flat_data[i]])

    # calculates number of runs from the encoding of the raw data passed in
    runs = len(encoded) // 2

    return runs

# Returns encoding in RLE of the raw data passed in
def encode_rle(flat_data):

    encoded = []
    count = 1

    # loops through every value in the list and checks if the previous one is equivalent
    for i in range(1, len(flat_data)):

        # if the item in the previous index is equal to the one at I increase count by 1
        if flat_data[i - 1] == flat_data[i]:
            count += 1

            if count >= 15:
                encoded.extend([count, flat_data[i]])     # adds the number of consecutive digits and digit to list
                count = 0

        else:
            encoded.extend([count, flat_data[i - 1]])     # adds the number of consecutive digits and digit to list
            count = 1

    # makes sure that the last digits are added to the list once the loop is broken out of
    encoded.extend([count, flat_data[i]])

    return encoded


# returns decompressed size RLE data
def get_decoded_length(rle_data):

    # adds the items from every other index, starting at 0, to the list
    num_occur = [i for i in rle_data[::2]]

    # returns the sum of the items in the list
    return sum(num_occur)


# returns the decoded data set from RLE encoded data
def decode_rle(rle_data):

    new_list = [rle_data[i:i + 2] for i in range(0, len(rle_data), 2)]

    list = []
    for i in new_list:
        list.extend(i[0] * str(i[-1]).split())

    final = [int(i) for i in list]

    return final


# translates a string in hexadecimal format into byte data
def string_to_data(data_string):

    deci = []

    # iterates through every character in data_string
    for i in data_string:

        # sets the variable equal to the ASCII value of i
        value = ord(str(i))

        # if the ASCII value is a string representing numbers 1-9 it will be converted to and integer and added to list
        if value <= 57:
            deci.append(int(i))

        # if ASCII value is equal to an uppercase chr its equivalent hex value will be calculated and added to list
        if 97 <= value <= 122:
            hex = value - 87
            deci.append(hex)

        # if ASCII value is equal to a lowercase chr its equivalent hex value will be calculated and added to list
        if 65 <= value <= 90:
            hex = value - 55
            deci.append(hex)

    return deci

# Translates RLE data into a human-readable representation
def to_rle_string(rle_data):

    # converts every element in the inputted list to a string
    rle_data_m = [str(i) for i in rle_data]
    list = []

    # groups the elements of the list into a nested list in groups of two
    new_list = [rle_data_m[i:i + 2] for i in range(0, len(rle_data_m), 2)]

    # loops over every value pair in the nested list
    for i in new_list:

        # if the value of the second item is > 9 it is converted to its hex equivalent, otherwise it stays the same
        if int(i[-1]) == 10:
            value = 'a'

        elif int(i[-1]) == 11:
            value = 'b'

        elif int(i[-1]) == 12:
            value = 'c'

        elif int(i[-1]) == 13:
            value = 'd'

        elif int(i[-1]) == 14:
            value = 'e'

        elif int(i[-1]) == 15:
            value = 'f'

        else:
            value = i[-1]

        # concatenates element at index 0 of current list with the value assigned previously and adds it to a new list
        list.append(i[0] + value)

    # returns the list and joins it together with ':'
    return ':'.join(list)

# Translates a string in human-readable RLE format (with delimiters) into RLE byte data
def string_to_rle(rle_string):

    data = rle_string.split(':')
    list = []
    for i in data:

        if i[-1] == 'a':
            value = 10

        elif i[-1] == 'b':
            value = 11

        elif i[-1] == 'c':
            value = 12

        elif i[-1] == 'd':
            value = 13

        elif i[-1] == 'e':
            value = 14

        elif i[-1] == 'f':
            value = 15

        else:
            value = int(i[-1])

        list.extend([int(i[0:-1]), value])


    return list


if __name__ == '__main__':

    # prints welcome message and color spectrum once when program is initiated
    print("Welcome to the RLE image encoder!")
    print("\nDisplaying Spectrum Image:")
    ConsoleGfx.display_image(ConsoleGfx.test_rainbow)

    # defines a variable to store the user menu input
    user_input = 0
    # sets image to the gator test image
    image_data = ConsoleGfx.test_image

    # loops while true
    while True:

        # calls function menu display to display menu and prompts user for input
        menu_display()
        user_input = input("Select a Menu Option: ")

        if user_input == "0":
            break

        # sets image data equal to the file the user wants to load
        elif user_input == "1":
            image_data = ConsoleGfx.load_file(input("Enter name of file to load: "))

        # prints gator test image
        elif user_input == "2":
            print("Test image data loaded.")
            image_data = ConsoleGfx.test_image

        # decodes RLE string inputted by user
        elif user_input == "3":

            input_data = input("Enter an RLE string to be decoded: ")
            image_data = decode_rle(string_to_rle(input_data))

        # reads RLE data from the user in hexadecimal notation without delimiters
        elif user_input == "4":

            input_data = input("Enter the hex string holding RLE data: ")
            image_data = decode_rle(string_to_data(input_data))

        # Reads raw data from the user in hexadecimal notation
        elif user_input == "5": #fixme

            input_data = input("Enter the hex string holding flat data: ")
            list = []
            # iterates through the flat string and adds the correspondinghex values to a list to return the flata byte data
            for i in input_data:

                if i == 'a':
                    value = 10

                elif i == 'b':
                    value = 11

                elif i == 'c':
                    value = 12

                elif i == 'd':
                    value = 13

                elif i == 'e':
                    value = 14

                elif i == 'f':
                    value = 15

                else:
                    value = int(i)

                list.append(value)

            image_data = list

        # displays the current image that that variable image_data is assigned to
        elif user_input == "6":
            print("Displaying image...")
            ConsoleGfx.display_image(image_data)

        # converts the current data into a human-readable RLE representation
        elif user_input == "7":

            print(f"RLE representation: {to_rle_string(encode_rle(image_data))}")

        # converts the current data into RLE hexadecimal representation
        elif user_input == "8":

            print(f"RLE hex values: {to_hex_string(encode_rle(image_data))}")

        # displays the current raw data in hexadecimal representation w/o delimiters
        elif user_input == "9":

            list = []

            # iterates through the image_data list and converts each element to its hex equivalent, prints flat string
            for i in image_data:

                if i == 10:
                    value = 'a'

                elif i == 11:
                    value = 'b'

                elif i == 12:
                    value = 'c'

                elif i == 13:
                    value = 'd'

                elif i == 14:
                    value = 'e'

                elif i == 15:
                    value = 'f'

                else:
                    value = str(i)

                list.append(value)

            print(f"Flat hex values: {''.join(list)}")


        # if an option not on the menu is chosen error message will appear
        else:
            print("Erorr! Invalid input.")