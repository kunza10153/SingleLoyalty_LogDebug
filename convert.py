import json
import csv
import os
import glob

# ชื่อโฟลเดอร์
INPUT_FOLDER = 'input'
OUTPUT_FOLDER = 'output'


def process_conversion():
    # 1. สร้างโฟลเดอร์ output ถ้ายังไม่มี
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    # 2. ค้นหาไฟล์ .json ทั้งหมดในโฟลเดอร์ input
    json_files = glob.glob(os.path.join(INPUT_FOLDER, '*.json'))

    # 3. ตรวจสอบว่ามีไฟล์หรือไม่
    if len(json_files) == 0:
        print("ไม่พบไฟล์ .json ในโฟลเดอร์ 'input'")
        return

    print(f"พบไฟล์ JSON ทั้งหมด {len(json_files)} ไฟล์")

    # 4. loop ทุกไฟล์
    for input_file in json_files:
        try:
            filename = os.path.basename(input_file)
            name_without_ext = os.path.splitext(filename)[0]
            output_file = os.path.join(OUTPUT_FOLDER, f"{name_without_ext}.csv")

            print(f"\nกำลังประมวลผล: {filename}")

            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            hits = data.get('hits', {}).get('hits', [])

            messages = []
            for hit in hits:
                msg = hit.get('_source', {}).get('message', '')
                if msg:
                    messages.append([msg])

            if not messages:
                print(f"⚠️ ไม่พบ message ในไฟล์ {filename}")
                continue

            with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(['message'])
                writer.writerows(messages)

            print(f"✅ สร้างไฟล์: {output_file}")

        except Exception as e:
            print(f"❌ Error ในไฟล์ {filename}: {e}")


if __name__ == "__main__":
    process_conversion()
    print("-" * 30)
    input("กด Enter เพื่อปิดหน้าต่างนี้...")