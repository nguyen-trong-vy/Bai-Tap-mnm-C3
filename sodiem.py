import io
import csv
from flask import Flask, url_for, request, redirect, abort, make_response
from markupsafe import escape

app = Flask(__name__)
app.json.ensure_ascii = False

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
        .filter {{ margin-bottom: 12px; }}
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

# --- Câu 1: Trang chủ ---
@app.route("/")
def index():
    total_students = len(STUDENTS)
    classes = sorted({info["lop"] for info in STUDENTS.values()})
    total_classes = len(classes)
    body = f"""<h1>Trang chủ Sổ điểm</h1>
    <p>Tổng số sinh viên: <strong>{escape(total_students)}</strong></p>
    <p>Số lớp: <strong>{escape(total_classes)}</strong> ({", ".join(escape(c) for c in classes)})</p>
    <p>
        <a href="{url_for('student_list')}">Xem danh sách sinh viên (Giao diện web)</a> | 
        <a href="{url_for('api_students')}">Xem danh sách sinh viên (API JSON)</a>
    </p>"""
    return layout("Trang chủ", body)

# --- Câu 2: Danh sách sinh viên ---
@app.route("/students")
def student_list():
    lop_filter = request.args.get("lop", "").strip()
    all_classes = sorted({info["lop"] for info in STUDENTS.values()})
    
    # Thanh lọc
    filter_links = [f'<a href="{url_for("student_list")}">Tất cả</a>']
    for c in all_classes:
        filter_links.append(f'<a href="{url_for("student_list", lop=c)}">{escape(c)}</a>')
    filter_bar = '<div class="filter">Lọc theo lớp: ' + " | ".join(filter_links) + "</div>"
    
    # Lọc danh sách
    filtered = []
    for mssv, info in STUDENTS.items():
        if not lop_filter or info["lop"].lower() == lop_filter.lower():
            filtered.append(student_summary(mssv))
            
    if not filtered:
        content = filter_bar + "<p>Không có sinh viên phù hợp.</p>"
        return layout("Danh sách sinh viên", content)
        
    rows = []
    for s in filtered:
        avg_display = f"{s['average']:.2f}" if s["average"] is not None else "-"
        detail_url = url_for("student_detail", mssv=s["mssv"])
        rows.append(
            f"<tr>"
            f'<td><a href="{detail_url}">{escape(s["mssv"])}</a></td>'
            f"<td>{escape(s['name'])}</td>"
            f"<td>{escape(s['lop'])}</td>"
            f"<td>{escape(avg_display)}</td>"
            f"<td>{escape(s['rank'])}</td>"
            f"</tr>"
        )
        
    table = f"""<table>
        <thead>
            <tr>
                <th>MSSV</th>
                <th>Họ tên</th>
                <th>Lớp</th>
                <th>Điểm TB</th>
                <th>Xếp loại</th>
            </tr>
        </thead>
        <tbody>
            {"".join(rows)}
        </tbody>
    </table>"""
    return layout("Danh sách sinh viên", filter_bar + table)

# --- Câu 3: Chi tiết sinh viên ---
@app.route("/students/<mssv>")
def student_detail(mssv):
    summary = student_summary(mssv)
    if not summary:
        abort(404, description=f"Không có sinh viên với MSSV = {mssv}.")
        
    avg_display = f"{summary['average']:.2f}" if summary["average"] is not None else "Chưa có điểm"
    class_filter_url = url_for("student_list", lop=summary["lop"])
    export_url = url_for("export_csv", mssv=mssv)
    short_url = url_for("short_link", mssv=mssv)
    
    score_rows = []
    for course, score in summary["scores"].items():
        score_rows.append(f"<tr><td>{escape(course)}</td><td>{escape(score)}</td></tr>")
    
    scores_table = "<p>Sinh viên chưa có điểm học phần nào.</p>"
    if score_rows:
        scores_table = f"""<table>
            <thead><tr><th>Học phần</th><th>Điểm</th></tr></thead>
            <tbody>{"".join(score_rows)}</tbody>
        </table>"""
        
    body = f"""<h1>Thông tin sinh viên</h1>
    <p><strong>MSSV:</strong> {escape(summary['mssv'])}</p>
    <p><strong>Họ tên:</strong> {escape(summary['name'])}</p>
    <p><strong>Lớp:</strong> <a href="{class_filter_url}">{escape(summary['lop'])}</a></p>
    <p><strong>Điểm trung bình:</strong> {escape(avg_display)}</p>
    <p><strong>Xếp loại:</strong> {escape(summary['rank'])}</p>
    <h3>Bảng điểm</h3>
    {scores_table}
    <p style="margin-top: 16px;">
        <a href="{export_url}">Tải bảng điểm (CSV)</a>
    </p>
    <p><small>Link rút gọn: <a href="{short_url}">{escape(short_url)}</a></small></p>"""
    return layout(f"Chi tiết - {summary['name']}", body)

# --- Câu 4: Link rút gọn ---
@app.route("/sv/<mssv>")
def short_link(mssv):
    return redirect(url_for("student_detail", mssv=mssv), code=301)

# --- Câu 5: Xuất CSV ---
@app.route("/students/<mssv>/export")
def export_csv(mssv):
    if mssv not in STUDENTS:
        abort(404, description=f"Không có sinh viên với MSSV = {mssv}.")
        
    student = STUDENTS[mssv]
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["hoc_phan", "diem"])
    for course, score in student["scores"].items():
        writer.writerow([course, score])
        
    response = make_response(output.getvalue())
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    response.headers["Content-Disposition"] = f"attachment; filename=diem_{mssv}.csv"
    return response

# --- Câu 6: Tìm kiếm an toàn ---
@app.route("/search")
def search():
    q = request.args.get("q", "")
    escaped_q = escape(q)
    results_html = ""
    
    if "q" in request.args:
        q_clean = q.strip().lower()
        matched = []
        if q_clean:
            for mssv, info in STUDENTS.items():
                if q_clean in info["name"].lower() or q_clean in mssv.lower():
                    matched.append((mssv, info["name"]))
                    
        results_html += f'<p>Tìm thấy <strong>{len(matched)}</strong> kết quả cho "{escaped_q}":</p>'
        if matched:
            results_html += "<ul>"
            for mssv, name in matched:
                detail_link = url_for("student_detail", mssv=mssv)
                results_html += f'<li><a href="{detail_link}">{escape(name)} ({escape(mssv)})</a></li>'
            results_html += "</ul>"
        else:
            results_html += "<p>Không tìm thấy kết quả nào phù hợp.</p>"
            
    body = f"""<h1>Tìm kiếm sinh viên</h1>
    <form method="GET" action="{url_for('search')}">
        <input type="text" name="q" value="{escaped_q}" placeholder="Nhập tên hoặc MSSV...">
        <button type="submit">Tìm kiếm</button>
    </form>
    <div style="margin-top: 16px;">
        {results_html}
    </div>"""
    return layout("Tìm kiếm", body)

# Route tạm thời cho API ở Phần 1
@app.route("/api/students")
def api_students():
    return {}