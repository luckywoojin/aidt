import streamlit as st
import sqlite3


# SQLite 데이터베이스 연결
conn = sqlite3.connect('users.db')
c = conn.cursor()

st.set_page_config(page_title='정보통신기술(ICT) 기반 장애 인식 개선 교육 프로그램', layout='wide')

# 로그인 중인 유저의 정보를 가져오는 함수
def get_current_user_info(userid):
    c.execute('SELECT email, user_type FROM users WHERE userid = ?', (userid,))
    return c.fetchone()  # (email, user_type) 형태로 반환됨

# 로그인 중인 사용자 정보 출력
if 'current_user' in st.session_state:
    user_info = get_current_user_info(st.session_state['current_user'])
    if user_info:
        email, user_type = user_info  # 튜플에서 이메일과 사용자 유형 추출
        st.success(f'로그인한 사용자: {st.session_state["current_user"]}, 이메일: {email}, 사용자 유형: {user_type}')
    else:
        st.warning('로그인 상태가 아닙니다.')
else:
    st.warning('로그인 상태가 아닙니다.')


st.subheader('네번째 메뉴입니다.')
t1, t2, t3 = st.tabs(['서브31', '서브32', '서브33'])
with t1:
    st.success('서브31입니다.')
with t2:
    st.success('서브32입니다.')
with t3:
    st.success('서브33입니다.')