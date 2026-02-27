# 📂 JSON to CSV Message Exporter

เครื่องมือสำหรับดึงข้อมูลจากฟิลด์ `message` ภายในไฟล์ JSON (Log format) และส่งออกเป็นไฟล์ CSV พร้อมระบบค้นหา keyword แบบอัตโนมัติ เพื่อเช็คว่าเป็นข้อมูลจากเส้นเก่าหรือเส้นใหม่

---

## 🛠 โครงสร้างระบบ (Folder Structure)

จัดเตรียมโฟลเดอร์ให้เป็นระเบียบดังนี้ก่อนใช้งาน:

```
script/
  convert.py        (ไฟล์โปรแกรมหลัก)
  input/            (โฟลเดอร์เก็บไฟล์ JSON ต้นทาง)
  output/           (โฟลเดอร์เก็บไฟล์ CSV ที่ได้)
  result/           (โฟลเดอร์เก็บไฟล์ผลลัพธ์การค้นหา)
  keyword/          (ไฟล์ keyword สำหรับค้นหา)
     new_keyword.json
     old_keyword.json
```

---

## 🚀 วิธีการใช้งาน

### 1. เตรียมไฟล์ JSON

นำไฟล์ `.json` ที่คุณต้องการแปลงไปวางไว้ในโฟลเดอร์ `input/`

รองรับ **หลายไฟล์ JSON** ในการทำงานครั้งเดียว

ตัวอย่าง:

```
input/
  log1.json
  log2.json
  log3.json
```

---

### 2. เตรียมไฟล์ Keyword

ระบบรองรับการค้นหาแบบแบ่งตามกลุ่มหัวข้อ โดยเตรียมไฟล์ในโฟลเดอร์ `keyword/`

ตัวอย่าง `new_keyword.json` หรือ `old_keyword.json`:

```json
{
  "Get Privilege Profile": [
    "loyaltyBalance",
    "getExpiration",
    "loyaltyProgramMember"
  ],
  "Redeem API": [
    "redeemPoint",
    "transactionId"
  ]
}
```

โครงสร้าง:

* key = หัวข้อหลัก
* value = keyword ที่ต้องการค้นหา

---

### 3. รันโปรแกรม

สามารถดับเบิลคลิกที่ไฟล์ `convert.py` หรือใช้คำสั่ง:

```bash
python3 convert.py
```

ระบบจะให้เลือก:

```
เลือก keyword (old / new):
```

---

### 4. ผลลัพธ์

#### 4.1 CSV จาก JSON

ไฟล์ CSV จะถูกสร้างในโฟลเดอร์ `output/`

```
output/
  Profile_Core.csv
  redeem.csv
```

#### 4.2 ผลลัพธ์การค้นหา

ระบบจะค้นหาข้อมูลจาก CSV และสร้างไฟล์สรุปใน `result/`

```
result/
  Get_Privilege_Profile.csv
  Redeem_API.csv
```

ชื่อไฟล์จะมาจากหัวข้อใน keyword

---

## 📝 รายละเอียดการทำงานของระบบค้นหา

* รองรับการค้นหา keyword หลายคำในครั้งเดียว
* ค้นหาแบบไม่สนตัวพิมพ์ใหญ่–เล็ก
* ค้นหาทุกไฟล์ CSV อัตโนมัติ
* แยกผลลัพธ์ตามหัวข้อ
* เหมาะสำหรับเปรียบเทียบระบบ Old vs New

ไฟล์ผลลัพธ์ประกอบด้วย:

| topic | keyword | filename | row_number | message |

---

## 🧾 การจัดการ Log (Handle Log)

### 🔹 No .json file

หากในโฟลเดอร์ `input/` ไม่มีไฟล์ `.json` โปรแกรมจะแจ้งเตือน

### 🔹 Empty Message

หากไฟล์ JSON ไม่มีฟิลด์ `message` โปรแกรมจะแจ้งเตือนและข้ามไฟล์นั้น

### 🔹 Error per file

หากไฟล์ใดเกิดข้อผิดพลาด โปรแกรมจะไม่หยุดทั้งระบบ แต่จะทำงานต่อกับไฟล์อื่น

---

## ⚙️ รูปแบบ JSON ที่รองรับ

```json
{
  "hits": {
    "hits": [
      {
        "_source": {
          "message": "log message here"
        }
      }
    ]
  }
}

```

---

*จัดทำขึ้นเพื่อช่วยให้การดึง Log และตรวจสอบข้อมูลเป็นเรื่องง่ายขึ้น* 🚀
