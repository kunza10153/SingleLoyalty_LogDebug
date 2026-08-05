# 📂 JSON to CSV Log Converter

รวมสคริปต์แปลง log 3 รูปแบบ โดยใช้โฟลเดอร์แยกตามชนิดของ log และสร้าง CSV อัตโนมัติ

---

## 🔧 สคริปต์ที่ใช้

1. `convert__debug_gitbash.py`
   - แปลงไฟล์จากโฟลเดอร์ `json_gitbash`
   - ผลลัพธ์จะเก็บไว้ใน `output_json_gitbash`

2. `convert_debug_athena.py`
   - แปลงไฟล์จากโฟลเดอร์ `json_athena`
   - ผลลัพธ์จะเก็บไว้ใน `output_json_athena`

3. `convert_debug_openseatch.py`
   - แปลงไฟล์จากโฟลเดอร์ `json_openseatch`
   - ผลลัพธ์จะเก็บไว้ใน `output_json_openseatch`
   - มีระบบค้นหา keyword ด้วยไฟล์ `keyword/{old,new}_keyword.json`

---

## 📁 โครงสร้างโฟลเดอร์ปัจจุบัน

```
JSON-to-CSV/
  convert__debug_gitbash.py
  convert_debug_athena.py
  convert_debug_openseatch.py
  json_athena/
  json_gitbash/
  json_openseatch/
  keyword/
    new_keyword.json
    old_keyword.json
  output_json_athena/
  output_json_gitbash/
  output_json_openseatch/
```

---

## 🚀 วิธีใช้งาน

1. วางไฟล์ `.json` ต้นทางไว้ในโฟลเดอร์ตามสคริปต์ที่ต้องการ
   - ใช้ `json_gitbash/` กับ `convert__debug_gitbash.py`
   - ใช้ `json_athena/` กับ `convert_debug_athena.py`
   - ใช้ `json_openseatch/` กับ `convert_debug_openseatch.py`

2. รันสคริปต์ด้วยคำสั่ง

```bash
python3 convert__debug_gitbash.py
python3 convert_debug_athena.py
python3 convert_debug_openseatch.py
```

3. ถ้าใช้ `convert_debug_openseatch.py` จะมีขั้นตอนค้นหา keyword ด้วย

```bash
python3 convert_debug_openseatch.py
```

ระบบจะรันแปลงไฟล์ก่อน แล้วรอให้กด Enter ก่อนปิดหน้าต่าง

---

## 📄 เปลี่ยนชื่อไฟล์เมื่อรัน

ไฟล์ CSV ที่ได้จะมีชื่อเดียวกับไฟล์ JSON ต้นฉบับ โดยเปลี่ยนสกุลเป็น `.csv`

ตัวอย่าง:

- `json_gitbash/example.json` → `output_json_gitbash/example.csv`
- `json_athena/example.json` → `output_json_athena/example.csv`
- `json_openseatch/example.json` → `output_json_openseatch/example.csv`

---

## ✅ รูปแบบ CSV ที่ได้

### `convert__debug_gitbash.py`

หัวคอลัมน์:

`level | digitalId | txId | reqTxId | zone | brand | prdType | sourceSystem | reqIP | thread | mode | logger | message`

### `convert_debug_athena.py`

หัวคอลัมน์:

`level | digitalId | txId | brand | thread | mode | logger | message`

### `convert_debug_openseatch.py`

หัวคอลัมน์:

`message`

---

## 🔍 ค้นหา keyword (เฉพาะ `convert_debug_openseatch.py`)

ไฟล์ keyword ที่รองรับ:

- `keyword/old_keyword.json`
- `keyword/new_keyword.json`

เมื่อรันสคริปต์แล้ว ให้เลือก

```text
old
หรือ
new
```

โปรแกรมจะสร้างไฟล์สรุปในโฟลเดอร์ `result/` สำหรับแต่ละหัวข้อ

---

## ⚠️ ข้อควรระวัง

- ถ้าไม่มีไฟล์ `.json` ในโฟลเดอร์ input จะไม่มีการสร้างไฟล์ CSV
- ชื่อ CSV จะตั้งตามชื่อ JSON ต้นฉบับโดยอัตโนมัติ
- `convert_debug_openseatch.py` จะอ่านโครงสร้าง JSON แบบ Elasticsearch/Opensearch ที่มี `hits.hits` และ `_source.message`

---

## 💡 สรุป

โปรเจกต์นี้ช่วยให้แปลง log จาก 3 แหล่งหลักเป็น CSV ได้ง่าย และเก็บผลลัพธ์ในโฟลเดอร์ตามแต่ละรูปแบบ

- `convert__debug_gitbash.py` → `output_json_gitbash/`
- `convert_debug_athena.py` → `output_json_athena/`
- `convert_debug_openseatch.py` → `output_json_openseatch/`

หากต้องการเพิ่มสคริปต์ใหม่ ให้สร้างไฟล์ใหม่และกำหนด `INPUT_FOLDER` กับ `OUTPUT_FOLDER` ให้ตรงกับโฟลเดอร์ต้นทางและผลลัพธ์
