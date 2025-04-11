import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 데이터 파일 경로 설정 (CSV 파일)
STUDENT_DB_FILE = "student_db.csv"
GRADE_DB_FILE = "grade_db.csv"
ASSIGNMENT_DB_FILE = "assignment_db.csv"
ATTENDANCE_DB_FILE = "attendance_db.csv"
ATTENDANCE_CODE_FILE = "attendance_codes.csv"  # 출결 코드 관리 파일

# 기본 관리자 계정 설정
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "admin123"

# 데이터 파일 불러오기
def load_data():
    if not pd.io.common.file_exists(STUDENT_DB_FILE):
        student_df = pd.DataFrame(columns=["학생명", "전화번호", "이메일", "학부모 연락처", "학교명", "학년", "기존성적"])
        student_df.to_csv(STUDENT_DB_FILE, index=False)
    else:
        student_df = pd.read_csv(STUDENT_DB_FILE)
    
    if not pd.io.common.file_exists(GRADE_DB_FILE):
        grade_df = pd.DataFrame(columns=["이름", "시험명", "점수"])
        grade_df.to_csv(GRADE_DB_FILE, index=False)
    else:
        grade_df = pd.read_csv(GRADE_DB_FILE)
    
    if not pd.io.common.file_exists(ASSIGNMENT_DB_FILE):
        assignment_df = pd.DataFrame(columns=["과제명", "과제 내용", "학생 이름", "제출 여부", "피드백", "제출 일자", "과제 상태"])
        assignment_df.to_csv(ASSIGNMENT_DB_FILE, index=False)
    else:
        assignment_df = pd.read_csv(ASSIGNMENT_DB_FILE)
    
    if not pd.io.common.file_exists(ATTENDANCE_DB_FILE):
        attendance_df = pd.DataFrame(columns=["이름", "출석 여부", "날짜"])
        attendance_df.to_csv(ATTENDANCE_DB_FILE, index=False)
    else:
        attendance_df = pd.read_csv(ATTENDANCE_DB_FILE)
    
    if not pd.io.common.file_exists(ATTENDANCE_CODE_FILE):
        attendance_codes_df = pd.DataFrame(columns=["출결 코드", "생성 시간", "유효 시간"])
        attendance_codes_df.to_csv(ATTENDANCE_CODE_FILE, index=False)
    else:
        attendance_codes_df = pd.read_csv(ATTENDANCE_CODE_FILE)
    
    return student_df, grade_df, assignment_df, attendance_df, attendance_codes_df

# 학생 관리 섹터 1 - 학생 정보 표
def student_management_info(student_df, grade_df, assignment_df, attendance_df):
    st.title("학생 관리")
    
    # 섹터 1 - 학생 관리 표
    student_summary = pd.merge(student_df, grade_df, on="학생명", how="left")
    student_summary = pd.merge(student_summary, assignment_df[['학생 이름', '과제명', '제출 여부']], on='학생명', how='left')
    student_summary = pd.merge(student_summary, attendance_df[['이름', '출석 여부']], on='학생명', how='left')
    
    st.markdown("<div style='background-color:#333333; padding:10px; color:white;'>학생 관리</div>", unsafe_allow_html=True)
    st.dataframe(student_summary)

# 학생 관리 섹터 2 - 성적 히스토그램
def grade_histogram(grade_df, student_df):
    st.title("학생별 성적 히스토그램")
    
    # 섹터 2 - 학생별 성적 히스토그램
    student_name = st.selectbox("성적을 볼 학생을 선택하세요", student_df["학생명"])
    student_grades = grade_df[grade_df['이름'] == student_name]
    
    plt.figure(figsize=(10,6))
    sns.histplot(student_grades['점수'], kde=True, color="blue")
    plt.title(f"{student_name}의 성적 히스토그램")
    st.pyplot(plt)

# 출결 관리 섹터 3 - 출결 현황
def attendance_management(attendance_df, student_df):
    st.title("출결 현황")
    
    # 섹터 3 - 학생별 출결 현황
    student_name = st.selectbox("출결 현황을 볼 학생을 선택하세요", student_df["학생명"])
    student_attendance = attendance_df[attendance_df['이름'] == student_name]
    
    # 출결 여부 그래프
    plt.figure(figsize=(10,6))
    sns.countplot(x='출석 여부', data=student_attendance, palette='Set2')
    plt.title(f"{student_name}의 출결 현황")
    st.pyplot(plt)
    
    st.markdown(f"**{student_name}**의 출결 현황:")
    st.dataframe(student_attendance)

# 과제 관리 섹터 4 - 과제 현황
def assignment_management(assignment_df, student_df):
    st.title("과제 관리")
    
    # 섹터 4 - 과제 관리 현황
    student_name = st.selectbox("과제 현황을 볼 학생을 선택하세요", student_df["학생명"])
    student_assignments = assignment_df[assignment_df['학생 이름'] == student_name]
    
    # 과제 제출 여부를 색상으로 구분 (미제출: 빨강, 제출완료: 초록)
    student_assignments['과제 상태'] = student_assignments['과제 상태'].apply(lambda x: '미제출' if x == '미제출' else '제출완료')
    
    st.markdown("<div style='background-color:#333333; padding:10px; color:white;'>과제 현황</div>", unsafe_allow_html=True)
    st.dataframe(student_assignments)

# 학급 평균 성적 섹터 5 - 학급 평균 성적
def class_average(grade_df, student_df):
    st.title("학급 평균 성적")
    
    # 섹터 5 - 학급 평균 성적
    class_avg = grade_df.groupby('이름')['점수'].mean().reset_index()
    
    plt.figure(figsize=(10,6))
    sns.barplot(x='이름', y='점수', data=class_avg)
    plt.title("학급 평균 성적")
    st.pyplot(plt)

# 출결률 계산 섹터 6 - 출결률 계산
def attendance_rate(attendance_df, student_df):
    st.title("출결률 계산")
    
    # 섹터 6 - 출결률 계산
    attendance_rate = attendance_df.groupby('이름')['출석 여부'].apply(lambda x: (x == '출석').sum() / len(x) * 100).reset_index()
    attendance_rate = attendance_rate.rename(columns={'출석 여부': '출석률'})
    
    st.markdown("<div style='background-color:#333333; padding:10px; color:white;'>출결률</div>", unsafe_allow_htsml=True)
    st.dataframe(attendance_rate)

# 메인 페이지
def main():
    student_df, grade_df, assignment_df, attendance_df, attendance_codes_df = load_data()
    
    menu = ["학생 관리", "성적 히스토그램", "출결 관리", "과제 관리", "학급 평균 성적", "출결률 계산"]
    choice = st.sidebar.radio("메뉴", menu)
    
    if choice == "학생 관리":
        student_management_info(student_df, grade_df, assignment_df, attendance_df)
    elif choice == "성적 히스토그램":
        grade_histogram(grade_df, student_df)
    elif choice == "출결 관리":
        attendance_management(attendance_df, student_df)
    elif choice == "과제 관리":
        assignment_management(assignment_df, student_df)
    elif choice == "학급 평균 성적":
        class_average(grade_df, student_df)
    elif choice == "출결률 계산":
        attendance_rate(attendance_df, student_df)

if __name__ == "__main__":
    main()
