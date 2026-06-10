import csv
from collections import defaultdict

# ----- ตั้งค่า -----
INPUT_FILE = "input.csv"        # ชื่อไฟล์ CSV ที่ต้องการอ่าน
OUTPUT_FILE = "Pattern.txt"     # ชื่อไฟล์ผลลัพธ์
TARGET_STATUS = {"400", "401", "403", "500", "502"}
HAS_HEADER = False              # ถ้า CSV มีแถวหัวตาราง ให้เปลี่ยนเป็น True
# -------------------

groups = defaultdict(list)

with open(INPUT_FILE, newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    if HAS_HEADER:
        next(reader, None)  # ข้ามแถวหัวตาราง

    for row in reader:
        if len(row) < 5:
            continue  # ข้ามแถวที่คอลัมน์ไม่ครบ

        status = row[4].strip()
        if status in TARGET_STATUS:
            ip = row[1].strip()           # index 1
            timestamp = row[0].strip()    # index 0
            path = row[3].strip()         # index 3
            groups[ip].append(f"{timestamp}, {path}")

# เขียนผลลัพธ์: IP เป็นหัว แล้วตามด้วยรายการด้านล่าง
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for ip, entries in groups.items():
        f.write(ip + "\n")
        for entry in entries:
            f.write(entry + "\n")
        f.write("\n")  # เว้นบรรทัดคั่นระหว่างแต่ละ IP

print(f"เสร็จแล้ว: พบ {sum(len(v) for v in groups.values())} แถว "
      f"จาก {len(groups)} IP -> บันทึกที่ {OUTPUT_FILE}")