import csv

total_rows = 0
above_500 = 0
total_price = 0
total_qty = 0
products = []

category_input = input("Enter category to search: ")

with open("products.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        total_rows += 1
        price = float(row["price"])
        qty = int(row["quantity"])
        total_price += price
        total_qty += qty
        products.append(row)

        # b) Print each row cleanly
        print(f'ID: {row["product_id"]}, Name: {row["product_name"]}, '
              f'category: {row["category"]}, price: {price}, qty: {qty}')

        # d) Price above 500
        if price > 500:
            above_500 += 1

print("\nTotal rows:", total_rows)
print("Products priced above 500:", above_500)
print("Average price:", total_price / total_rows)
print("Total quantity in stock:", total_qty)

print("\nProducts in category:", category_input)
for p in products:
    if p["category"].lower() == category_input.lower():
        print(p["product_name"])
