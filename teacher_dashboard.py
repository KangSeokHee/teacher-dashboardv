
import streamlit as st
import sqlite3
import os

st.set_page_config(page_title="식키수학연구소 - TMS", layout="wide")
st.title("📘 식키수학연구소 - 선생님 대시보드")

# DB 확인
db_path = "students.db"
if not os.path.exists(db_path):
    st.error("❌ DB 파일이 없습니다. students.db를 프로젝트 폴더에 포함해주세요.")
    st.stop()

# DB 연결
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS students (name TEXT, grade TEXT)")
conn.commit()

# 학생 목록 출력
st.subheader("👩‍🏫 등록된 학생 목록")
students = c.execute("SELECT name, grade FROM students").fetchall()
if students:
    for name, grade in students:
        st.write(f"- {name} ({grade})")
else:
    st.info("아직 등록된 학생이 없습니다.")

# 학생 추가
st.subheader("➕ 학생 추가")
with st.form("add_student"):
    new_name = st.text_input("이름")
    new_grade = st.selectbox("학년", [f"초등학교 {i}학년" for i in range(1, 7)] + [f"중학교 {i}학년" for i in range(1, 4)] + [f"고등학교 {i}학년" for i in range(1, 4)])
    submitted = st.form_submit_button("등록")
    if submitted and new_name:
        c.execute("INSERT INTO students (name, grade) VALUES (?, ?)", (new_name, new_grade))
        conn.commit()
        st.success(f"{new_name} 학생이 등록되었습니다.")
        st.rerun()
