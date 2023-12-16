def fibonacci_generator():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

def write_large_file(filename, size):
    with open(filename, 'w') as f:
        for i, n in enumerate(fibonacci_generator()):
            f.write(str(n) + '\n')
            if i > size:
                break

if __name__ == '__main__':
    write_large_file('large_payload.txt', 10_000)