import os
import csv

# Paths
training_folder = "TrainingImage"
csv_folder = "StudentDetails"
csv_file = os.path.join(csv_folder, "StudentDetails.csv")

# Make sure folder exists
if not os.path.exists(csv_folder):
    os.makedirs(csv_folder)

# Columns for CSV
columns = ['SERIAL NO.', '', 'ID', '', 'NAME']

# Collect data from filenames
data = []
serial_set = set()  # To avoid duplicate SERIAL NO. entries

for filename in os.listdir(training_folder):
    if filename.endswith(".jpg"):
        try:
            # Filename pattern: Name.Serial.ID.Sample.jpg
            parts = filename.split(".")
            name = parts[0]
            serial = int(parts[1])
            student_id = parts[2]

            # Avoid duplicate SERIAL NO. entries
            if serial not in serial_set:
                serial_set.add(serial)
                data.append([serial, '', student_id, '', name])

        except Exception as e:
            print(f"Skipping file {filename}: {e}")

# Write CSV
with open(csv_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(columns)
    writer.writerows(data)

print(f"[INFO] StudentDetails.csv created with {len(data)} entries.")
