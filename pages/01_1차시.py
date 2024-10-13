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

st.subheader('1차시: 장애인 교육 오리엔테이션')
t1, t2, t3, t4, t5 = st.tabs(['질문', '학습목표', '영상시청/감상나누기', '학습정리', '선생님탭'])

with t1:
    st.success('서브1입니다.')
    c1, c2 = st.columns((7, 3))
    with c1:
        with st.expander('학생들에게 뭅습니다.'):
            st.subheader('여러분은 장애인에 대한 기억이 있나요?')
            txtdata = '''
    장애인에 관해서 조금 이야기를 나눠봅시다.<br>
    그림에 무엇이 보이나요? (사실 확인)<br>
    이러한 장애인 학생과 같이 학교를 다녀본 경험이 있나요? (열린 물음)<br>
    제시된 그림을 참고하면, 이번시간에 무엇에 대해 공부할 것 같은가요?
    '''
            st.markdown(txtdata, unsafe_allow_html=True)
        with st.form('mynoteform'):
            txtString = st.text_area('무엇을 공부할거 같은가요?', height=200)
            if st.form_submit_button('저장하기'): 
                if txtString != '':
                    st.info(txtString + '<BR>저장되었습니다.', unsafe_allow_html=True)
                else:
                    st.error('노트가 비어 있어요 ㅠㅠㅠ')  

        with st.expander('설문조사 해보기'):
            st.subheader('설문조사를 하기 위해 아래 링크로 접속하세요.')
            txtdata = '''
    통합교육을_실시하는_초등학교_학생의_장애학생에_대한_인식<br>
    위 pdf에 따라 질문을 구성하여 설문조사를 할 예정입니다.<br>
    구글 설문지를 이용할 수도 있고, 사이트 내에 항목을 만들 수도 있을거 같습니다.<br>
    '''
            st.markdown(txtdata, unsafe_allow_html=True)  
    with c2:
        with st.expander('Tips...'):
            st.info('장애인에 관하여 생각해볼 때는..')
            txtdata2 = '''
우선 학교에서 마주친 장애인 친구에 대해 이야기 해봅시다.<br>
만약 없다면, 학교 외에서 만난 장애인도 좋습니다.<br>
또, 시각 장애인, 청각 장애인, 지체 장애인, 신체 장애인 등
여러가지 부류의 장애인 친구에 대해서도 생각해봅시다.
            '''
            st.markdown(txtdata, unsafe_allow_html=True)
with t2:
    st.success('서브2입니다.')
    c1, c2 = st.columns((7, 3))
    with st.expander('학습목표'):
            st.subheader('오늘은 이러한 것을 배워봅시다.')
            txtdata = '''
    학습목표: 
학생은 장애학생의 경험을 깊이 이해하고, 포용적 태도와 존중 문화를 형성한다.<br>
또한 정보통신기술을 활용해, 데이터 분석 능력을 키우며 다양한 관점을 비판적 사고를 할 수 있다. (기대효과였던 것)
    '''
            st.markdown(txtdata, unsafe_allow_html=True)
    with st.expander('앞으로 배울 것 소개'):
            st.subheader('앞으로 6차시 동안 이러한 것을 배울 것입니다.')
            txtdata = '''
    1차시:<br>
    2차시:<br>
    3차시:<br>
    4차시:<br>
    5차시:<br>
    6차시:
    '''
            st.markdown(txtdata, unsafe_allow_html=True) # unsafe이하는 txtdata내에서 <br>표시를 해주면 줄바꿈으로 인식하도록 해줌.

with t3:
    st.success('서브3입니다.')
    c1, c2 = st.columns((7, 3))
    with c1:
        url = 'https://youtu.be/qyIbtz-l6q8?si=RMZ9ZJbBdqEdcvmQ'
        st.video(url)
    with c2:
        with st.form('mynoteform2'):
            txtString = st.text_area('영상에 대한 의견을 적어봅시다!', height=200)
            if st.form_submit_button('저장하기'): 
                if txtString != '':
                    st.info(txtString + '<BR>저장되었습니다.', unsafe_allow_html=True)
                else:
                    st.error('노트가 비어 있어요 ㅠㅠㅠ')
with t4:
    st.success('서브4입니다.')
    c1, c2 = st.columns((7, 3))
    with c1:
        with st.expander('오늘의 학습을 정리해봅시다.'):
            st.subheader('오늘은 이러한 활동을 했습니다.')
            txtdata = '''
    1. 장애인에 대해 생각해보기<br>
    2. 장애학생과 관련된 VR영상보기<br>
    3. 영상 보고 감회 나누기<br>
    이러한 것들을 해보았는데, 어땠나요? 오른쪽 탭에 적어보아요.
    '''
            st.markdown(txtdata, unsafe_allow_html=True)
        with st.expander('다음에는 어떤 활동을 할까요?'):
            st.subheader('다음에는 이러한 활동을 할 것입니다.')
            txtdata = '''
    다음 차시에서는 다시 한번 영상을 보면서 그 녹취록을 작성하여<br>
    단어 리스트를 만들어보는 활동을 할 것입니다.
    '''
            st.markdown(txtdata, unsafe_allow_html=True)
    with c2:
        with st.form('mynoteform3'):
            txtString = st.text_area('오늘 한 차시를 마무리 하며.. 소감 한마디', height=200)
            if st.form_submit_button('저장하기'): 
                if txtString != '':
                    st.info(txtString + '<BR>저장되었습니다.', unsafe_allow_html=True)
                else:
                    st.error('노트가 비어 있어요 ㅠㅠㅠ')
with t5:
    with st.expander('이 탭이 무엇인지 궁금하신가요?'):
        st.subheader('여기는..')
        txtdata = '''
    여기는 나중에 선생님 권한을 가진 사람이 학생의 답들을 열람할 수 있도록 하겠습니다.
    '''
        st.markdown(txtdata, unsafe_allow_html=True)
