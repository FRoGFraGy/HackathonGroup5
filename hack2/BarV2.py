# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 19:40:27 2026

@author: aunch
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches

# 1. โหลดข้อมูลจริงจากไฟล์ CSV (ข้ามบรรทัดแรกที่เป็น sep=,)
df = pd.read_csv('Export.csv', skiprows=1)

# แปลงคอลัมน์เวลาให้เป็นรูปแบบเดทไทม์ที่ระบบเข้าใจ
df['Time'] = pd.to_datetime(df['Time'])

# 2. ยุบรวมข้อมูลรายนาทีให้เป็น "ค่าเฉลี่ยรายวัน" (Daily Average) เพื่อความสบายตาและเห็นภาพรวมครบทุกวัน
df_daily = df.groupby(df['Time'].dt.date)['D/T'].mean().reset_index()
df_daily.columns = ['Date', 'Value']
df_daily['Date'] = pd.to_datetime(df_daily['Date'])

# 3. กำหนดเกณฑ์ (Threshold) และชุดสีมินิมอลพาสเทลเพื่อความสบายตา
threshold = 2.0          # เกณฑ์ความเข้มข้นของกลิ่น (ปรับเปลี่ยนตัวเลขนี้ได้ตามต้องการ)
color_low = '#84B4D7'   # สีฟ้าพาสเทล (กลิ่นน้อย / ปกติ)
color_high = '#E98080'  # สีแดงโรสพาสเทล (กลิ่นมาก / เหม็น)
bg_color = '#FDFDFD'    # สีพื้นหลังขาวนวล (ช่วยลดความจ้าของหน้าจอ)
text_color = '#333333'  # สีตัวอักษรเทาเข้ม (นุ่มนวลกว่าสีดำสนิท)

# คำนวณสีแท่งกราฟโดยอิงจากความสูงจริง (Value) ของวันนั้นๆ โดยตรง ป้องกันปัญหาสีไม่ตรงกับความสูง
colors = [color_high if val >= threshold else color_low for val in df_daily['Value']]

# 4. ตั้งค่าหน้ากระดาษและดีไซน์แบบ Minimal
fig = plt.figure(figsize=(16, 6), facecolor=bg_color)
ax = plt.subplot(111, facecolor=bg_color)

# วาดกราฟแท่ง (width=0.75 เผื่อช่องไฟเล็กน้อยให้ดูโปร่ง โล่ง ไม่เบียดแน่น)
bars = ax.bar(df_daily['Date'], df_daily['Value'], color=colors, width=0.75, alpha=0.9, edgecolor='none')

# ลากเส้นประสีเทาบอกเกณฑ์ Threshold ช่วยให้กวาดสายตามองเห็นวันที่มีปัญหากลิ่นได้ทันที
ax.axhline(y=threshold, color='#BBBBBB', linestyle='--', linewidth=1.2, alpha=0.6)

# 5. จัดการแกน X ให้แสดงผลครบทุกเดือนอย่างถูกต้อง (เริ่มตั้งแต่ต้นเดือน ก.พ. - สิ้นเดือน พ.ค.)
ax.set_xlim(pd.Timestamp('2026-02-01'), pd.Timestamp('2026-05-31'))
ax.xaxis.set_major_locator(mdates.MonthLocator())          # มาร์กแกนหลักที่จุดเริ่มต้นของทุกเดือน
ax.xaxis.set_major_formatter(mdates.DateFormatter('%B %Y')) # รูปแบบชื่อเดือนภาษาอังกฤษตัวเต็มและปี ค.ศ.
ax.xaxis.set_minor_locator(mdates.DayLocator(interval=1))   # มาร์กขีดสเกลย่อยรายวันด้านล่างแกน

# 6. ลบขอบเส้นด้านบนและขวาออก เพื่อให้กราฟดูคลีน ไม่กระด้าง
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#E0E0E0')
ax.spines['bottom'].set_color('#E0E0E0')

# เส้นกริดแนวนอนแบบจางมากๆ ไม่แย่งสายตาข้อมูล
ax.grid(axis='y', linestyle='-', linewidth=0.5, color='#EAEAEA', zorder=0)
ax.set_axisbelow(True)
ax.tick_params(colors=text_color, labelsize=10)

# 7. สร้างกล่องคำอธิบายสี (Legend) สไตล์เรียบหรู
legend_patches = [
    mpatches.Patch(color=color_low, label=f'Low Odor (< {threshold} D/T)'),
    mpatches.Patch(color=color_high, label=f'High Odor (>= {threshold} D/T)')
]
ax.legend(handles=legend_patches, loc='upper right', frameon=True, 
          facecolor=bg_color, edgecolor='#EAEAEA', fontsize=10, labelcolor=text_color)

# ตั้งชื่อกราฟและป้ายแกน Y
plt.title('Daily Odor Concentration (D/T) - Real Data Analysis', fontsize=15, fontweight='bold', color=text_color, pad=20)
plt.ylabel('Average D/T Value', fontsize=11, color=text_color, labelpad=10)

plt.tight_layout()
plt.show()