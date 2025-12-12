nums=input("enter numbers: ")

numbers=[int(x) for x in nums.split(",")]

even=0
odd=0

for n in numbers:
    if n%2==0:
        even=even+1
    else:
        odd=odd+1

print("even numbers: ",even)
print("odd numbers: ",odd)