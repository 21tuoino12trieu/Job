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

def run_labeling():
    """
    Chạy gán nhãn tất cả ảnh trong IMAGE_FOLDER.
    Trả về danh sách kết quả sau khi xử lý xong.
    """
    pdf_file = None
    results = []
    try:
        # --- Luôn upload lại file PDF từ đầu (bắt buộc) ---
        print("Bắt đầu upload file hướng dẫn...")
        pdf_file = genai.upload_file(path=PDF_PATH, mime_type="application/pdf")
        
        while pdf_file.state.name == "PROCESSING":
            print("Đang xử lý file PDF...")
            time.sleep(2)
            pdf_file = genai.get_file(name=pdf_file.name)

        if pdf_file.state.name != "ACTIVE":
            raise RuntimeError(f"File PDF bị lỗi sau khi upload: {pdf_file.state.name}")
        print("File PDF đã sẵn sàng.")

        # --- Xử lý tất cả các ảnh bằng cách đọc trực tiếp ---
        image_files = [
            f for f in os.listdir(IMAGE_FOLDER)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]
        print(f"\nTìm thấy {len(image_files)} ảnh. Bắt đầu xử lý...")

        for img_name in image_files:
            img_path = os.path.join(IMAGE_FOLDER, img_name)
            print(f"--> Đang xử lý: {img_name}")
            try:
                # Đọc ảnh trực tiếp bằng Pillow
                img = Image.open(img_path)
                # Gửi thẳng đối tượng ảnh, không cần upload
                response = model.generate_content([pdf_file, img])
                data = json.loads(response.text)
                results.append({"filename": img_name, "labels": data})
                print(f"-->Hoàn tất: {img_name}")
                time.sleep(10)  # Giữ nguyên độ trễ giữa các yêu cầu
            except Exception as e:
                print(f"Lỗi khi xử lý ảnh {img_name}: {e}")
                results.append({"filename": img_name, "error": str(e)})

        print(f"\nHoàn tất! Đã trả về {len(results)} kết quả.")
        return results

    finally:
        # --- Luôn dọn dẹp file PDF sau khi chạy ---
        if pdf_file:
            try:
                print(f"Đang xoá file PDF {pdf_file.name} trên server...")
                genai.delete_file(name=pdf_file.name)
                print(f"   Đã xoá file PDF.")
            except Exception as e:
                print(f"Lỗi khi xoá file PDF {pdf_file.name}: {e}")

if __name__ == "__main__":
    run_labeling()
