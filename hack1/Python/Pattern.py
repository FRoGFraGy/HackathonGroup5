import csv
from collections import defaultdict, Counter
from datetime import datetime
# ----- ตั้งค่า -----
INPUT_FILE = "cart_web.csv"        # ชื่อไฟล์ CSV ที่ต้องการอ่าน
OUTPUT_FILE = "Pattern.txt"     # ชื่อไฟล์ผลลัพธ์
SUMMARY_FILE = "summary.txt"    # ชื่อไฟล์สรุป
TARGET_STATUS = {"400", "401", "403", "500", "502", "503", "504", "521"}
HAS_HEADER = False              # ถ้า CSV มีแถวหัวตาราง ให้เปลี่ยนเป็น True
# -------------------
groups = defaultdict(list)
summary = {}   # ip -> สถิติสรุป
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

            # --- เก็บสถิติสำหรับ summary ---
            s = summary.get(ip)
            if s is None:
                s = summary[ip] = {"count": 0, "paths": Counter(),
                                   "hours": Counter(), "first": None, "last": None}
            s["count"] += 1
            s["paths"][path] += 1
            try:
                dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                s["hours"][dt.hour] += 1
                if s["first"] is None or dt < s["first"]:
                    s["first"] = dt
                if s["last"] is None or dt > s["last"]:
                    s["last"] = dt
            except ValueError:
                pass
# เขียนผลลัพธ์: IP เป็นหัว แล้วตามด้วยรายการด้านล่าง
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for ip, entries in groups.items():
        f.write(ip + "\n")
        for entry in entries:
            f.write(entry + "\n")
        f.write("\n")  # เว้นบรรทัดคั่นระหว่างแต่ละ IP

# เขียนไฟล์สรุป: เรียง IP จากโจมตีมากสุดลงไป
with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
    f.write("=" * 55 + "\n")
    f.write(f"สรุปการโจมตี | รวม {len(summary)} IP | "
            f"{sum(s['count'] for s in summary.values())} ครั้ง\n")
    f.write("=" * 55 + "\n\n")
    for ip in sorted(summary, key=lambda k: summary[k]["count"], reverse=True):
        s = summary[ip]
        f.write(f"IP: {ip}\n")
        f.write(f"  จำนวนครั้ง : {s['count']}\n")
        f.write(f"  ช่วงวันที่  : {s['first']}  ถึง  {s['last']}\n")
        hours_txt = ", ".join(f"{h:02d}:00 น. ({c})" for h, c in s["hours"].most_common(5))
        f.write(f"  ชม.ที่บ่อย : {hours_txt}\n")
        f.write(f"  path ที่ใช้ ({len(s['paths'])} แบบ):\n")
        for path, c in s["paths"].most_common():
            f.write(f"      {path}  ->  {c} ครั้ง\n")
        f.write("\n")

print(f"เสร็จแล้ว: พบ {sum(len(v) for v in groups.values())} แถว "
      f"จาก {len(groups)} IP")
print(f"  -> {OUTPUT_FILE}")
print(f"  -> {SUMMARY_FILE}")