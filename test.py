import os, time, json
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image  # Thêm thư viện xử lý ảnh
from prompt import PROMPT

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
IMAGE_FOLDER = "Ảnh"
PDF_PATH = "Thống_nhất_gán_nhãn_phương_tiện_NMS.pptx.pdf"
MODEL_NAME = "gemini-2.5-flash"

if not API_KEY:
    raise RuntimeError("Chưa có GEMINI_API_KEY trong .env")

genai.configure(api_key=API_KEY)

generation_config = {
    "temperature": 0.1,
    "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    generation_config=generation_config,
    system_instruction=PROMPT,
)

def iter_labeling():
    """
    Generator gán nhãn từng ảnh, yield (result, index, total).
    """
    pdf_file = None
    try:
        print("Bắt đầu upload file hướng dẫn...")
        pdf_file = genai.upload_file(path=PDF_PATH, mime_type="application/pdf")

        while pdf_file.state.name == "PROCESSING":
            print("Đang xử lý file PDF...")
            time.sleep(2)
            pdf_file = genai.get_file(name=pdf_file.name)

        if pdf_file.state.name != "ACTIVE":
            raise RuntimeError(f"File PDF bị lỗi sau khi upload: {pdf_file.state.name}")
        print("File PDF đã sẵn sàng.")

        image_files = [
            f for f in os.listdir(IMAGE_FOLDER)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]
        total = len(image_files)
        print(f"\nTìm thấy {total} ảnh. Bắt đầu xử lý...")

        for idx, img_name in enumerate(image_files, start=1):
            img_path = os.path.join(IMAGE_FOLDER, img_name)
            print(f"--> Đang xử lý: {img_name}")
            try:
                img = Image.open(img_path)
                response = model.generate_content([pdf_file, img])
                data = json.loads(response.text)
                result = {"filename": img_name, "labels": data}
                print(f"-->Hoàn tất: {img_name}")
                time.sleep(10)
            except Exception as e:
                print(f"Lỗi khi xử lý ảnh {img_name}: {e}")
                result = {"filename": img_name, "error": str(e)}
            yield result, idx, total

        print("\nHoàn tất toàn bộ ảnh.")

    finally:
        if pdf_file:
            try:
                print(f"Đang xoá file PDF {pdf_file.name} trên server...")
                genai.delete_file(name=pdf_file.name)
                print(f"   Đã xoá file PDF.")
            except Exception as e:
                print(f"Lỗi khi xoá file PDF {pdf_file.name}: {e}")

def run_labeling():
    """
    Thu thập toàn bộ kết quả sau khi xử lý.
    """
    results = []
    for result, _, _ in iter_labeling():
        results.append(result)
    print(f"\nHoàn tất! Đã trả về {len(results)} kết quả.")
    return results

if __name__ == "__main__":
    run_labeling()
