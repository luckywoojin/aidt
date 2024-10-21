import streamlit as st # 웹 송출 모듈
import pandas as pd
import sqlite3 # 데이터베이스 연결 관련 모듈

######################## 데이터베이스 관련 #############################

# SQLite 데이터베이스 연결, 최우선 순위!
# user.db 데이터베이스
conn = sqlite3.connect('users.db')
conn_user = conn.cursor()

st.set_page_config(page_title='정보통신기술(ICT) 기반 장애 인식 개선 교육 프로그램', layout='wide')

# question1.db 데이터베이스
conn_2 = sqlite3.connect('question1.db')
conn_question1 = conn_2.cursor()
conn_question1.execute('''
    CREATE TABLE  IF NOT EXISTS question1 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userid TEXT NOT NULL,
        txtfile TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''') # 만약 question1.db 파일이 존재하지 않는다면 해당 형식으로 생성함.

# question2.db 데이터베이스
conn_3 = sqlite3.connect('question2.db')
conn_question2 = conn_3.cursor()
conn_question2.execute('''
    CREATE TABLE  IF NOT EXISTS question2 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userid TEXT NOT NULL,
        txtfile TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

# question3.db 데이터베이스
conn_4 = sqlite3.connect('question3.db')
conn_question3 = conn_4.cursor()
conn_question3.execute('''
    CREATE TABLE  IF NOT EXISTS question3 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userid TEXT NOT NULL,
        txtfile TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

######################## 로그인 상태 확인 #############################

# 로그인 중인 유저의 정보를 가져오는 함수
def get_current_user_info(userid):
    conn_user.execute('SELECT email, user_type FROM users WHERE userid = ?', (userid,))
    return conn_user.fetchone()  # (email, user_type) 형태로 반환됨

if 'login_status' not in st.session_state: # 만약 사용자가 비로그인 상태라면.. login_status는 False.
    st.session_state['login_status'] = False

def add_question(txtfile):
    userid = st.session_state.get('current_user')
    if not userid:
        st.error('비로그인 상태이므로 질문을 저장할 수 없습니다.')
        return
    else:
        # Insert without the timestamp column
        conn_question1.execute('INSERT INTO question1 (userid, txtfile) VALUES (?, ?)', (userid, txtfile))
        conn_2.commit()  # Commit the transaction using conn_2, the connection to question1.db
        st.success('질문이 성공적으로 저장되었습니다!')

def add_question2(txtfile):
    userid = st.session_state.get('current_user')
    if not userid:
        st.error('비로그인 상태이므로 질문을 저장할 수 없습니다.')
        return
    else:
        # Insert without the timestamp column
        conn_question2.execute('INSERT INTO question2 (userid, txtfile) VALUES (?, ?)', (userid, txtfile))
        conn_3.commit()
        st.success('질문이 성공적으로 저장되었습니다!')

def add_question3(txtfile):
    userid = st.session_state.get('current_user')
    if not userid:
        st.error('비로그인 상태이므로 질문을 저장할 수 없습니다.')
        return
    else:
        # Insert without the timestamp column
        conn_question3.execute('INSERT INTO question3 (userid, txtfile) VALUES (?, ?)', (userid, txtfile))
        conn_4.commit()
        st.success('질문이 성공적으로 저장되었습니다!')

# 로그인 중인 사용자 정보 출력
if 'current_user' in st.session_state:
    user_info = get_current_user_info(st.session_state['current_user'])
    if user_info:
        email, user_type = user_info  # 튜플에서 이메일과 사용자 유형 추출
        st.success(f'로그인한 사용자: {st.session_state["current_user"]}, 이메일: {email}, 사용자 유형: {user_type}')


######################## 여기부터 진짜 페이지 구성 시작 #############################

if st.session_state['login_status']:
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
            # 공부할거 같은 내용을 답변    
            with st.form('mynoteform'):
                txtString = st.text_area('무엇을 공부할거 같은가요?', height=200)
                if st.form_submit_button('저장하기'): 
                    if not st.session_state['login_status']:
                        st.error('비로그인 상태이므로 메모를 저장할 수 없습니다.')
                    else:
                        if txtString != '':
                            add_question(txtString)

                        else:
                            st.error('노트가 비어 있어요 ㅠㅠㅠ')  

            with st.expander('설문조사 해보기'):
                st.subheader('설문조사를 하기 위해 아래 링크로 접속하세요.')
                import streamlit.components.v1 as components
                url = 'https://forms.gle/RaPfUoT7fRRKiAfFA'
                components.iframe(url, width=600, height=768)
        with c2:
            with st.expander('Tips...'):
                st.info('장애인에 관하여 생각해볼 때는..')
                txtdata = '''
    우선 학교에서 마주친 장애인 친구에 대해 이야기 해봅시다.<br>
    만약 없다면, 학교 외에서 만난 장애인도 좋습니다.<br>
    또, 시각 장애인, 청각 장애인, 지체 장애인, 신체 장애인 등
    여러가지 부류의 장애인 친구에 대해서도 생각해봅시다.
                '''
                st.markdown(txtdata, unsafe_allow_html=True)

            # 질문 1의 자신의 답변에 대해 볼 수 있게 하는 기능
            if st.session_state['login_status'] and 'current_user' in st.session_state:
                with st.expander('자신의 답변 보기'):
                    user_id = st.session_state['current_user']
                    
                    # Display only user-specific questions for question1
                    st.write("About: 질문 탭")
                    conn_question1.execute('SELECT id, txtfile, timestamp FROM question1 WHERE userid = ? ORDER BY timestamp DESC', (user_id,))
                    questions11 = conn_question1.fetchall()
                    if questions11:
                        df_questions = pd.DataFrame(questions11, columns=["ID", "Question", "Timestamp"])
                        st.dataframe(df_questions)
                    else:
                        st.warning("현재 저장된 질문이 없습니다.")
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
            url = 'https://www.youtube.com/watch?v=7CtP9Ta3-ww&t=2s'
            st.video(url)
        with c2:
            with st.form('mynoteform2'):
                txtString = st.text_area('영상에 대한 의견을 적어봅시다.', height=200)
                if st.form_submit_button('저장하기'): 
                    if not st.session_state['login_status']:
                        st.error('비로그인 상태이므로 메모를 저장할 수 없습니다.')
                    else:
                        if txtString != '':
                            add_question2(txtString)

                        else:
                            st.error('노트가 비어 있어요 ㅠㅠㅠ')
            # 질문 2의 자신의 답변에 대해 볼 수 있게 하는 기능
            if st.session_state['login_status'] and 'current_user' in st.session_state:
                with st.expander('자신의 답변 보기'):
                    user_id = st.session_state['current_user']
                    
                    # Display only user-specific questions for question1
                    st.write("About: 질문 탭")
                    conn_question2.execute('SELECT id, txtfile, timestamp FROM question2 WHERE userid = ? ORDER BY timestamp DESC', (user_id,))
                    questions22 = conn_question2.fetchall()
                    if questions22:
                        df_questions = pd.DataFrame(questions22, columns=["ID", "Question", "Timestamp"])
                        st.dataframe(df_questions)
                    else:
                        st.warning("현재 저장된 질문이 없습니다.")
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
                txtString = st.text_area('1차시를 마치며 소감 한마디를 적어주세요.', height=200)
                if st.form_submit_button('저장하기'): 
                    if not st.session_state['login_status']:
                        st.error('비로그인 상태이므로 메모를 저장할 수 없습니다.')
                    else:
                        if txtString != '':
                            add_question3(txtString)

                        else:
                            st.error('노트가 비어 있어요 ㅠㅠㅠ')  
            # 질문 3의 자신의 답변에 대해 볼 수 있게 하는 기능
            if st.session_state['login_status'] and 'current_user' in st.session_state:
                with st.expander('자신의 답변 보기'):
                    user_id = st.session_state['current_user']
                    
                    # Display only user-specific questions for question1
                    st.write("About: 질문 탭")
                    conn_question3.execute('SELECT id, txtfile, timestamp FROM question3 WHERE userid = ? ORDER BY timestamp DESC', (user_id,))
                    questions33 = conn_question3.fetchall()
                    if questions33:
                        df_questions = pd.DataFrame(questions33, columns=["ID", "Question", "Timestamp"])
                        st.dataframe(df_questions)
                    else:
                        st.warning("현재 저장된 질문이 없습니다.")

    with t5:
        if st.session_state['login_status'] and st.session_state['current_user'] == 'admin':
            with st.expander('이 탭이 무엇인지 궁금하신가요?'):
                st.subheader('여기는..')
                txtdata = '''
                선생님 권한을 가진 admin 유저가 학생들의 답을 볼 수 있는 공간입니다.
                '''
                st.markdown(txtdata, unsafe_allow_html=True)

            # 질문1 불러오기
            st.write("About: 질문 탭")
            conn_question1.execute('SELECT id, userid, txtfile, timestamp FROM question1 ORDER BY timestamp DESC')
            questions = conn_question1.fetchall()
            if questions:
                # Create a DataFrame from the fetched questions
                df_questions = pd.DataFrame(questions, columns=["ID", "User ID", "Question", "Timestamp"])

                # Display the DataFrame
                st.dataframe(df_questions)

                # Select a question to delete by ID
                question_id_to_delete = st.selectbox("지울 질문의 ID를 선택하세요.", df_questions["ID"].tolist())

                # Button to delete the selected question
                if st.button(f"질문 삭제하기 ID: {question_id_to_delete}", key=f"delete_button_{question_id_to_delete}"):
                    conn_question1.execute('DELETE FROM question1 WHERE id = ?', (question_id_to_delete,))
                    conn_2.commit()  # Commit the transaction
                    st.success(f'질문 ID {question_id_to_delete}이(가) 성공적으로 삭제되었습니다!')
                    # Refresh the DataFrame after deletion
                    conn_question1.execute('SELECT id, userid, txtfile, timestamp FROM question1 ORDER BY timestamp DESC')
                    questions = conn_question1.fetchall()
                    df_questions = pd.DataFrame(questions, columns=["ID", "User ID", "Question", "Timestamp"])
                    st.dataframe(df_questions)  # Display updated DataFrame
            else:
                st.warning("현재 저장된 질문이 없습니다.")

            # 질문2 불러오기
            st.write("About: 질문2 탭")
            conn_question2.execute('SELECT id, userid, txtfile, timestamp FROM question2 ORDER BY timestamp DESC')
            questions2 = conn_question2.fetchall()
            if questions2:
                # Create a DataFrame from the fetched questions
                df_questions = pd.DataFrame(questions2, columns=["ID", "User ID", "Question", "Timestamp"])

                # Display the DataFrame
                st.dataframe(df_questions)

                # Select a question to delete by ID
                question_id_to_delete = st.selectbox("지울 질문의 ID를 선택하세요.", df_questions["ID"].tolist())

                # Button to delete the selected question
                if st.button(f"질문 삭제하기 ID: {question_id_to_delete}", key=f"delete_button2_{question_id_to_delete}"):
                    conn_question2.execute('DELETE FROM question2 WHERE id = ?', (question_id_to_delete,))
                    conn_3.commit()  # Commit the transaction
                    st.success(f'질문 ID {question_id_to_delete}이(가) 성공적으로 삭제되었습니다!')
                    # Refresh the DataFrame after deletion
                    conn_question2.execute('SELECT id, userid, txtfile, timestamp FROM question2 ORDER BY timestamp DESC')
                    questions2 = conn_question2.fetchall()
                    df_questions = pd.DataFrame(questions2, columns=["ID", "User ID", "Question", "Timestamp"])
                    st.dataframe(df_questions)  # Display updated DataFrame
            else:
                st.warning("현재 저장된 질문이 없습니다.")

            # 질문3 불러오기
            st.write("About: 질문3 탭")
            conn_question3.execute('SELECT id, userid, txtfile, timestamp FROM question3 ORDER BY timestamp DESC')
            questions3 = conn_question3.fetchall()
            if questions3:
                # Create a DataFrame from the fetched questions
                df_questions = pd.DataFrame(questions3, columns=["ID", "User ID", "Question", "Timestamp"])

                # Display the DataFrame
                st.dataframe(df_questions)

                # Select a question to delete by ID
                question_id_to_delete = st.selectbox("지울 질문의 ID를 선택하세요.", df_questions["ID"].tolist())

                # Button to delete the selected question
                if st.button(f"질문 삭제하기 ID: {question_id_to_delete}", key=f"delete_button3_{question_id_to_delete}"):
                    conn_question3.execute('DELETE FROM question3 WHERE id = ?', (question_id_to_delete,))
                    conn_4.commit()  # Commit the transaction
                    st.success(f'질문 ID {question_id_to_delete}이(가) 성공적으로 삭제되었습니다!')
                    # Refresh the DataFrame after deletion
                    conn_question3.execute('SELECT id, userid, txtfile, timestamp FROM question3 ORDER BY timestamp DESC')
                    questions3 = conn_question3.fetchall()
                    df_questions = pd.DataFrame(questions3, columns=["ID", "User ID", "Question", "Timestamp"])
                    st.dataframe(df_questions)  # Display updated DataFrame
            else:
                st.warning("현재 저장된 질문이 없습니다.")
        else:
            st.error("접근권한이 없습니다.")
else:
    st.error("로그인을 먼저하세요.")

    if st.session_state['login_status']:
         st.error("로그인을 먼저하세요.")
