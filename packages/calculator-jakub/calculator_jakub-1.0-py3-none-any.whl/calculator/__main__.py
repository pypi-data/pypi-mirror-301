import argparse

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def main():
    parser = argparse.ArgumentParser(description="Kalkulator.")
    parser.add_argument('operation', choices=['add', 'subtract'], help='Operacja do wykonania (add lub substract)')
    parser.add_argument('-na', '--number-a', type=float, required=True, help='Liczba A')
    parser.add_argument('-nb', '--number-b', type=float, required=True, help='Liczba B')

    args = parser.parse_args()

    if args.operation == 'add':
        result = add(args.number_a, args.number_b)
    elif args.operation == 'subtract':
        result = subtract(args.number_a, args.number_b)

    print(f"Wynik: {result}")


if __name__ == '__main__':
    main()
