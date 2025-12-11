import pandas as pd

df = pd.read_csv("Products.csv")

print("\n--- Product List ---")
for index, row in df.iterrows():
    print(
        f"ID: {row['product_id']} | "
        f"Name: {row['product_name']} | "
        f"Category: {row['category']} | "
        f"Price: {row['price']} | "
        f"Quantity: {row['quantity']}"
    )

# c) Total rows
print("\nTotal number of rows:", len(df))

# d) Products priced above 500
print("Products priced above 500:", len(df[df['price'] > 500]))

# e) Average price
print("Average price:", df['price'].mean())

# f) Filter by category (user input)
category = input("\nEnter category: ")
filtered = df[df['category'].str.lower() == category.lower()]
print(filtered)

# g) Total quantity
print("\nTotal quantity in stock:", df['quantity'].sum())
