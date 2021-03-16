from datetime import datetime

# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

def count_sort_letters(array, size, col, base, max_len):
    """ Helper routine for performing a count sort based upon column col """
    output = [0] * size
    count = [0] * (base + 1)  # One addition cell to account for dummy letter
    min_base = ord('a') - 1  # subtract one too allow for dummy character

    for item in array:  # generate Counts
        # get column letter if within string, else use dummy position of 0
        # col_item = str(item[col])
        letter = ord(item[col]) - min_base if col < len(item) else 0
        count[letter] += 1

    for i in range(len(count) - 1):  # Accumulate counts
        count[i + 1] += count[i]

    for item in reversed(array):
        # Get index of current letter of item at index col in count array
        letter = ord(item[col]) - min_base if col < len(item) else 0
        output[count[letter] - 1] = item
        count[letter] -= 1

    return output


def radix_sort_letters(array, max_col=None):
    """ Main sorting routine """
    if not max_col:
        print(max(array, key=len))
        max_col = len(max(array, key=len))  # edit to max length
        print(max_col)
    for col in range(max_col - 1, -1, -1):  # max_len-1, max_len-2, ...0
        array = count_sort_letters(array, len(array), col, 105, max_col)

    return array


def count_sort_letters_dict(array, size, col, base, max_len):
    """ Helper routine for performing a count sort based upon column col """
    # output = {}
    output = [0] * size
    count = [0] * (base + 1)  # One addition cell to account for dummy letter
    min_base = ord('a') - 1  # subtract one too allow for dummy character

    for item in array:  # generate Counts
        # get column letter if within string, else use dummy position of 0
        key = list(item.keys())[0]
        letter = ord(key[col]) - min_base if col < len(key) else 0
        count[letter] += 1

    for i in range(len(count) - 1):  # Accumulate counts
        count[i + 1] += count[i]

    for item in reversed(array):
        # Get index of current letter of item at index col in count array
        key = list(item.keys())[0]
        letter = ord(key[col]) - min_base if col < len(key) else 0
        output[count[letter] - 1] = item
        # output[count[letter] - 1] = {item: my_dict[item]}
        count[letter] -= 1

    return output


def radix_sort_letters_dict(array, max_col=None):
    """ Main sorting routine """
    if not max_col:
        max_col = len(list(max(array, key=len).keys())[0])  # edit to max length

    for col in range(max_col - 1, -1, -1):  # max_len-1, max_len-2, ...0
        array = count_sort_letters_dict(array, len(array), col, 105, max_col)

    return array

def yield_line():
    with open("first-100-mb-input.txt") as myfile:
        for line in myfile:
            yield line

def main():

    print(datetime.now())
    unordered_array = []
    for line in yield_line():
        try:
            key = line[:10]
            hex_number = line[12:44]
            value = line[45:]
            unordered_array.append(
                {
                    key: {
                        'hex_number': hex_number,
                        'value': value
                    }
                }
            )
        except ValueError:
            print(line)
            raise

    ordered_array = radix_sort_letters_dict(unordered_array)

    with open('ordered.txt', 'w+') as my_write_file:
        for item in ordered_array:
            for key, value in item.items():
                my_write_file.write(f'{key}  {value["hex_number"]}  {value["value"]}')


    print(datetime.now())



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
