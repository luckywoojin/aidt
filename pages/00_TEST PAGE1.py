import streamlit as st # 웹 송출 모듈
import pandas as pd
import sqlite3 # 데이터베이스 연결 관련 모듈
from datetime import datetime

######################## 데이터베이스 관련 #############################

# SQLite 데이터베이스 연결, 최우선 순위!
# user.db 데이터베이스
conn = sqlite3.connect('users.db')
conn_user = conn.cursor()

######################## 로그인 상태 확인 #############################

# 로그인 중인 유저의 정보를 가져오는 함수
def get_current_user_info(userid):
    conn_user.execute('SELECT name, email, user_type FROM users WHERE userid = ?', (userid,))
    return conn_user.fetchone()  # (name, email, user_type) 형태로 반환됨

if 'login_status' not in st.session_state: # 만약 사용자가 비로그인 상태라면.. login_status는 False.
    st.session_state['login_status'] = False

# 로그인 중인 사용자 정보 출력
if 'current_user' in st.session_state:
    user_info = get_current_user_info(st.session_state['current_user'])
    if user_info:
        name, email, user_type = user_info  # 튜플에서 이름, 이메일, 사용자 유형 추출
        user_id = st.session_state['current_user']  # current_user에서 user_id 추출
        st.success(f'{name}({user_id}) {user_type}, 접속을 환영합니다.')

#log 관련 db불러오기
l = sqlite3.connect('log.db')
log_cursor = l.cursor()  # 커서 객체 생성

def log_record(page, tab):
    date = datetime.now().isoformat()
    l.execute('INSERT INTO log (userid, name, page, tab, date) VALUES (?, ?, ?, ?, ?)', (user_id, name, page, tab, date))
    l.commit()

######################## 세부 내용 코드 #############################

if st.session_state['login_status']:
    st.subheader('4차시: 분석을 기반으로한 보고서 작성, 인식제고영상 보기')

    # 모든 탭 메뉴를 사이드바에 라디오 버튼으로 표시
    tabs = ['서브1', '서브2', '서브3', '서브4', '서브5', '선생님탭']
    selected_tab = st.sidebar.radio("탭 선택", tabs)

    if selected_tab == '서브1':
        log_record(0,1)
        c1, c2 = st.columns((7, 3))
        with c1:
            st.write('빈페이지')
        with c2:
            st.write('빈페이지')

    elif selected_tab == '서브2':
        log_record(0,2)
        with st.expander('학습목표'):
                st.subheader('오늘은 이러한 것을 배워봅시다.')
                txtdata = '''
                학습목표: 
                1. <br>
                2. <br>
                3.
                '''
                st.markdown(txtdata, unsafe_allow_html=True)
    elif selected_tab == '서브3':
        log_record(0,3)
        st.write('빈페이지')

    elif selected_tab == '서브4':
        log_record(0,4)
        st.success('서브4입니다.')
        c1, c2 = st.columns((7, 3))
        with c1:
            url = 'https://youtu.be/qyIbtz-l6q8?si=RMZ9ZJbBdqEdcvmQ'
            st.video(url)
        with c2:
            st.write('미정')    

    elif selected_tab == '서브5':
        log_record(0,5)
        c1, c2 = st.columns((7, 3))
        with c1:
            with st.expander('오늘의 학습을 정리해봅시다.'):
                st.subheader('오늘은 이러한 활동을 했습니다.')
                txtdata = '''
        1. <br>
        2. <br>
        3.
        '''
                st.markdown(txtdata, unsafe_allow_html=True)

            with st.expander('다음에는 어떤 활동을 할까요?'):
                st.subheader('다음에는 이러한 활동을 할 것입니다.')
                txtdata = '''
        1. <br>
        2. <br>
        '''
                st.markdown(txtdata, unsafe_allow_html=True)
        with c2:
            st.write('미정')

    elif selected_tab == '선생님탭':
        log_record(0,6)
        if st.session_state['login_status'] and st.session_state['current_user'] == 'admin':
            st.subheader("로그 조회 및 관리")

            # 사용자 선택으로 로그 조회
            log_cursor.execute("SELECT DISTINCT userid FROM log")
            users = [user[0] for user in log_cursor.fetchall()]
            selected_user = st.selectbox("사용자별 로그 조회", users)

            if st.button("로그 조회"):
                user_logs = pd.read_sql_query(f"SELECT * FROM log WHERE userid = '{selected_user}'", l)
                st.write(f"{selected_user}의 로그 기록")
                st.dataframe(user_logs)

            # 전체 로그 삭제 버튼
            if st.button("전체 로그 삭제"):
                log_cursor.execute("DELETE FROM log")
                l.commit()
                st.warning("모든 로그 기록이 삭제되었습니다.")
else:
    st.error("로그인을 먼저하세요.")