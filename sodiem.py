from flask import Flask, url_for
from markupsafe import escape

app = Flask(__name__)
# Cấu hình JSON tiếng Việt có dấu
app.json.ensure_ascii = False

# Dữ liệu mẫu
STUDENTS = {
    "23T1020001": {
        "name": "Nguyễn Văn An",
        "lop": "K47A",
        "scores": {"PMMNM": 8.5, "CSDL": 7.0, "MMT": 9.0},
    },
    "23T1020002": {
        "name": "Trần Thị Bình",
        "lop": "K47A",
        "scores": {"PMMNM": 6.0, "CSDL": 5.5, "MMT": 7.0},
    },
    "23T1020003": {
        "name": "Lê Hoàng Cường",
        "lop": "K47B",
        "scores": {"PMMNM": 9.5, "CSDL": 9.0},
    },
    "23T1020004": {
        "name": "Phạm Minh Dũng",
        "lop": "K47B",
        "scores": {"PMMNM": 4.0, "CSDL": 3.5, "MMT": 5.0},
    },
    "23T1020005": {
        "name": "Hoàng Thu Hà",
        "lop": "K47A",
        "scores": {},
    },
    "23T1020006": {
        "name": "Võ Quốc Khánh",
        "lop": "K47C",
        "scores": {"PMMNM": 7.5, "MMT": 8.0},
    },
}

# --- Các hàm phụ ---
def average(scores: dict):
    if not scores:
        return None
    return round(sum(scores.values()) / len(scores), 2)

def rank(avg):
    if avg is None:
        return "Chưa có điểm"
    if avg >= 8.5:
        return "Giỏi"
    if avg >= 7.0:
        return "Khá"
    if avg >= 5.0:
        return "Trung bình"
    return "Yếu"

def student_summary(mssv: str):
    info = STUDENTS.get(mssv)
    if not info:
        return None
    avg = average(info["scores"])
    return {
        "mssv": mssv,
        "name": info["name"],
        "lop": info["lop"],
        "scores": dict(info["scores"]),
        "average": avg,
        "rank": rank(avg),
    }

def layout(title: str, body: str) -> str:
    escaped_title = escape(title)
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Sổ điểm - {escaped_title}</title>
    <style>
        body {{ font-family: sans-serif; margin: 24px; line-height: 1.5; }}
        nav {{ margin-bottom: 20px; }}
        nav a {{ margin-right: 12px; }}
        table {{ border-collapse: collapse; margin-top: 12px; }}
        th, td {{ border: 1px solid #ccc; padding: 6px 12px; text-align: left; }}
    </style>
</head>
<body>
    <nav>
        <strong>Sổ điểm</strong> |
        <a href="{url_for('index')}">Trang chủ</a>
        <a href="{url_for('student_list')}">Sinh viên</a>
        <a href="{url_for('search')}">Tìm kiếm</a>
    </nav>
    <main>
        {body}
    </main>
</body>
</html>"""

# Route tạm thời để url_for hoạt động ở Phần 0
@app.route("/")
def index():
    return layout("Trang chủ", "<p>Đang xây dựng...</p>")

@app.route("/students")
def student_list():
    return layout("Sinh viên", "<p>Đang xây dựng...</p>")

@app.route("/search")
def search():
    return layout("Tìm kiếm", "<p>Đang xây dựng...</p>")