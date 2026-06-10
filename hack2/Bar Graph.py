# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 16:55:45 2026

@author: aunch
"""

import pandas as pd
import matplotlib.pyplot as plt

# 1. โหลดข้อมูลและแปลงเวลา
df = pd.read_csv('Export.csv', skiprows=1)
df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
df = df.dropna(subset=['Time'])
df['D/T'] = pd.to_numeric(df['D/T'], errors='coerce')

# 2. สร้างคอลัมน์ 'Hour' เพื่อดึงเฉพาะ "ชั่วโมง" ออกมา (0-23)
df['Hour'] = df['Time'].dt.hour

# 3. จัดกลุ่มตามชั่วโมงและหาค่าเฉลี่ยของระดับกลิ่น (D/T)
hourly_avg = df.groupby('Hour')['D/T'].mean()

# ==========================================
# 4. พล็อตกราฟแท่ง (Bar Chart)
# ==========================================
plt.figure(figsize=(12, 6))

# สร้างกราฟแท่ง กำหนดสีพื้นฐานเป็นสีฟ้า
bars = plt.bar(hourly_avg.index, hourly_avg.values, color='skyblue', edgecolor='black', alpha=0.8)

# ไฮไลท์สีแดงตรงช่วงเวลาที่กลิ่นแรงที่สุด (ชั่วโมงที่ 6, 7 และ 8) เพื่อให้เห็นชัดๆ
for i in [6, 7, 8]:
    bars[i].set_color('salmon')
    bars[i].set_edgecolor('black')

# ตกแต่งกราฟ
plt.title('Average Odor Intensity (D/T) by Hour of Day\n', fontsize=16, pad=15)
plt.xlabel('Hour of the Day (00:00 - 23:00)', fontsize=12)
plt.ylabel('Average D/T ', fontsize=12)

# บังคับให้แกน X แสดงตัวเลขชั่วโมงครบทุกตัว (0 ถึง 23)
plt.xticks(hourly_avg.index)
plt.grid(axis='y', linestyle='--', alpha=0.5)

# เพิ่มตัวเลขกำกับไว้บนหัวกราฟแท่งแต่ละแท่ง
for bar in bars:
    yval = bar.get_height()
    # เช็คว่าถ้าไม่ใช่ค่าว่าง (NaN) ให้แสดงตัวเลข ทศนิยม 2 ตำแหน่ง
    if pd.notna(yval):
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.02, f'{yval:.2f}', 
                 ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()