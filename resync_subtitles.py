#!/usr/bin/env python3

from pathlib import Path
import chardet

def detect_encoding(file_name):
    """Detect the file encoding and returns it."""
    file_path = Path(file_name)

    # We must read as binary (bytes) because we don't yet know encoding
    blob = file_path.read_bytes()

    detection = chardet.detect(blob)
    encoding = detection["encoding"]

    return encoding

def delay_time(time, delay):
    """Add delay to timecode in 'hours:minutes:seconds,milliseconds' format."""
    hour, minute, second = time.split(':')

    hours = float(hour)
    minutes = float(minute)
    seconds = float(second.replace(',', '.'))

    total_seconds = 3600*hours + 60*minutes + seconds
    new_total_seconds = total_seconds + delay

    new_hours = new_total_seconds//3600
    new_minutes = (new_total_seconds%3600)//60
    new_seconds = (new_total_seconds%3600)%60

    new_hour = '%02d' % new_hours
    new_minute = '%02d' % new_minutes
    new_second = ('%06.3f' % new_seconds).replace('.', ',')

    new_time = ':'.join([new_hour, new_minute, new_second])

    return new_time

def main():

    input_file_name = input("Input file name: \n")
    delay = float(input("Delay (s): \n").replace(',', '.'))
    output_file_name = input("Output file name: \n")

    detected_encoding = detect_encoding(input_file_name)

    output_file_lines = []

    with open(input_file_name, mode='r', encoding=detected_encoding) as input_file:
        input_file_lines = input_file.readlines()
         
        for line in input_file_lines:
            words = line.split()
            if len(words) == 3 and words[1] == '-->':
                words[0] = delay_time(words[0], delay)
                words[2] = delay_time(words[2], delay)
            new_line = ' '.join(words) + '\n'

            output_file_lines.append(new_line)

    with open(output_file_name, 'w') as output_file:
        output_file.writelines(output_file_lines)

if __name__ == "__main__":
   main()
