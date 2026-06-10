#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
guess_name.py
-------------
อ่าน log ดิบ (Pattern.txt) แล้วถอด "ข้อความที่ซ่อนไว้" ออกมา
หลักการ: ในแต่ละ IP เรียง request ตามเวลา (timestamp) แล้วดึงตัวอักษร
สุดท้ายของ path (ถ้าลงท้าย .html ให้เอาตัวก่อน .html) จากนั้นยุบตัวที่
ติดกัน (เช่น NNNN -> N) ผลที่ได้จะกลายเป็นประโยค โดย '_' = ช่องว่าง

ฟอร์แมต log ดิบ:
    209.103.8.44                      <- บรรทัด IP เปล่าๆ
    2024-06-16 10:25:29, /indexN.html <- เวลา, /path
    ...

วิธีใช้:
    python3 guess_name.py Pattern.txt
ถ้าไม่ใส่ argument จะหาไฟล์ชื่อ Pattern.txt ในโฟลเดอร์ปัจจุบัน
"""

import os
import re
import sys

IP_RE = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")


def decode(path_file: str):
    """คืนค่า list ของ (ip, ข้อความที่ถอดได้) เรียงตามลำดับที่เจอในไฟล์"""
    results = []
    current_ip = None
    last_char = None          # ตัวล่าสุด ใช้ยุบตัวติดกันแบบ streaming
    message_parts = []        # ตัวอักษรของ IP ปัจจุบัน

    def flush():
        if current_ip is not None:
            results.append((current_ip, "".join(message_parts)))

    with open(path_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()          # ตัด \r\n และช่องว่างหัวท้าย
            if not line:
                continue

            if IP_RE.match(line):        # เจอ IP ใหม่
                flush()                  # เก็บผลของ IP ก่อนหน้า
                current_ip = line
                message_parts = []
                last_char = None
                continue

            if "," in line:              # บรรทัด "เวลา, /path"
                path = line.split(",", 1)[1].strip()
                name = path[:-5] if path.endswith(".html") else path
                ch = name[-1]
                if ch != last_char:      # ยุบเฉพาะตัวที่ติดกัน
                    message_parts.append(ch)
                    last_char = ch

    flush()                              # IP สุดท้าย
    return results


def guess_signature(message: str):
    """เดา 'ชื่อ/ลายเซ็น' ของผู้โจมตีจากข้อความที่ถอดได้
    ข้อความวนซ้ำเป็นลูป: NEXUS_..._IT_WAS_ME_<ชื่อ>NEXUS_...
    ชื่ออยู่หลัง '_ME_' และอยู่ก่อนคำว่า NEXUS ที่วนกลับมา
    """
    m = re.search(r"_ME_([A-Z]+?)NEXUS", message)
    if not m:
        return None
    name = m.group(1)
    # ตัวสุดท้ายของชื่อถ้าเป็น N จะถูกยุบรวมกับ N ของ NEXUS (ยุบตัวติดกัน)
    # ข้อความ loop ขึ้นต้นด้วย 'N' เสมอ จึงเติม N กลับถ้าจำเป็น
    if not name.endswith("N"):
        name += "N"
    return name


def main():
    path_file = sys.argv[1] if len(sys.argv) > 1 else "Pattern.txt"
    out_file = sys.argv[2] if len(sys.argv) > 2 else "name_2.txt"

    if not os.path.exists(path_file):
        print(f"[ผิดพลาด] หาไฟล์ไม่เจอ: {path_file}")
        print(f"          โฟลเดอร์ปัจจุบัน: {os.getcwd()}")
        print(f"          ไฟล์ในโฟลเดอร์นี้: {os.listdir('.')}")
        sys.exit(1)

    results = decode(path_file)

    # เดาชื่อจาก IP แรกที่ถอดได้
    guessed = None
    for _ip, msg in results:
        guessed = guess_signature(msg)
        if guessed:
            break

    lines_out = [f"จำนวน IP ที่เจอ: {len(results)}", ""]
    for ip, msg in results:
        lines_out.append(f"IP: {ip}")
        lines_out.append(msg)
        lines_out.append("")
    text = "\n".join(lines_out)

    print(text)
    print("=" * 50)
    print(f">> ชื่อผู้โจมตี (ลายเซ็น): {guessed}")
    print("=" * 50)

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(text)
        f.write(f"\n==================================================\n")
        f.write(f">> ชื่อผู้โจมตี (ลายเซ็น): {guessed}\n")
    print(f">> บันทึกผลลงไฟล์: {out_file}")


if __name__ == "__main__":
    main()