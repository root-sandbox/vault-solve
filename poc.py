import subprocess
import string
import timeit

FINAL_PASSWORD = ""
MAX_PASS_LENGTH = 20
TOTAL_RUNS = 0
TIMING_DATA = []
CHARSET = string.ascii_lowercase

def char_with_longest_time(arr):
    if not arr:
        return None

    max_char = arr[0][0]
    max_time = arr[0][1]

    for char, timing in arr:
        if timing > max_time:
            max_time = timing
            max_char = char

    return max_char

def check_pass(password):
    command = f"subprocess.call(['./vault.o', '{password}'], stdout=subprocess.PIPE)"
    result = timeit.timeit(command, setup="import subprocess", number=1)
    TIMING_DATA.append((password, result))

def main():
    global FINAL_PASSWORD, TOTAL_RUNS, TIMING_DATA

    keep_running = True

    while keep_running:
        if len(FINAL_PASSWORD) > MAX_PASS_LENGTH:
            FINAL_PASSWORD = ""

        for char in CHARSET:
            check_pass(FINAL_PASSWORD + char)

        FINAL_PASSWORD = char_with_longest_time(TIMING_DATA)
        TIMING_DATA = []

        print(f"Current Password: {FINAL_PASSWORD}")
        result = subprocess.run(
            ["./vault.o", FINAL_PASSWORD],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if "success" in result.stdout.decode().lower():
            print(f"Final Password: {FINAL_PASSWORD}")
            print(f"Total Runs: {TOTAL_RUNS}")
            keep_running = False
        
        TOTAL_RUNS += 1

if __name__ == "__main__":
    main()
