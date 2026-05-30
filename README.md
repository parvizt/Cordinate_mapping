# 🌍 Coordinate Mapping — Well UTM ↔ Lat/Lon

<div align="center">
  
  **تبدیل هوشمند مختصات جغرافیایی برای مهندسان و ژئولوژیست‌ها**
  
  [![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
  [![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange?logo=python)](https://docs.python.org/3/library/tkinter.html)
  [![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)
  [![GitHub Stars](https://img.shields.io/github/stars/parvizt/Cordinate_mapping?style=social)](https://github.com/parvizt/Cordinate_mapping)
  
</div>

---

## 📋 فهرست مطالب
- [🎯 ویژگی‌های کلیدی](#-ویژگیهای-کلیدی)
- [🚀 شروع سریع](#-شروع-سریع)
- [💻 نحوه استفاده](#-نحوه-استفاده)
- [📦 صادرات داده‌ها](#-صادرات-دادهها)
- [🗺️ یکپارچگی نقشه](#-یکپارچگی-نقشه)
- [📋 الزامات سیستم](#-الزامات-سیستم)
- [👨‍💻 درباره](#-درباره)

---

## 🎯 ویژگی‌های کلیدی

✅ **تبدیل دقیق مختصات:**
- UTM ↔ Latitude/Longitude
- فرمت‌های مختلف: DMS (Degree, Minute, Second) و Decimal
- سیستم‌های مختصات کامل

✅ **رابط کاربری دسکتاپی:**
- Tkinter مدرن و کاربرپسند
- مدیریت چندین چاه‌ (Well)
- ویرایش و حذف فوری

✅ **یکپارچگی Google Maps:**
- نمایش مختصات بر روی نقشه
- لینک‌های مستقیم به Google Maps

✅ **صادرات چند‌فرمتی:**
- 📊 CSV (برای Excel)
- 📄 JSON (برای API‌ها)
- 🗺️ KML (برای Google Earth)

✅ **ذخیره‌سازی دائمی:**
- داده‌های خودکار ذخیره
- بازیابی سریع پروژه‌های قدیمی

---

## 📸 نمونه‌های صفحه

<img width="1362" height="1116" alt="نمونه 1" src="https://github.com/user-attachments/assets/185b8ca7-a1e7-40ae-8ce7-7806dd6dea5c" />

---

## 🚀 شروع سریع

### 📥 نصب

**پیش‌نیازها:**
```bash
Python 3.9+
```

**گام 1: Clone ریپوزیتوری**
```bash
git clone https://github.com/parvizt/Cordinate_mapping.git
cd Cordinate_mapping
```

**گام 2: نصب وابستگی‌ها**
```bash
pip install pyproj
```

**گام 3: اجرای برنامه**
```bash
python well_coordinate_mapping.py
```

---

## 💻 نحوه استفاده

### 1️⃣ **تبدیل مختصات**

**فرمت‌های ورودی پذیرفته‌شده:**

| فرمت | مثال |
|------|------|
| **DMS** | `30°57'25.2"N 49°06'37.4"E` |
| **Decimal** | `30.957, 49.11` |
| **فاصله‌دار** | `30.957 49.11` |

### 2️⃣ **تبدیل UTM**
```
Easting:  500000
Northing: 3420000
Zone:     39N
```

### 3️⃣ **نمایش بر روی نقشه** 🗺️
- کپی لینک Google Maps
- نمایش مسیر (Route)
- باز کردن تمام نقاط

---

## 📦 صادرات داده‌ها

| فرمت | کاربرد | 💾 |
|------|--------|-----|
| **CSV** | Excel، Power BI، پایگاه‌های داده | ✅ |
| **JSON** | تبادل داده، API‌ها | ✅ |
| **KML** | Google Earth، نقشه‌گری | ✅ |

---

## 🗺️ ویژگی‌های نقشه‌ای

```
✓ یکپارچگی Google Maps
✓ نمایش مختصات بر روی نقشه
✓ لینک‌های مستقیم به نقاط
✓ دسته‌ای در یک نقشه
```

---

## 📋 الزامات سیستم

| موارد | نسخه/وضعیت |
|------|----------|
| Python | 3.9+ ✅ |
| pyproj | latest ✅ |
| Tkinter | built-in ✅ |

---

## 🎨 انتخاب تم‌ها

برنامه چندین تم ارائه می‌دهد:
- 🎨 Modern
- 📘 Classic
- 💓 Girly
- 💼 Formal

---

## 📝 نمونه داده

```json
{
  "wells": [
    {
      "name": "Well-01",
      "latitude": 30.957,
      "longitude": 49.11,
      "utm_zone": "39N",
      "easting": 500000,
      "northing": 3420000
    }
  ]
}
```

---

## 🔧 ویژگی‌های تکنیکی

- 🖥️ **GUI:** Tkinter
- 📍 **مختصات:** pyproj (WGS84)
- 📊 **داده‌ها:** JSON/CSV
- ⚡ **بدون اینترنت:** کار آفلاین
- 🎯 **سبک:** مناسب برای لپ‌تاپ میدانی

---

## 🤝 مشارکت

ما از کمک‌های شما استقبال می‌کنیم! 💪

**برای مشارکت:**
```bash
1. Fork کنید 🍴
2. Branch جدید بسازید
3. تغییرات را commit کنید
4. Pull Request بسازید
```

---

## 📄 لایسنس

**Apache License 2.0** — برای استفاده و توسعه آزادانه

---

## 👨‍💻 درباره

**نویسنده:** پرویز تاجداری
- 🔬 ژئولوژیست | توسعه‌دهنده Python | ابزارهای جغرافیایی
- 🔗 [GitHub](https://github.com/parvizt)

---

## 🚀 بهبود‌های آینده

- 🗂️ صادرات DXF
- 📥 واردات دسته‌ای از CSV
- 🗺️ نمایش نقشه درون برنامه
- 🌊 پشتیبانی از مسیر چاه

---

<div align="center">

⭐ **اگر این پروژه مفید بود، لطفاً ستاره دهید!**

![GitHub last commit](https://img.shields.io/github/last-commit/parvizt/Cordinate_mapping?style=flat-square)

</div>
