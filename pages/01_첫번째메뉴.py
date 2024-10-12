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

st.subheader('첫번째 메뉴입니다.')
t1, t2, t3 = st.tabs(['서브1', '서브2', '서브3'])

with t1:
    

    c1, c2 = st.columns((7, 3))
    with c1:
        with st.expander('교과내용1'):
            st.subheader('저작권이란?')
            txtdata = '''
    저작권이란 시, 소설, 음악, 미술, 영화, 연극, 컴퓨터프로그램 등과 같은 ‘저작물’에 대하여 창작자가 가지는 권리를 말한다. 예를 들면, 소설가가 소설작품을 창작한 경우에 그는 원고 그대로 출판·배포할 수 있는 복제·배포권과 함께 그 소설을 영화나 번역물 등과 같이 다른 형태로 저작할 수 있는 2차적저작물 작성권, 연극 등으로 공연할 수 있는 공연권, 방송물로 만들어 방송할 수 있는 방송권 등 여러 가지의 권리를 가지게 된다. 이러한 여러 가지 권리의 전체를 저작권이라고 하는데, 이러한 저작권은 크게 저작재산권과 저작인격권으로 나누어 볼 수 있다.

    저작권은 토지와 같은 부동산과 마찬가지로 매매하거나 상속할 수 있고, 다른 사람에게 빌려 줄 수도 있다. 만일 어떤 사람이 허락을 받지 않고 타인의 저작물을 사용한다면 저작권자는 그를 상대로 민사상의 손해배상을 청구할 수 있고, 그 침해자에 대하여 형사상 처벌을 요구(고소)할 수도 있다. 저작권자는 일반적으로 저작권을 다른 사람에게 양도하거나 다른 사람에게 자신의 저작물을 사용할 수 있도록 허락함으로써 경제적인 대가를 받을 수 있다. 이러한 저작권의 경제적 측면을 저작재산권이라고 한다.
    '''
            st.markdown(txtdata)
    with c2:
        with st.expander('Tips...'):
            st.info(' 2차적저작물')
            st.write('① 원저작물을 번역·편곡·변형·각색·영상제작 그 밖의 방법으로 작성한 창작물(이하 "2차적저작물"이라 한다)은 독자적인 저작물로서 보호된다. ② 2차적저작물의 보호는 그 원저작물의 저작자의 권리에 영향을 미치지 아니한다.')
with t2:
    st.success('서브2입니다.')
with t3:
    st.success('서브3입니다.')
