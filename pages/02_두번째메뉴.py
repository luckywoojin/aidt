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


st.subheader('두번째 메뉴입니다.')

t1, t2, t3 = st.tabs(['서브21', '서브22', '서브23'])
with t1:
    st.success('서브21입니다.')
    c1, c2 = st.columns((7, 3))
    with c1:
        url = 'https://youtu.be/qyIbtz-l6q8?si=RMZ9ZJbBdqEdcvmQ'
        st.video(url)
    with c2:
        with st.form('mynoteform'):
            txtString = st.text_area('정리하기', height=200)
            if st.form_submit_button('저장하기'): 
                if txtString != '':
                    st.info(txtString + '<BR>저장되었습니다.', unsafe_allow_html=True)
                else:
                    st.error('노트가 비어 있어요 ㅠㅠㅠ')
with t2:
    st.success('서브22입니다.')
with t3:
    st.success('서브23입니다.')