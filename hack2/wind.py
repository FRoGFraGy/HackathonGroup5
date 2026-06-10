# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 00:56:26 2026

@author: aunch
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. โหลดข้อมูลและจัดการชนิดตัวแปรตามข้อเท็จจริง
df = pd.read_csv('Export.csv', skiprows=1)
df['Time'] = pd.to_datetime(df['Time'])

for col in ['Wind Direction', 'Wind Speed']:
    df[col] = df[col].astype(str).str.replace(',', '')
    df[col] = pd.to_numeric(df[col], errors='coerce')

df_wind = df.dropna(subset=['Wind Direction', 'Wind Speed']).copy()
df_wind['Month'] = df_wind['Time'].dt.strftime('%Y-%m')
months = sorted(df_wind['Month'].unique())

# 2. สร้างโครงสร้าง Layout ตาราง 2x2
fig, axes = plt.subplots(
    2, 2, 
    figsize=(11, 11), 
    subplot_kw={'projection': 'polar'}
)
axes = axes.flatten()

max_speed = df_wind['Wind Speed'].max()
yticks_inside = list(range(5, int(max_speed) + 5, 5))

# 3. วนลูปสร้างกราฟแต่ละเดือน
for i, month in enumerate(months):
    ax = axes[i]
    month_data = df_wind[df_wind['Month'] == month]
    
    theta_radians = np.radians(month_data['Wind Direction'])
    speed = month_data['Wind Speed']
    
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    
    # ดีไซน์พื้นหลังมินิมอล
    ax.set_facecolor('#f8fafc')
    ax.grid(True, color='#cbd5e1', linestyle=':', linewidth=1)
    
    # พลอตจุดข้อมูล
    ax.scatter(
        theta_radians, 
        speed, 
        color='#007a87', 
        alpha=0.2, 
        s=12, 
        edgecolor='none'
    )
    
    # จัดการแกน Y (ความเร็วลม) เฉียงไปที่ 45 องศา (ทิศ NE) เพื่อไม่ให้ทับแนวแกนดิ่ง
    ax.set_ylim(0, max_speed)
    ax.set_yticks(yticks_inside)
    ax.set_yticklabels([f"{y} m/s" for y in yticks_inside], fontsize=9, color='#64748b')
    ax.set_rlabel_position(45) 
    
    # จัดการข้อความทิศทาง (แกน X)
    ax.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])
    
    # ปรับระยะห่างตัวอักษรทิศรอบวงกลมให้พอดี (ออกห่างจากขอบวงกลมพองาม ไม่ชิดเกินไป)
    ax.tick_params(axis='x', which='major', pad=15, labelsize=11, labelcolor='#1e293b')
    
    # 🛠️ แก้ไขหลัก: ดันชื่อเดือนขึ้นไปด้านบนเหนือกราฟอย่างเด็ดขาดด้วยค่า y=1.18 
    # ทำให้ตัว N ด้านบนสุดมีพื้นที่ว่างลอยตัวอย่างอิสระ ไม่ชนกับข้อความใดๆ
    ax.set_title(f'Month: {month}', fontsize=13, fontweight='bold', color='#0f172a', y=1.18)

# ซ่อนช่องย่อยที่เหลือ (ถ้าจำนวนเดือนไม่ครบ 4 ช่อง)
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

# หัวข้อใหญ่ของหน้ารายงาน
plt.suptitle('Wind Direction & Speed Environmental Analysis', fontsize=16, fontweight='bold', color='#0f172a', y=0.98)

# 🛠️ ป้องกันตัว N และชื่อเรื่องหลุดขอบจอ หรือชนกันระหว่างแถวบน-แถวล่าง
plt.subplots_adjust(
    top=0.88,      # เว้นพื้นที่ด้านบนสุดให้หัวข้อใหญ่
    bottom=0.05,   # เว้นพื้นที่ด้านล่างสุด
    left=0.05,     # เว้นขอบซ้าย
    right=0.95,    # เว้นขอบขวา
    hspace=0.45,   # เพิ่มช่องว่างแนวตั้งระหว่างกราฟแถวบนและแถวล่างอย่างเต็มที่
    wspace=0.35    # เพิ่มช่องว่างแนวนอนระหว่างกราฟซ้ายและขวา
)

plt.show()