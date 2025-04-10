import sqlite3
import streamlit as st

# 데이터베이스 연결
conn = sqlite3.connect("students.db")
c = conn.cursor()

# 테이블 생성 코드: 만약 테이블이 없다면 생성
def create_tables():
    try:
        c.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            grade TEXT
        )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            student_id INTEGER,
            date TEXT,
            status TEXT
        )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            student_id INTEGER,
            test_name TEXT,
            score INTEGER
        )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            due_date TEXT,
            description TEXT
        )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS counseling (
            student_id INTEGER,
            date TEXT,
            counselor TEXT,
            type TEXT,
            content TEXT
        )
        """)
        conn.commit()
    except sqlite3.OperationalError as e:
        st.error(f"테이블 생성 오류: {e}")
        conn.rollback()

create_tables()  # 테이블 생성 함수 호출

# 메뉴 선택
menu = st.sidebar.selectbox("📂 메뉴 선택", ["학생 관리", "출결 관리", "성적 등록", "과제 관리", "상담 기록"])

# 학생 관리
if menu == "학생 관리":
    st.subheader("👩‍🏫 학생 목록")
    try:
        students = c.execute("SELECT id, name, grade FROM students").fetchall()
        for sid, name, grade in students:
            st.write(f"- {name} ({grade})")
    except sqlite3.OperationalError as e:
        st.error(f"학생 목록 조회 중 오류 발생: {e}")

    st.markdown("---")
    st.subheader("➕ 학생 추가")
    with st.form("add_student"):
        name = st.text_input("이름")
        grade = st.selectbox("학년", [f"초등학교 {i}학년" for i in range(1, 7)] + [f"중학교 {i}학년" for i in range(1, 4)] + [f"고등학교 {i}학년" for i in range(1, 4)])
        submit = st.form_submit_button("등록")
        if submit:
            try:
                c.execute("INSERT INTO students (name, grade) VALUES (?, ?)", (name, grade))
                conn.commit()
                st.success(f"{name} 학생이 등록되었습니다.")
                st.rerun()  # 화면 리로딩
            except sqlite3.OperationalError as e:
                st.error(f"학생 추가 중 오류 발생: {e}")

# 출결 관리
elif menu == "출결 관리":
    st.subheader("📆 학생 출결 관리")
    students = c.execute("SELECT id, name FROM students").fetchall()
    try:
        for sid, name in students:
            with st.expander(f"{name} 출결 기록"):
                date = st.date_input(f"출결 날짜 ({name})", key=f"date_{sid}")
                status = st.radio(f"출결 상태", ["출석", "지각", "결석"], key=f"status_{sid}")
                if st.button("저장", key=f"save_att_{sid}"):
                    c.execute("INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)", (sid, date.strftime('%Y-%m-%d'), status))
                    conn.commit()
                    st.success("저장 완료")
    except sqlite3.OperationalError as e:
        st.error(f"출결 기록 저장 중 오류 발생: {e}")

# 성적 등록
elif menu == "성적 등록":
    st.subheader("📊 성적 입력")
    students = c.execute("SELECT id, name FROM students").fetchall()
    try:
        for sid, name in students:
            with st.expander(f"{name} 성적 입력"):
                test = st.text_input(f"시험명", key=f"test_{sid}")
                score = st.number_input("점수", 0, 100, key=f"score_{sid}")
                if st.button("저장", key=f"save_score_{sid}"):
                    c.execute("INSERT INTO scores (student_id, test_name, score) VALUES (?, ?, ?)", (sid, test, score))
                    conn.commit()
                    st.success("성적 저장됨")
    except sqlite3.OperationalError as e:
        st.error(f"성적 저장 중 오류 발생: {e}")

# 과제 관리
elif menu == "과제 관리":
    st.subheader("📝 과제 등록")
    with st.form("assignment_form"):
        title = st.text_input("과제 제목")
        due = st.date_input("마감일")
        desc = st.text_area("과제 설명")
        submit = st.form_submit_button("등록")
        if submit:
            try:
                c.execute("INSERT INTO assignments (title, due_date, description) VALUES (?, ?, ?)", (title, due.strftime('%Y-%m-%d'), desc))
                conn.commit()
                st.success("과제가 등록되었습니다.")
            except sqlite3.OperationalError as e:
                st.error(f"과제 등록 중 오류 발생: {e}")

    st.subheader("📋 과제 목록")
    try:
        for aid, title, due, desc in c.execute("SELECT * FROM assignments").fetchall():
            st.markdown(f"### {title} (마감: {due})\n{desc}")
    except sqlite3.OperationalError as e:
        st.error(f"과제 목록 조회 중 오류 발생: {e}")

# 상담 기록
elif menu == "상담 기록":
    st.subheader("🗂 상담 내용 입력")
    students = c.execute("SELECT id, name FROM students").fetchall()
    try:
        for sid, name in students:
            with st.expander(f"{name} 상담 작성"):
                date = st.date_input("상담일")
                counselor = st.text_input("상담자명", key=f"counselor_{sid}")
                kind = st.selectbox("상담 종류", ["생활", "학습", "기타"], key=f"type_{sid}")
                content = st.text_area("상담 내용", key=f"content_{sid}")
                if st.button("기록", key=f"log_{sid}"):
                    c.execute("INSERT INTO counseling (student_id, date, counselor, type, content) VALUES (?, ?, ?, ?, ?)", (sid, date.strftime('%Y-%m-%d'), counselor, kind, content))
                    conn.commit()
                    st.success("상담 내용이 저장되었습니다.")
    except sqlite3.OperationalError as e:
        st.error(f"상담 기록 저장 중 오류 발생: {e}")
