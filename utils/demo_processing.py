import multiprocessing
import time

def square_numbers(numbers, result):
    for num in numbers:
        time.sleep(0.0005)
        result.append(num * num)

if __name__ == "__main__":
    numbers = list(range(1, 10000))
    result = []

    start_time = time.time()

    process1 = multiprocessing.Process(target=square_numbers, args=(numbers[:5000], result))
    process2 = multiprocessing.Process(target=square_numbers, args=(numbers[5000:], result))

    process1.start()
    process2.start()

    process1.join()
    process2.join()

    end_time = time.time()

    print(f"Processing Time: {end_time - start_time} seconds")
