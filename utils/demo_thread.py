import threading
import time

def square_numbers(numbers, result):
    for num in numbers:
        time.sleep(0.0005)
        result.append(num * num)

if __name__ == "__main__":
    numbers = list(range(1, 10000))
    result = []

    start_time = time.time()

    thread1 = threading.Thread(target=square_numbers, args=(numbers[:5000], result))
    thread2 = threading.Thread(target=square_numbers, args=(numbers[5000:], result))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    end_time = time.time()

    print(f"Threading Time: {end_time - start_time} seconds")
