import csv

# Generate the values
values = []
increase = True
counter = 0

for _ in range(5000):
    values.append(counter)
    if increase:
        counter += 1
        if counter == 500:
            increase = False
    else:
        counter -= 1
        if counter == 0:
            increase = True

# Write values to heart2.csv
with open("heart2.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["intensity"])
    for val in values:
        writer.writerow([val])

print("heart2.csv has been generated!")