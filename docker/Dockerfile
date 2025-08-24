# Sử dụng Python 3.12 slim image làm base image
# Slim version nhẹ hơn nhưng vẫn đủ các thư viện cần thiết
FROM python:3.12-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Cài đặt các dependencies hệ thống cần thiết
# build-essential: để compile các package Python có C extensions
# curl: để health check
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy file requirements.txt trước để tận dụng Docker layer caching
# Nếu requirements.txt không thay đổi, layer này sẽ được cache
COPY requirements.txt .

# Cài đặt các dependencies Python
# --no-cache-dir: không lưu cache để giảm kích thước image
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ source code vào container
# Sử dụng cấu trúc thư mục mới đã refactor
COPY src/ ./src/
COPY data/ ./data/
COPY .env* ./

# Tạo các thư mục cần thiết cho ứng dụng
# rag_storage: lưu trữ indexes và embeddings
# logs: lưu trữ log files (nếu cần)
RUN mkdir -p /app/rag_storage /app/logs

# Expose port 8000 để truy cập API từ bên ngoài
EXPOSE 8000

# Thiết lập biến môi trường
# PYTHONPATH: Thêm src vào Python path để import modules
ENV PYTHONPATH=/app/src
# PYTHONUNBUFFERED: Hiển thị output ngay lập tức (không buffer)
ENV PYTHONUNBUFFERED=1
# WORKING_DIR: Thư mục làm việc chính
ENV WORKING_DIR=/app
# DATA_PATH: Đường dẫn file dữ liệu mặc định
ENV DATA_PATH=/app/data/data.txt

# Health check để kiểm tra container có hoạt động không
# Kiểm tra mỗi 30s, timeout 10s, thử lại 3 lần, chờ 40s ban đầu
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Chạy ứng dụng chính thông qua main.py (entry point mới)
CMD ["python", "src/main.py"]
