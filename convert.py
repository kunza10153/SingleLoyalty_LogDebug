import json
import csv
import os
import glob

# ชื่อไฟล์ต้นทางและปลายทาง
INPUT_FOLDER = 'input'
OUTPUT_FOLDER = 'output'
OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, 'result.csv')


def process_conversion():
    # 1. สร้างโฟลเดอร์ output ถ้ายังไม่มี
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    # 2. ค้นหาไฟล์ .json ทั้งหมดในโฟลเดอร์ input
    json_files = glob.glob(os.path.join(INPUT_FOLDER, '*.json'))

    # 3. ตรวจสอบเงื่อนไขการอ่านไฟล์
    if len(json_files) == 0:
        print("ไม่พบไฟล์ .json ในโฟลเดอร์ 'input' กรุณาเช็คชื่อไฟล์")
        return
    elif len(json_files) > 1:
        print(f"พบไฟล์ .json ทั้งหมด {len(json_files)} ไฟล์")
        print("กรุณาให้เหลือไฟล์เดียวในโฟลเดอร์ input เพื่อป้องกันข้อมูลสับสน")
        return

    input_file = json_files[0]
    print(f"กำลังอ่านไฟล์: {os.path.basename(input_file)}")

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        hits = data.get('hits', {}).get('hits', [])

        messages = []
        for hit in hits:
            msg = hit.get('_source', {}).get('message', '')
            if msg:
                messages.append([msg])

        if not messages:
            print("ไม่พบข้อมูลในฟิลด์ 'message' ภายในไฟล์นี้")
            return

        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['message'])
            writer.writerows(messages)

        print(f"ไฟล์ถูกสร้างที่: {OUTPUT_FILE}")

    except Exception as e:
        print(f"เกิดข้อผิดพลาดระหว่างทำงาน: {e}")


if __name__ == "__main__":
    process_conversion()
    print("-" * 30)
    input("กด Enter เพื่อปิดหน้าต่างนี้...")