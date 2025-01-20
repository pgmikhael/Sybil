# Hướng Dẫn Cài Đặt

## 1. Cài Đặt Các Công Cụ Cần Thiết

Dùng pip phiên bản < 24.1

```sh
\Sybil\.venv\Scripts\python.exe -m pip install --upgrade pip==24.0
```

Cài đặt các công cụ cần thiết (setuptools, setuptools_scm, wheel, build):

```sh
pip install --upgrade setuptools setuptools_scm wheel build
```

## 2. Xây Dựng Thư Viện

```sh
python -m build
```

## 3. Cài Đặt Thư Viện

Cài đặt thư viện từ tệp .whl trong thư mục dist:

```sh
pip install dist/sybil-<version>.whl
```

## 4. Chạy Thử Thư Viện

Sau khi cài đặt, chạy thử thư viện:

```sh
python -m sybil
```

## 5. Gỡ Cài Đặt Thư Viện

Gỡ cài đặt thư viện:

```sh
pip uninstall sybil
```

## 6. Kiểm Tra Phiên Bản

Kiểm tra phiên bản thư viện đã cài đặt:

```sh
pip show sybil
```

## 7. Cập Nhật Thư Viện

Cập nhật thư viện lên phiên bản mới nhất:

```sh
pip install --upgrade sybil
```

## 8. Tài Liệu Tham Khảo

Tham khảo tài liệu chính thức tại [đây](https://example.com/sybil-docs).

---

Hy vọng hướng dẫn này sẽ giúp bạn cài đặt và sử dụng thư viện Sybil dễ dàng. Nếu có câu hỏi, vui lòng liên hệ qua email hỗ trợ.

---

*Chú ý: Đảm bảo sử dụng phiên bản Python và pip tương thích với thư viện Sybil.*

---

Cuối cùng, hãy đọc và hiểu các điều khoản và điều kiện sử dụng của thư viện trước khi cài đặt và sử dụng.
