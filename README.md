# BÀI TẬP TỔNG HỢP CHƯƠNG 3 - SỔ ĐIỂM LỚP HỌC

## 1. Kết quả kiểm tra Routes (`flask --app sodiem routes`)

```text
Endpoint            Methods    Rule
------------------  ---------  ------------------------------------------
api_student_detail  GET, HEAD  /api/students/<mssv>
api_students        GET, HEAD  /api/students
export_csv          GET, HEAD  /students/<mssv>/export
index               GET, HEAD  /
manage_score        DELETE,    /api/students/<mssv>/scores/<course>
                    GET, HEAD,
                    PUT
search              GET, HEAD  /search
short_link          GET, HEAD  /sv/<mssv>
static              GET, HEAD  /static/<path:filename>
student_detail      GET, HEAD  /students/<mssv>
student_list        GET, HEAD  /students
```

*(Tổng cộng chính xác 10 routes, bao gồm cả endpoint `static` mặc định của Flask).*

---

## 2. Dòng trạng thái HTTP, Header quan trọng và Body của các lệnh curl

Thiết lập biến môi trường kiểm thử:
```bash
B=http://127.0.0.1:8000
S=$B/api/students/23T1020005/scores
```

---

### Lệnh 1: `curl -i $B/sv/23T1020001`
- **Dòng trạng thái**: `HTTP/1.1 301 MOVED PERMANENTLY`
- **Header quan trọng**:
  - `Location: /students/23T1020001`
  - `Content-Type: text/html; charset=utf-8`
- **Body**:
  ```html
  <!doctype html>
  <html lang=en>
  <title>301 Moved</title>
  <h1>Moved Permanently</h1>
  <p>The document has moved <a href="/students/23T1020001">here</a>.</p>
  ```

---

### Lệnh 2: `curl -i $B/students/23T1020001/export`
- **Dòng trạng thái**: `HTTP/1.1 200 OK`
- **Header quan trọng**:
  - `Content-Type: text/csv; charset=utf-8`
  - `Content-Disposition: attachment; filename=diem_23T1020001.csv`
- **Body**:
  ```csv
  hoc_phan,diem
  PMMNM,8.5
  CSDL,7.0
  MMT,9.0
  ```

---

### Lệnh 3: `curl "$B/api/students?lop=k47a&min_avg=7"`
- **Dòng trạng thái**: `HTTP/1.1 200 OK`
- **Header quan trọng**:
  - `Content-Type: application/json`
- **Body**:
  ```json
  [
    {
      "average": 8.17,
      "lop": "K47A",
      "mssv": "23T1020001",
      "name": "Nguyễn Văn An",
      "rank": "Khá",
      "scores": {
        "CSDL": 7.0,
        "MMT": 9.0,
        "PMMNM": 8.5
      }
    }
  ]
  ```

---

### Lệnh 4: `curl -i "$B/api/students?min_avg=abc"`
- **Dòng trạng thái**: `HTTP/1.1 400 BAD REQUEST`
- **Header quan trọng**:
  - `Content-Type: application/json`
- **Body**:
  ```json
  {
    "detail": "Tham số min_avg phải là một số thực hợp lệ.",
    "error": "Dữ liệu không hợp lệ"
  }
  ```

---

### Lệnh 5: `curl -i $B/api/students/999`
- **Dòng trạng thái**: `HTTP/1.1 404 NOT FOUND`
- **Header quan trọng**:
  - `Content-Type: application/json`
- **Body**:
  ```json
  {
    "detail": "Không có sinh viên với MSSV = 999.",
    "error": "Không tìm thấy"
  }
  ```

---

### Lệnh 6: `curl -i -X PUT "$S/web?score=9"`
- **Dòng trạng thái**: `HTTP/1.1 201 CREATED`
- **Header quan trọng**:
  - `Location: /api/students/23T1020005/scores/WEB`
  - `Content-Type: application/json`
- **Body**:
  ```json
  {
    "average": 9.0,
    "course": "WEB",
    "mssv": "23T1020005",
    "score": 9.0
  }
  ```

---

### Lệnh 7: `curl -X PUT "$S/WEB?score=7.5"`
- **Dòng trạng thái**: `HTTP/1.1 200 OK`
- **Header quan trọng**:
  - `Content-Type: application/json`
- **Body**:
  ```json
  {
    "average": 7.5,
    "course": "WEB",
    "mssv": "23T1020005",
    "score": 7.5
  }
  ```

---

### Lệnh 8: `curl -i -X PUT "$S/WEB?score=11"`
- **Dòng trạng thái**: `HTTP/1.1 400 BAD REQUEST`
- **Header quan trọng**:
  - `Content-Type: application/json`
- **Body**:
  ```json
  {
    "detail": "Điểm số phải nằm trong khoảng từ 0 đến 10.",
    "error": "Dữ liệu không hợp lệ"
  }
  ```

---

### Lệnh 9: `curl -i -X DELETE $S/WEB`
- **Dòng trạng thái**: `HTTP/1.1 204 NO CONTENT`
- **Header quan trọng**:
  - `Content-Type: text/html; charset=utf-8` (hoặc rỗng)
- **Body**:
  *(Rỗng - 0 bytes)*

---

### Lệnh 10: `curl -i -X POST $S/WEB`
- **Dòng trạng thái**: `HTTP/1.1 405 METHOD NOT ALLOWED`
- **Header quan trọng**:
  - `Allow: DELETE, GET, HEAD, OPTIONS, PUT`
  - `Content-Type: application/json`
- **Body (JSON theo Câu 9)**:
  ```json
  {
    "detail": "The method is not allowed for the requested URL.",
    "error": "Phương thức không được hỗ trợ"
  }
  ```

---

### Lệnh 11: `curl -i -X POST $B/students`
- **Dòng trạng thái**: `HTTP/1.1 405 METHOD NOT ALLOWED`
- **Header quan trọng**:
  - `Allow: GET, HEAD, OPTIONS`
  - `Content-Type: text/html; charset=utf-8`
- **Body (HTML theo Câu 9)**:
  ```html
  <!DOCTYPE html>
  <html lang="vi">
  <head>
      <meta charset="UTF-8">
      <title>Sổ điểm - Lỗi 405</title>
      ...
  </head>
  <body>
      ...
      <main>
          <h1>Phương thức không được hỗ trợ (405)</h1>
          <p>The method is not allowed for the requested URL.</p>
          <p><a href="/">Quay lại Trang chủ</a></p>
      </main>
  </body>
  </html>
  ```

---

## 3. Trả lời câu hỏi lý thuyết

### Câu 1: Vì sao Câu 4 dùng mã 301 còn Câu 8 trả về mã 201 kèm header Location?
- **Mã `301 Moved Permanently` (Câu 4):**
  - Dùng để thông báo rằng tài nguyên đã được chuyển hướng vĩnh viễn từ URL rút gọn (`/sv/<mssv>`) sang URL chính thức (`/students/<mssv>`).
  - Trình duyệt và công cụ tìm kiếm sẽ tự động lưu bộ nhớ cache cho chuyển hướng này, tự động dùng URL mới trong các lần truy cập tiếp theo nhằm tối ưu tốc độ và SEO.
- **Mã `201 Created` kèm header `Location` (Câu 8):**
  - Theo chuẩn thiết kế RESTful API, khi một tài nguyên mới được tạo thành công trên máy chủ (thêm mới điểm học phần), server phải phản hồi mã `201 Created`.
  - Header `Location` bắt buộc đi kèm để cung cấp URI định danh trực tiếp tới tài nguyên vừa mới được tạo (`/api/students/<mssv>/scores/<course>`), giúp client biết chính xác địa chỉ để truy xuất hoặc chỉnh sửa tài nguyên đó về sau.

### Câu 2: Thêm điểm cho sinh viên 23T1020005 rồi khởi động lại server, điểm đó còn không? Vì sao?
- **Kết quả:** Điểm đó **không còn** (bị mất).
- **Lý do:**
  - Ứng dụng hiện tại đang lưu trữ dữ liệu sinh viên trong một biến từ điển in-memory (`STUDENTS`) nằm trên bộ nhớ RAM của tiến trình Python.
  - Khi khởi động lại server, toàn bộ tiến trình Python bị hủy và bộ nhớ RAM giải phóng. Khi chạy lại, ứng dụng sẽ nạp lại từ điển ban đầu được định nghĩa tĩnh trong mã nguồn file `sodiem.py`, do đó mọi thay đổi trước đó sẽ biến mất vì chưa được lưu trữ bền vững vào cơ sở dữ liệu (Database) hoặc tệp tin lưu trữ lâu dài.

---

## 4. Cấu trúc nộp bài
```text
chuong_03/tong_hop/
├── .gitignore
├── README.md
├── requirements.txt
└── sodiem.py
```
