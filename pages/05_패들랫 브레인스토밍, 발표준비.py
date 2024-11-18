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

# 사용자 정보 가져오기 함수
def get_users():
    conn_user.execute('SELECT userid, passwd, email, user_type, name FROM users')  # 모든 열을 명시적으로 선택
    return conn_user.fetchall()

#log 관련 db불러오기
l = sqlite3.connect('log.db')
log_cursor = l.cursor()  # 커서 객체 생성

def log_record(page, tab):
    date = datetime.now().isoformat()
    l.execute('INSERT INTO log (userid, name, page, tab, date) VALUES (?, ?, ?, ?, ?)', (user_id, name, page, tab, date))
    l.commit()

######################## 여기부터 진짜 페이지 구성 시작 #############################

if st.session_state['login_status']:
    st.subheader('5차시: 패들랫을 토대로 브레인스토밍하고 발표 준비하기')

    tabs = ['복습, 질문', '학습목표', '패들랫 브레인 스토밍', '발표준비하기', '학습정리', '선생님탭']
    selected_tab = st.sidebar.radio("탭 선택", tabs)

    if selected_tab == '복습, 질문':
        log_record(5,1)
        c1, c2 = st.columns((7, 3))
        with c1:
            st.write('빈페이지')
        with c2:
            st.write('빈페이지')

    elif selected_tab == '학습목표':
        log_record(5,2)
        with st.expander('학습목표'):
                st.subheader('오늘은 이러한 것을 배워봅시다.')
                txtdata = '''
        학습목표: 
    1. <br>
    2. <br>
    3.
        '''
                st.markdown(txtdata, unsafe_allow_html=True)

    elif selected_tab == '패들랫 브레인 스토밍':
        log_record(5,3)
        import streamlit.components.v1 as components
        url = 'https://padlet.com/asdsadasda/padlet-xlvwdduymrs9vu7l'
        components.iframe(url, width=1024, height=768)

        st.markdown("[패들랫 바로가기(로그인하려면 여기로)](https://padlet.com/asdsadasda/padlet-xlvwdduymrs9vu7l)", unsafe_allow_html=True)

    elif selected_tab == '발표준비하기':
        log_record(5,4)
        c1, c2 = st.columns((7, 3))
        with c1:
            st.write('미정')
        with c2:
            st.write('미정')

    elif selected_tab == '학습정리':
        log_record(5,5)
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

    elif selected_tab == '선생님탭':
        log_record(5,6)
        if st.session_state['login_status'] and st.session_state['current_user'] == 'admin':
            st.write('빈페이지')
        else:
            st.error('접근권한이 없습니다.')
else:
    st.error("로그인을 먼저하세요.")
