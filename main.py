import boto3
import os
import sys
import uuid
from urllib.parse import unquote_plus

s3_client = boto3.client('s3')

def count_sort_letters(array, size, col, base, max_len):
    """ Helper routine for performing a count sort based upon column col """
    output = [0] * size
    count = [0] * (base + 1)  # One addition cell to account for dummy letter
    min_base = ord('a') - 1  # subtract one too allow for dummy character

    for item in array:  # generate Counts
        # get column letter if within string, else use dummy position of 0
        key = list(item.keys())[0]
        print("Item in ARRAY: " + key)
        letter = ord(key[col]) - min_base if col < len(key) else 0
        count[letter] += 1

    for i in range(len(count) - 1):  # Accumulate counts
        count[i + 1] += count[i]

    for item in reversed(array):
        # Get index of current letter of item at index col in count array
        key = list(item.keys())[0]
        letter = ord(key[col]) - min_base if col < len(key) else 0
        output[count[letter] - 1] = item
        count[letter] -= 1

    return output


def radix_sort_letters(array, max_col=None):
    """ Main sorting routine """
    if not max_col:
        # print(max(array, key=len))
        max_col = len(list(max(array, key=len).keys())[0])  # edit to max length

    for col in range(max_col - 1, -1, -1):  # max_len-1, max_len-2, ...0
        print(col)
        array = count_sort_letters(array, len(array), col, 105, max_col)

    return array

def iterate_file(event):
    s3 = boto3.resource('s3')
    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']
        bucket_name_upload = f'{bucket_name}-sorted'
        file_name_upload = f'{object_key.split(".")[0]}-reordered.txt'
        print("BEFORE BUCKET INIT")
        bucket = s3.Bucket(bucket_name)
        object = bucket.Object(key=object_key)
        print("AFTER OBJECT INIT")
        # get the object
        response = object.get()
        # read the contents of the file
        lines = response['Body'].iter_lines()
        for line in lines:
            yield line.decode('utf-8')

def lambda_handler(event, context):
    unordered_array = []
    for decoded_line in iterate_file(event):
        key = decoded_line[:10]
        hex_number = decoded_line[12:44]
        value = decoded_line[45:]
        unordered_array.append(
            {
                key: {
                    'hex_number': hex_number,
                    'value': value
                }
            }
        )
    print("After for loop")
    ordered_array = radix_sort_letters(unordered_array)
    print("After sort")
    string_array = ""
    for item in ordered_array:
        for key, value in item.items():
            string_array += f'{key}  {value["hex_number"]}  {value["value"]}\n'
    print("Created string array")
    s3_client.put_object(
        Bucket=bucket_name_upload,
        Key=file_name_upload,
        Body=string_array,
    )
    print("DONE")
