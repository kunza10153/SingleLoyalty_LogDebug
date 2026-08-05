import json
import csv
import os
import glob
import re

INPUT_FOLDER = 'json_gitbash'
OUTPUT_FOLDER = 'output_json_gitbash'


# =========================
# helper ดึงค่า field
# =========================
def extract_value(text, key):
    """
    ดึง value จาก json log แบบไม่ strict
    รองรับ log พัง / quote หาย / comma หาย
    """

    patterns = [
        rf'"{key}"\s*:\s*"([^"]*)"',      # "key":"value"
        rf'"{key}"\s*:\s*([^,",}}]+)',   # "key":value
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)

    return ''


# =========================
# helper clean message
# =========================
def clean_message(message):
    if not message:
        return ''

    # ลบ newline
    message = message.replace('\n', ' ').replace('\r', ' ')

    # ลบ pipe กัน csv เพี้ยน
    message = message.replace('|', ' ')

    # ลด space ซ้ำ
    message = re.sub(r'\s+', ' ', message)

    return message.strip()


# =========================
# extract logs
# =========================
def extract_messages_from_file(input_file):

    messages = []

    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:

        for line_number, line in enumerate(f, start=1):

            line = line.strip()

            if not line:
                continue

            try:

                # =========================
                # พยายาม parse json ก่อน
                # =========================
                try:
                    data = json.loads(line)

                    row = [
                        data.get('level', ''),
                        data.get('digitalId', ''),
                        data.get('txId', ''),
                        data.get('reqTxId', ''),
                        data.get('zone', ''),
                        data.get('brand', ''),
                        data.get('prdType', ''),
                        data.get('sourceSystem', ''),
                        data.get('reqIP', ''),
                        data.get('thread', ''),
                        data.get('mode', ''),
                        data.get('logger', ''),
                        clean_message(
                            data.get('message')
                            or data.get('msg')
                            or data.get('log')
                            or data.get('content')
                            or ''
                        )
                    ]

                    messages.append(row)

                except Exception:

                    # =========================
                    # fallback regex mode
                    # =========================
                    row = [
                        extract_value(line, 'level'),
                        extract_value(line, 'digitalId'),
                        extract_value(line, 'txId'),
                        extract_value(line, 'reqTxId'),
                        extract_value(line, 'zone'),
                        extract_value(line, 'brand'),
                        extract_value(line, 'prdType'),
                        extract_value(line, 'sourceSystem'),
                        extract_value(line, 'reqIP'),
                        extract_value(line, 'thread'),
                        extract_value(line, 'mode'),
                        extract_value(line, 'logger'),
                        clean_message(extract_value(line, 'message'))
                    ]

                    messages.append(row)

            except Exception as e:
                print(f"⚠️ Error line {line_number}: {e}")

    return messages


# =========================
# main process
# =========================
def process_conversion():

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    json_files = glob.glob(os.path.join(INPUT_FOLDER, '*.json'))

    if len(json_files) == 0:
        print("ไม่พบไฟล์ .json")
        return

    print(f"พบไฟล์ JSON ทั้งหมด {len(json_files)} ไฟล์")

    for input_file in json_files:

        try:

            filename = os.path.basename(input_file)
            name_without_ext = os.path.splitext(filename)[0]

            output_file = os.path.join(
                OUTPUT_FOLDER,
                f"{name_without_ext}.csv"
            )

            print(f"\nกำลังประมวลผล: {filename}")

            messages = extract_messages_from_file(input_file)

            if not messages:
                print(f"⚠️ ไม่พบข้อมูลในไฟล์")
                continue

            with open(
                output_file,
                'w',
                newline='',
                encoding='utf-8-sig'
            ) as f:

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
            print(f"✅ จำนวน rows: {len(messages)}")

        except Exception as e:
            print(f"❌ Error ในไฟล์ {filename}: {e}")


if __name__ == "__main__":
    process_conversion()

    print("-" * 30)
    input("กด Enter เพื่อปิดหน้าต่างนี้...")