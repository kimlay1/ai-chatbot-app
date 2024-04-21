# App 1

user_input = input("Enter a string: ")
double = (char * 2 for char in user_input)
output = ''.join(double)

print(f"{user_input} -> {output}")

# App 2

alphabet = "abcdefghijklmnopqrstuvwxyz"
user_range = input("Enter a range of letters (e.g., a-z): ")

start, end = user_range.split('-')
first = alphabet.index(start.lower())
last = alphabet.index(end.lower())

letter = ''.join(alphabet[first:last+1])

if start.isupper() and end.isupper():
    result = letter.upper()
else:
    result = letter
print(result)

