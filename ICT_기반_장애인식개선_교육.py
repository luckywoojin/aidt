import streamlit as st
import sqlite3
import pandas as pd
import re  # Importing regex module for email validation
import smtplib
from email.mime.text import MIMEText
from datetime import datetime # 시간을 기록

st.set_page_config(page_title='정보통신기술(ICT) 기반 장애 인식 개선 교육 프로그램', layout='wide')

######################## DB 관련 #############################

# SQLite 데이터베이스 연결
conn = sqlite3.connect('users.db')
c = conn.cursor()

# 새 users 테이블 생성
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        userid TEXT PRIMARY KEY,
        passwd TEXT,
        email TEXT,
        file_data type,
        user_type TEXT,
        name TEXT
    )
''')
conn.commit()

def send_email(recipient_email, subject, body):
    sender_email = "imeilbonaeneunyong@gmail.com"
    sender_password = "xgym xgab hfgc ymeo"  # 생성한 앱 비밀번호로 대체

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
    except smtplib.SMTPAuthenticationError:
        st.error("이메일 인증 오류입니다. 사용자 이름과 비밀번호를 확인하세요.")
    except Exception as e:
        st.error(f"이메일 전송 중 오류가 발생했습니다: {e}")

# 사용자 로그인 확인 함수
def check_user(userid, passwd):
    c.execute('SELECT * FROM users WHERE userid = ? AND passwd = ?', (userid, passwd))
    return c.fetchone()

######################## 유저 정보 가져오기, 로그 관련 함수 #############################

def get_current_user_info(userid):
    c.execute('SELECT name, email, user_type FROM users WHERE userid = ?', (userid,))
    return c.fetchone()  # (name, email, user_type) 형태로 반환됨

# 사용자 정보 가져오기 함수
def get_users():
    c.execute('SELECT userid, passwd, email, user_type, name FROM users')  # 모든 열을 명시적으로 선택
    return c.fetchall()

#log 관련 db불러오기
l = sqlite3.connect('log.db')

l.execute('''
    CREATE TABLE IF NOT EXISTS log (
        userid TEXT,
        name TEXT,
        page TEXT,
        tab TEXT,
        date TEXT,
        PRIMARY KEY (userid, date)  -- Composite primary key to allow multiple entries per user
    )
''')
l.commit()

def log_record(page, tab):
    date = datetime.now().isoformat()
    l.execute('INSERT INTO log (userid, name, page, tab, date) VALUES (?, ?, ?, ?, ?)', (userid, name, page, tab, date))
    l.commit()

######################## 회원가입 관련 #############################

# 이메일 형식 검증 함수 (수정된 버전)
def is_valid_email(email):
    # 정규 표현식을 사용하여 이메일 형식 검사
    email_regex = r'^[\w\.-]+@(naver\.com|gmail\.com)$'
    return re.match(email_regex, email) is not None

# 사용자 이메일 확인 함수
def check_email_exists(email):
    c.execute('SELECT * FROM users WHERE email = ?', (email,))
    return c.fetchone() is not None

# 사용자 삭제 함수
def delete_user(userid):
    c.execute('DELETE FROM users WHERE userid = ?', (userid,))
    conn.commit()

# 로그인 중인 사용자 정보 출력
if 'current_user' in st.session_state:
    user_info = get_current_user_info(st.session_state['current_user'])
    if user_info:
        name, email, user_type = user_info  # 튜플에서 이름, 이메일, 사용자 유형 추출
        user_id = st.session_state['current_user']  # current_user에서 user_id 추출
        st.success(f'{name}({user_id}) {user_type}, 접속을 환영합니다.')

def add_user(userid, passwd, email, user_type, name):
    c.execute('INSERT INTO users (userid, passwd, email, user_type, name) VALUES (?, ?, ?, ?, ?)', 
              (userid, passwd, email, user_type, name))
    conn.commit()  # 변경 사항을 커밋해야 함

######################## 여기부터 진짜 내용 시작 #############################

c1, c2 = st.columns((6, 4))
with c1:
    st.title('정보통신기술(ICT) 기반 장애 인식 개선 교육 프로그램')
    st.image('./images/00_main_page.png')
    st.image('./images/00_howto_connet.png')

# Tabs for login, register, and admin
with c2:
    t1, t2, t3 = st.tabs(['로그인', '회원가입', '관리자'])

# 로그인 탭
with t1:
    st.subheader('로그인')

    # session_state 키를 초기화
    if 'login_status' not in st.session_state:
        st.session_state['login_status'] = False # 해당 사용자는 로그인 상태가 아님.
    if 'current_user' not in st.session_state:
        st.session_state['current_user'] = None
    if 'find_account' not in st.session_state:
        st.session_state['find_account'] = False  # 아이디/비밀번호 찾기 상태

    # 로그인 상태일 때 로그아웃 버튼 표시
    if st.session_state['login_status']:
        st.success(f'로그인 성공: {name}({user_id})님, 환영합니다.')
        if st.button('로그아웃'):
            st.session_state.clear()  # 세션 초기화로 로그아웃 처리
            st.rerun()  # 페이지 새로고침 효과

    else:
        # 로그인 폼
        with st.form('login_form'):
            userid = st.text_input('아이디', key='luserid')
            passwd = st.text_input('비밀번호', key='lpasswd', type='password')
            login_button = st.form_submit_button('로그인')

            if login_button:
                if all([userid, passwd]):
                    user = check_user(userid, passwd)
                    if user:
                        st.session_state['login_status'] = True
                        st.session_state['current_user'] = userid
                        name, email, user_type = get_current_user_info(userid)  # 사용자 정보 가져오기
                        st.success(f'{name}님, 로그인에 성공하였습니다.')
                    else:
                        st.error('잘못된 사용자 ID 또는 비밀번호입니다.')
                else:
                    st.error('모든 정보를 입력해야 합니다.')

        # 아이디/비밀번호 찾기 버튼 추가
        if st.button('아이디/비밀번호 찾기'):
            st.session_state['find_account'] = not st.session_state['find_account']  # 상태 토글

    # 아이디/비밀번호 찾기 섹션
    if st.session_state['find_account']:
        tabs = st.tabs(["아이디 찾기", "비밀번호 찾기"])

        # 첫 번째 탭 (아이디 찾기)
        with tabs[0]:
            email = st.text_input("이메일을 입력하세요", key="find_id_email")
            if st.button("아이디 찾기"):
                if check_email_exists(email):
                    # 데이터베이스에서 해당 이메일의 사용자 아이디를 찾음
                    c.execute('SELECT userid FROM users WHERE email = ?', (email,))
                    user_id = c.fetchone()[0]
                    # 이메일로 아이디 전송
                    send_email(email, "아이디 찾기", f"당신의 아이디는 {user_id}입니다.")
                    st.success(f"{email}로 아이디가 전송되었습니다.")
                else:
                    st.error("등록되지 않은 이메일입니다.")

        # 두 번째 탭 (비밀번호 찾기)
        with tabs[1]:
            userid = st.text_input("아이디를 입력하세요", key="find_pw_userid")
            email = st.text_input("이메일을 입력하세요", key="find_pw_email")
            if st.button("비밀번호 찾기"):
                if check_email_exists(email):
                    # 아이디와 이메일이 일치하는 사용자 확인
                    c.execute('SELECT passwd FROM users WHERE userid = ? AND email = ?', (userid, email))
                    result = c.fetchone()
                    if result:
                        user_password = result[0]
                        # 이메일로 비밀번호 전송
                        send_email(email, "비밀번호 찾기", f"{name}({user_id})님, 당신의 비밀번호는 {user_password}입니다.")
                        st.success(f"{email}로 비밀번호가 전송되었습니다.")
                    else:
                        st.error("아이디 또는 이메일이 잘못되었습니다.")
                else:
                    st.error("등록되지 않은 이메일입니다.")

    # Registration form with email and password confirmation
    with t2:
        if st.session_state['login_status']:
            st.error('로그인 상태이므로 회원가입을 진행할 수 없습니다.')
        else:
            with st.form('회원가입'):
                userid = st.text_input('아이디 (4자 이상)', key='ruserid') # 유저 아이디
                passwd = st.text_input('비밀번호 (6자 이상)', key='rpasswd', type='password') # 비밀번호
                confirm_passwd = st.text_input('비밀번호 확인', key='rconfirm_passwd', type='password') # 비밀번호 확인
                email = st.text_input('이메일', key='remail') # 이메일
                user_type = st.radio('사용자 유형을 선택하세요', ('학생', '선생님'))  # 사용자 유형 (학생 또는 선생님)
                name = st.text_input('이름을 입력하세요', key='name') # 사용자 이름
                if st.form_submit_button('가입하기'):
                    if all([userid, passwd, confirm_passwd, email]):
                        # Check password length
                        if len(userid) < 4:
                            st.error('아이디는 4자 이상이어야 합니다. 다시 입력해주세요.')
                        elif len(passwd) < 6:
                            st.error('비밀번호는 6자 이상이어야 합니다. 다시 입력해주세요.')
                        # Check password confirmation
                        elif passwd != confirm_passwd:
                            st.error('비밀번호가 일치하지 않습니다. 다시 입력해주세요.')
                        # Check email format
                        elif not is_valid_email(email):  # 이메일 형식 체크
                            st.error('이메일은 naver.com 또는 gmail.com 형식이어야 합니다.')
                        elif check_email_exists(email):  # 이메일 기존 DB와 중복 체크
                            st.error('이미 존재하는 이메일입니다.')
                        else:
                            # Check if user already exists
                            user = check_user(userid, passwd)
                            if user:
                                st.error('이미 존재하는 사용자 ID입니다.')
                            else:
                                add_user(userid, passwd, email, user_type, name)  # 사용자 유형 추가
                                st.success('등록 성공')
                    else:
                        st.error('모든 정보를 입력해야 합니다.')

    # Admin page: Display all registered users and allow deletion
    with t3:
        if st.session_state['login_status'] and st.session_state['current_user'] == 'admin':
            st.subheader('등록된 사용자 목록')
            users = get_users()
            if users:
                df = pd.DataFrame(users, columns=['UserID', 'Password', 'Email', 'User Type', 'name'])  # Add user type column
                st.dataframe(df)

                # User deletion section
                userid_to_delete = st.selectbox('삭제할 사용자 선택', options=[user[0] for user in users])
                if st.button('삭제'):
                    # Prevent deletion of the admin user
                    if userid_to_delete == 'admin':
                        st.error('관리자 계정은 삭제할 수 없습니다.')
                    else:
                        # Confirm deletion using a checkbox
                        if 'confirm_deletion' not in st.session_state:
                            st.session_state['confirm_deletion'] = False

                        if st.session_state['confirm_deletion']:
                            delete_user(userid_to_delete)
                            st.success(f'{userid_to_delete} 사용자가 삭제되었습니다.')
                            st.session_state['confirm_deletion'] = False  # Reset confirmation
                            st.rerun()  # Refresh the app to reflect changes
                        else:
                            st.session_state['confirm_deletion'] = True
                            st.warning(f'정말로 {userid_to_delete} 사용자를 삭제하시겠습니까? 삭제를 한 번 더 클릭해 주세요.')

            else:
                st.info('등록된 사용자가 없습니다.')
        else:
            st.warning('관리자만 접근 가능합니다. 로그인 해주세요.')

# Footer
st.info('copyright(c) all rights reserved since 2024 powered by Team TOGO, developed by Woojin Jung')

# Close the database connection when done
conn.close()
