import json
import csv
import os
import glob
import re

# ชื่อโฟลเดอร์
INPUT_FOLDER = 'input2'
OUTPUT_FOLDER = 'output2'


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

            messages = extract_messages_from_file(input_file)
            if not messages:
                print(f"⚠️ ไม่พบ message ในไฟล์ {filename}")
                continue

            with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(
                    f,
                    delimiter='|',
                    quoting=csv.QUOTE_MINIMAL
                )
                writer.writerow([
                    'level',
                    'digitalId',
                    'txId',
                    'reqTxId',
                    'zone',
                    'brand',
                    'prdType',
                    'sourceSystem',
                    'reqIP',
                    'thread',
                    'mode',
                    'logger',
                    'message'
                ])
                writer.writerows(messages)

            print(f"✅ สร้างไฟล์: {output_file}")

        except Exception as e:
            print(f"❌ Error ในไฟล์ {filename}: {e}")



def extract_messages_from_file(input_file):
    messages = []

    with open(input_file, 'r', encoding='utf-8') as f:

        for line_number, line in enumerate(f, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                data = json.loads(line)

                level = data.get('level', '')
                digital_id = data.get('digitalId', '')
                tx_id = data.get('txId', '')
                req_tx_id = data.get('reqTxId', '')
                zone = data.get('zone', '')
                brand = data.get('brand', '')
                prd_type = data.get('prdType', '')
                source_system = data.get('sourceSystem', '')
                req_ip = data.get('reqIP', '')
                thread = data.get('thread', '')
                mode = data.get('mode', '')
                logger = data.get('logger', '')
                message = data.get('message', '')

                messages.append([
                    level,
                    digital_id,
                    tx_id,
                    req_tx_id,
                    zone,
                    brand,
                    prd_type,
                    source_system,
                    req_ip,
                    source_system,
                    brand,
                    thread,
                    mode,
                    logger,
                    message
                ])

            except json.JSONDecodeError as e:
                print(f"⚠️ JSON parse error line {line_number}: {e}")

    return messages



if __name__ == "__main__":
    process_conversion()
    print("-" * 30)
    input("กด Enter เพื่อปิดหน้าต่างนี้...")