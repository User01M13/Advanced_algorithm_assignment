
import time
import random

TABLE_SIZE = 20
DATASET_SIZES = [100, 1000, 10000, 50000]
NUM_SEARCHES = 200

# Entity class for a pharmacy product
class Product:
    def __init__(self, product_id, name, price, quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return (f"ID: {self.product_id} | "
                f"Name: {self.name} | "
                f"Price: RM{self.price:.2f} | "
                f"Stock: {self.quantity}")


#hash table using open addressing with linear probing
class HashTable:
    def __init__(self, size):
        if size <= 0:
            raise ValueError("Hash table size must be greater than zero.")
        self.size = size
        self.table = [None] * size

    #division method hash function
    def hash_function(self, key):
        return key % self.size

    # Insert using linear probing: if a slot is taken, try the next one
    def insert(self, product, display=True):
        #compute the starting slot index
        index = self.hash_function(product.product_id)

        for i in range(self.size):
            slot = (index + i) % self.size

            if (self.table[slot] is not None
                    and self.table[slot].product_id == product.product_id):
                if display:
                    print("[ERROR] Product ID already exists.")
                return False

            # If slot is empty, insert product
            if self.table[slot] is None:
                self.table[slot] = product
                if display:
                    print("\n[SUCCESS] Product added to inventory!")
                    print(f"{self.table[slot]} stored at {slot}.")
                return True

        # If the table is full
        if display:
            print("[ERROR] Hash table is full. Cannot add product.")
        return False

    #Write search with probing.
    def search(self, product_id):
        index = self.hash_function(product_id)

        for i in range(self.size):
            slot = (index + i) % self.size
            if self.table[slot] is None:
                return None
            if self.table[slot].product_id == product_id:
                return self.table[slot]
        return None


#array search
def array_search(arr, product_id):
    # Sequential Search
    for product in arr:
        if product.product_id == product_id:
            return product
    return None


#add product to both data structures
def add_product(ht, arr, product):
    # Insert into Hash Table
    inserted = ht.insert(product)

    # Insert into Array only if successful
    if inserted:
        arr.append(product)


# Display all products
def display_products(arr):
    if not arr:
        print("\n[NOTICE] Inventory is empty.")
        return

    print("\n********** PHARMACY INVENTORY **********")
    for product in arr:
        print(product)
    print("*" * 42)


# Performance experiment: hash table vs one-dimensional array
def performance_experiment():
    print("\n********** PERFORMANCE EXPERIMENT **********")
    print(f"{'Records':>10} | {'Hash Table (s)':>16} | "
          f"{'Array (s)':>14} | {'Speed-up':>10}")
    print("-" * 62)

    dataset_sizes = DATASET_SIZES
    num_searches = NUM_SEARCHES

    for n in dataset_sizes:
        # Load factor kept at about 50%
        table = HashTable(n * 2 + 1)
        array = []

        # Random unique IDs so collisions and probing actually happen
        ids = random.sample(range(1, n * 10), n)

        # Insert the same records into both structures
        for pid in ids:
            product = Product(pid, f"Lozenges {pid}", 10.00, 50)
            inserted = table.insert(product, display=False)
            if inserted:
                array.append(product)

        # Same random (successful) search targets for both structures
        targets = [random.choice(ids) for _ in range(num_searches)]

        # Time the hash table
        start = time.perf_counter()
        for target in targets:
            table.search(target)
        hash_time = time.perf_counter() - start

        # Time the array
        start = time.perf_counter()
        for target in targets:
            array_search(array, target)
        array_time = time.perf_counter() - start

        # Average time per search
        hash_average = hash_time / num_searches
        array_average = array_time / num_searches

        if hash_average > 0:
            speed_up = array_average / hash_average
        else:
            speed_up = 0

        print(f"{n:>10} | {hash_average:>16.9f} | "
              f"{array_average:>14.9f} | {speed_up:>9.2f}x")

    print(f"\nEach value is the average of {num_searches} random searches.")
    print("Experiment completed successfully!")


#Menu
def main():
    ht = HashTable(TABLE_SIZE)  # Create Hash Table
    products_array = []  #create array

    # Pre-defined records
    sample_products = [
        Product(1042, "Aspirin 500mg", 5.90, 120),
        Product(1007, "Vitamin C 1000mg", 12.50, 80),
        Product(1062, "Cough Syrup", 15.00, 30),
        Product(1092, "Magnesium Glycinate 250mg", 75.00, 30),
        Product(1023, "Face Mask", 20.00, 100),
        Product(1061, "Vitamin D 1000mg", 30.00, 50),
        Product(1078, "Antiseptic Cream", 27.00, 80),
        Product(1015, "Digital Thermometer", 18.90, 30)
    ]

    # Insert sample products into both data structures
    for product in sample_products:
        add_product(ht, products_array, product)

    while True:
        print("\n****************************************")
        print("       PHARMACY STOCK MANAGEMENT")
        print("****************************************")
        print("[1] Add New Product")
        print("[2] Find Product")
        print("[3] View All Inventory")
        print("[4] Run Search Performance Test")
        print("[5] Close Application")
        print("----------------------------------------")

        choice = input("Enter choice: ")

        if choice == "1":
            try:
                pid = int(input("Enter Product ID: "))
                name = input("Enter Product Name: ")
                price = float(input("Enter Price: "))
                qty = int(input("Enter Stock Quantity: "))

                # validate input
                if pid <= 0:
                    print("[ERROR] Product ID must be a positive number.")
                    continue
                if name.strip() == "":
                    print("[ERROR] Product name cannot be empty.")
                    continue
                if price < 0 or qty < 0:
                    print("[ERROR] Price and quantity cannot be negative.")
                    continue

                # Create Product object
                product = Product(pid, name, price, qty)

                # Insert into both structures
                add_product(ht, products_array, product)

            except ValueError:
                print("[ERROR] Invalid input. Please enter the correct data type.")

        elif choice == "2":
            try:
                pid = int(input("Enter Product ID to search: "))

                #Search using Hash Table
                start = time.perf_counter()
                result = ht.search(pid)
                hash_time = time.perf_counter() - start

                #search using array
                start = time.perf_counter()
                array_result = array_search(products_array, pid)
                array_time = time.perf_counter() - start

                # Check whether both search results match
                if result == array_result:
                    print("\nBoth search results match.")
                else:
                    print("\n[WARNING] Search results do not match.")

                # Display Search Result
                if result is not None:
                    print("\n[SUCCESS] Matching product found!")
                    print("----------------------------------------")
                    print(result)
                    print("----------------------------------------")
                else:
                    print("\n[NOTICE] No matching product exists in the inventory.")

                # Display Search Time
                print("\n********** SEARCH PERFORMANCE **********")
                print(f"Hash Table execution time : {hash_time:.9f} seconds")
                print(f"Array execution time      : {array_time:.9f} seconds")
                print("*" * 42)

            except ValueError:
                print("[ERROR] Invalid Product ID. Please enter a number.")

        elif choice == "3":
            display_products(products_array)

        elif choice == "4":
            performance_experiment()

        elif choice == "5":
            print("\nApplication closed successfully. Thank you!")
            break

        else:
            print("[ERROR] Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
