# Huong Dan Cai Dat

## 1. Cài đặt Các Công Cụ Cần Thiết

Dung pip version < 24.1

```sh
\Sybil\.venv\Scripts\python.exe -m pip install --upgrade pip==24.0
```

Cài đặt các công cụ cần thiết (setuptools, setuptools_scm, wheel, build) để xây dựng và cài đặt thư viện.

```bash
pip install --upgrade setuptools setuptools_scm wheel build
```

## 2. Xây Dựng Thư Viện

```sh
python -m build
```

## 3. Cài Đặt Thư Viện

Cài đặt thư viện đã được xây dựng từ tệp .whl trong thư mục dist:

```sh
pip install dist/sybil-<...>.whl
```

```sh
pip uninstall sybil
```