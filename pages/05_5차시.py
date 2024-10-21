import streamlit as st # 웹 송출 모듈
import pandas as pd
import sqlite3 # 데이터베이스 연결 관련 모듈

######################## 데이터베이스 관련 #############################

# SQLite 데이터베이스 연결, 최우선 순위!
# user.db 데이터베이스
conn = sqlite3.connect('users.db')
conn_user = conn.cursor()

######################## 로그인 상태 확인 #############################

# 로그인 중인 유저의 정보를 가져오는 함수
def get_current_user_info(userid):
    conn_user.execute('SELECT email, user_type FROM users WHERE userid = ?', (userid,))
    return conn_user.fetchone()  # (email, user_type) 형태로 반환됨

if 'login_status' not in st.session_state: # 만약 사용자가 비로그인 상태라면.. login_status는 False.
    st.session_state['login_status'] = False

# 로그인 중인 사용자 정보 출력
if 'current_user' in st.session_state:
    user_info = get_current_user_info(st.session_state['current_user'])
    if user_info:
        email, user_type = user_info  # 튜플에서 이메일과 사용자 유형 추출
        st.success(f'로그인한 사용자: {st.session_state["current_user"]}, 이메일: {email}, 사용자 유형: {user_type}')

if st.session_state['login_status']:
    st.subheader('5차시: 패들랫을 토대로 브레인스토밍하고 발표 준비하기')

    t1, t2, t3, t4, t5, t6 = st.tabs(['복습, 질문', '학습목표', '패들랫 브레인 스토밍', '발표준비하기', '학습정리', '선생님탭'])

    with t1:
        st.success('서브1입니다.')
        c1, c2 = st.columns((7, 3))
        with c1:
            st.write('빈페이지')
        with c2:
            st.write('빈페이지')

    with t2:
        st.success('서브2입니다.')
        with st.expander('학습목표'):
                st.subheader('오늘은 이러한 것을 배워봅시다.')
                txtdata = '''
        학습목표: 
    1. <br>
    2. <br>
    3.
        '''
                st.markdown(txtdata, unsafe_allow_html=True)

    with t3:
        st.success('서브3입니다.')
        st.write('빈페이지')

    with t4:
        st.success('서브4입니다.')
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

    with t5:
        st.success('서브5입니다.')
        st.write('빈페이지')

    with t6:
        if st.session_state['login_status'] and st.session_state['current_user'] == 'admin':
            st.write('빈페이지')
        else:
            st.error('접근권한이 없습니다.')
else:
    st.error("로그인을 먼저하세요.")
