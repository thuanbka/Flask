import time

def square_numbers(numbers, result):
    for num in numbers:
        time.sleep(0.0005)
        result.append(num * num)

if __name__ == "__main__":
    numbers = list(range(1, 10000))
    result = []

    start_time = time.time()
    square_numbers(numbers=numbers, result=result)
    end_time = time.time()

    print(f"Threading Time: {end_time - start_time} seconds")
