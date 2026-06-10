#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_pattern.py
------------------
ดึง "ตัวอักษรสุดท้าย" ของชื่อ path ในแต่ละ IP จากไฟล์ summary.txt
- path เรียงตามจำนวนครั้ง (มาก -> น้อย) อยู่แล้วในไฟล์
- ถ้า path ลงท้ายด้วย .html ให้เอาตัวก่อน .html
- '_' ก็นับ เพราะเป็นตัวสุดท้ายของ path ฐาน (เช่น /cart_, /index_.html)
- ตัดตัวซ้ำออก คงลำดับตามความถี่

วิธีใช้:
    python3 extract_pattern.py summary.txt          # เซฟลง name.txt อัตโนมัติ
    python3 extract_pattern.py summary.txt out.txt   # กำหนดชื่อไฟล์ผลลัพธ์เอง
ถ้าไม่ใส่ argument จะใช้ไฟล์ชื่อ summary.txt และเซฟผลเป็น name.txt
"""

import re
import sys


def extract(path_file: str):
    """อ่านไฟล์ แล้วคืนค่า (ลำดับ IP, dict: ip -> ลำดับตัวอักษรไม่ซ้ำ)"""
    with open(path_file, encoding="utf-8") as f:
        lines = f.readlines()

    ip_order = []          # เก็บลำดับ IP ตามที่เจอในไฟล์
    chars_by_ip = {}       # ip -> list ตัวอักษรสุดท้าย (ตามลำดับความถี่)
    current_ip = None

    for line in lines:
        # บรรทัดหัว IP เช่น "IP: 197.82.237.190"
        m_ip = re.match(r"\s*IP:\s*([\d.]+)", line)
        if m_ip:
            current_ip = m_ip.group(1)
            ip_order.append(current_ip)
            chars_by_ip[current_ip] = []
            continue

        # บรรทัด path เช่น "    /index_.html  ->  8049 ครั้ง"
        m_path = re.match(r"\s*(/\S+)\s*->", line)
        if m_path and current_ip:
            name = m_path.group(1)
            if name.endswith(".html"):
                name = name[:-5]          # ตัด ".html" ออก
            last_char = name[-1]          # ตัวสุดท้าย ('_' ก็นับ)
            chars_by_ip[current_ip].append(last_char)

    return ip_order, chars_by_ip


def collapse_consecutive(items):
    """ยุบเฉพาะตัวที่ติดกัน (run-length) คงตัวที่กระโดดกลับมาซ้ำไว้
    เช่น  _ _ E E A A R T R O  ->  _ E A R T R O
    """
    out = []
    for c in items:
        if not out or out[-1] != c:
            out.append(c)
    return out


def main():
    path_file = sys.argv[1] if len(sys.argv) > 1 else "pattern.txt"
    out_file = sys.argv[2] if len(sys.argv) > 2 else "name.txt"

    ip_order, chars_by_ip = extract(path_file)

    lines_out = [f"จำนวน IP ที่เจอ: {len(ip_order)}", ""]
    for idx, ip in enumerate(ip_order, start=1):
        pattern = "".join(collapse_consecutive(chars_by_ip[ip]))
        lines_out.append(f"IP: {ip}")
        lines_out.append(pattern)
        lines_out.append("")

    text = "\n".join(lines_out)

    # แสดงบนหน้าจอ
    print(text)

    # เซฟลงไฟล์
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"\n>> บันทึกผลลงไฟล์: {out_file}")


if __name__ == "__main__":
    main()