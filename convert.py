import json
import csv
import os
import glob

# ชื่อโฟลเดอร์
INPUT_FOLDER = 'input'
OUTPUT_FOLDER = 'output'
RESULT_FOLDER = 'result'

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

def search_by_keyword_file():
    import glob
    import json

    # สร้าง result folder
    if not os.path.exists(RESULT_FOLDER):
        os.makedirs(RESULT_FOLDER)

    # ให้ user เลือก
    choice = input("เลือก keyword (old / new): ").strip().lower()

    keyword_path = os.path.join("keyword", f"{choice}_keyword.json")

    if not os.path.exists(keyword_path):
        print("❌ ไม่พบไฟล์ keyword")
        return

    # โหลด keyword
    with open(keyword_path, "r", encoding="utf-8") as f:
        keyword_data = json.load(f)

    csv_files = glob.glob(os.path.join(OUTPUT_FOLDER, "*.csv"))

    # loop ตามหัวข้อหลัก
    for topic, keywords in keyword_data.items():
        print(f"\n🔎 Searching topic: {topic}")

        topic_results = []

        for file_path in csv_files:
            filename = os.path.basename(file_path)

            with open(file_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                next(reader, None)

                for row_number, row in enumerate(reader, start=2):
                    if not row:
                        continue

                    full_text = " ".join(row).lower()

                    for keyword in keywords:
                        if keyword.lower() in full_text:
                            topic_results.append([
                                topic,
                                keyword,
                                filename,
                                row_number,
                                full_text
                            ])

        if not topic_results:
            print(f"⚠️ ไม่พบ keyword สำหรับ {topic}")
            continue

        # ตั้งชื่อไฟล์จาก topic
        safe_topic = topic.replace(" ", "_")
        summary_file = os.path.join(
            RESULT_FOLDER,
            f"{safe_topic}.csv"
        )

        with open(summary_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow([
                "topic",
                "keyword",
                "filename",
                "row_number",
                "message"
            ])
            writer.writerows(topic_results)

        print(f"✅ Export: {summary_file}")

if __name__ == "__main__":
    process_conversion()
    print("-" * 30)
    search_by_keyword_file()
    input("กด Enter เพื่อปิดหน้าต่างนี้...")