import streamlit as st
import json
import os
from PIL import Image, ImageOps
import test as labeler  # tái sử dụng logic gán nhãn

# Đường dẫn đến thư mục chứa ảnh
IMAGE_DIR = 'Ảnh'

def process_image(image_path, size=(250, 250)):
    """Opens an image, pads it to a square, and resizes it."""
    try:
        img = Image.open(image_path)
        # Pad the image to be a square
        img_square = ImageOps.pad(img, size, color='white')
        return img_square
    except FileNotFoundError:
        return None

def display_entry(entry):
    """Displays a single entry as a row with two columns (image and labels)."""
    filename = entry.get('filename')
    labels = entry.get('labels', {})

    if not filename:
        st.warning("Entry missing 'filename'. Skipping.")
        return

    col1, col2 = st.columns([1, 2])

    with col1:
        image_path = os.path.join(IMAGE_DIR, filename)
        processed_image = process_image(image_path)
        
        image_html = ""
        if processed_image:
            # Streamlit's st.image automatically handles centering if width is not 100%
            # To explicitly center and align vertically, we use a div with flexbox
            # The caption will be rendered by st.image, and we'll center the whole block
            st.markdown(f"""
            <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100%;">
            """, unsafe_allow_html=True)
            st.image(processed_image, caption=filename)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning(f"Image not found: {image_path}")

    with col2:
        label_items = []
        for key, value in labels.items():
            if key != "reasoning":
                label_items.append(f"<li><b>{key.replace('_', ' ').title()}:</b> {value}</li>")
        
        # Center the text block using HTML for better alignment
        label_html = f"""
        <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
            <ul style="text-align: left; list-style-position: inside; margin: 0; padding: 0;">
                {''.join(label_items)}
            </ul>
        </div>
        """
        st.markdown(label_html, unsafe_allow_html=True)

    st.markdown("---") # Separator for the next row

def main():
    st.set_page_config(layout="wide")
    # Centered main title
    st.markdown("<h1 style='text-align: center;'>Bảng thông tin chi tiết xe</h1>", unsafe_allow_html=True)

    if st.button("Chạy gán nhãn"):
        progress = st.progress(0.0, text="Đang xử lý 0 ảnh...")
        status = st.empty()
        results = []
        try:
            for result, idx, total in labeler.iter_labeling():
                results.append(result)
                st.session_state["label_results"] = results
                if total > 0:
                    progress.progress(idx / total, text=f"Đang xử lý {idx}/{total} ảnh...")
            st.success("Hoàn tất! Đã cập nhật lại kết quả gán nhãn trong phiên hiện tại.")
            st.rerun()
        except Exception as e:
            st.error(f"Lỗi khi chạy gán nhãn: {e}")

    # Create and center table headers
    header_col1, header_col2 = st.columns([1, 2])
    with header_col1:
        st.markdown("<h2 style='text-align: center;'>Hình ảnh</h2>", unsafe_allow_html=True)
    with header_col2:
        st.markdown("<h2 style='text-align: center;'>Thông tin chi tiết</h2>", unsafe_allow_html=True)
    st.markdown("---")

    # Lấy dữ liệu từ session_state (đã được cập nhật sau khi bấm nút)
    data = st.session_state.get("label_results", [])

    if data:
        data.sort(key=lambda x: x.get('filename', ''))
        for entry in data:
            display_entry(entry)
    else:
        st.info("Không có dữ liệu để hiển thị. Hãy bấm nút 'Chạy gán nhãn' để tạo kết quả mới.")

if __name__ == "__main__":
    main()
