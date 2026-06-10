# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 16:51:08 2026

@author: aunch
"""

import pandas as pd
import matplotlib.pyplot as plt

# 1. โหลดข้อมูลและเตรียมข้อมูลเบื้องต้น
# ใช้ skiprows=1 เพื่อข้ามบรรทัดแรก (sep=,)
df = pd.read_csv('Export.csv', skiprows=1)

# แปลงคอลัมน์ Time ให้เป็นรูปแบบ Datetime และลบแถวที่ไม่มีข้อมูลเวลา
df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
df = df.dropna(subset=['Time']) 

# แปลงคอลัมน์ที่เกี่ยวข้องให้เป็นตัวเลข (Numeric)
cols_to_numeric = ['D/T', 'Wind Direction', 'Wind Speed', 'Temperature', 'Relative Humidity', 'PM 2.5', 'Atmospheric Pressure']
for col in cols_to_numeric:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# กำหนดเกณฑ์ D/T ที่ถือว่ากลิ่นแรง (เช่น >= 5.0) เพื่อใช้แยกกลุ่มข้อมูล
high_dt_threshold = 5.0
high_dt = df[df['D/T'] >= high_dt_threshold]
low_dt = df[df['D/T'] < high_dt_threshold]


# ==========================================
# กราฟที่ 1: การกระจายตัวของทิศทางลม (Wind Direction Distribution)
# เปรียบเทียบช่วงที่กลิ่นแรง vs กลิ่นเบาบาง
# ==========================================
plt.figure(figsize=(10, 5))
plt.hist(high_dt['Wind Direction'].dropna(), bins=36, alpha=0.6, color='red', label='High D/T (>= 5.0)', density=True)
plt.hist(low_dt['Wind Direction'].dropna(), bins=36, alpha=0.4, color='blue', label='Low D/T (< 5.0)', density=True)

plt.legend()
plt.title('Wind Direction Distribution (High vs Low D/T)')
plt.xlabel('Wind Direction (Degrees)')
plt.ylabel('Density')
plt.grid(axis='y', alpha=0.5)
plt.show()


# ==========================================
# กราฟที่ 2: แนวโน้มระดับความเข้มกลิ่นเฉลี่ยรายวัน (Daily Average Trend)
# ==========================================
plt.figure(figsize=(15, 6))

# จัดกลุ่มข้อมูลตามวัน (Daily) และหาค่าเฉลี่ยของ D/T
df_resampled = df.set_index('Time').resample('D')['D/T'].mean()

# พล็อตกราฟเส้น
plt.plot(df_resampled.index, df_resampled.values, marker='o', color='teal', linewidth=2)

plt.title('Daily Average Odor Intensity (D/T)')
plt.ylabel('Average D/T')
plt.xlabel('Date')
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(rotation=45) # เอียงตัวหนังสือแกน X เพื่อให้อ่านง่ายขึ้น
plt.tight_layout() # จัดระเบียบขอบกราฟไม่ให้ข้อความตกขอบ
plt.show()