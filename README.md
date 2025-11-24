# Gemini AI - Trình Gán Nhãn Phương Tiện Giao Thông

Dự án này là một công cụ ứng dụng mô hình ngôn ngữ lớn (LLM) **Gemini Pro** của Google để tự động phân tích và gán nhãn cho hình ảnh phương tiện giao thông. Giao diện web được xây dựng bằng **Streamlit** và đã được triển khai lên Streamlit Cloud.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://jobngoai.streamlit.app/)

## Giới thiệu

Công cụ này có khả năng đọc một file hướng dẫn quy tắc gán nhãn (dưới dạng PDF) và áp dụng các quy tắc đó để trích xuất thông tin chi tiết từ hình ảnh phương tiện, bao gồm:
- Hãng xe (Brand)
- Model xe (Model)
- Số lượng chỗ ngồi (Seat Count)
- Loại xe (Vehicle Type)
- Màu xe (Vehicle Color)
- Màu biển số (License Plate Color)

Mục tiêu là tự động hóa và tăng tốc quá trình gán nhãn dữ liệu, đảm bảo tính nhất quán và chính xác theo các quy tắc định sẵn.

## Demo trực tiếp

Bạn có thể trải nghiệm ứng dụng trực tiếp trên Streamlit Cloud qua đường link sau:

**[https://jobngoai.streamlit.app/](https://jobngoai.streamlit.app/)**

## Hướng dẫn cài đặt và chạy project локально

### Yêu cầu
- [Git](https://git-scm.com/downloads)
- [Python 3.9+](https://www.python.org/downloads/)

### Các bước cài đặt

**1. Clone a repository**
```bash
git clone https://github.com/21tuoino12trieu/Job.git
cd Job
```

**2. Tạo và kích hoạt môi trường ảo**
- **Đối với Windows:**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
- **Đối với macOS/Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

**3. Cài đặt các thư viện cần thiết**
```bash
pip install -r requirements.txt
```

**4. Cấu hình API Key**
1.  Tạo một file mới trong thư mục gốc của dự án và đặt tên là `.env`.
2.  Mở file `.env` và thêm vào nội dung sau, thay `YOUR_API_KEY_HERE` bằng Gemini API Key của bạn:
    ```
    GEMINI_API_KEY="YOUR_API_KEY_HERE"
    ```

**5. Chạy ứng dụng**
Sau khi hoàn tất các bước trên, chạy lệnh sau để khởi động ứng dụng Streamlit:
```bash
streamlit run app.py
```
Ứng dụng sẽ tự động mở trong trình duyệt của bạn.

## Cấu trúc dự án
```
.
├── Ảnh/                   # Thư mục chứa các hình ảnh phương tiện cần xử lý
├── .env                    # File (local) chứa API key
├── .gitignore              # Các file và thư mục được Git bỏ qua
├── app.py                  # File chính của ứng dụng Streamlit
├── prompt.py               # Chứa prompt chi tiết cho mô hình Gemini
├── README.md               # File hướng dẫn này
├── requirements.txt        # Danh sách các thư viện Python cần thiết
└── Thống_nhất_gán_nhãn_phương_tiện_NMS.pptx.pdf  # File hướng dẫn quy tắc gán nhãn
```
