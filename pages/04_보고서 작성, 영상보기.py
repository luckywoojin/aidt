import streamlit as st # 웹 송출 모듈
import pandas as pd
import sqlite3 # 데이터베이스 연결 관련 모듈
from datetime import datetime

######################## 데이터베이스 관련 #############################

# SQLite 데이터베이스 연결, 최우선 순위!
# user.db 데이터베이스
conn = sqlite3.connect('users.db')
conn_user = conn.cursor()

# question1.db 데이터베이스
conn_2 = sqlite3.connect('question41.db')
conn_question1 = conn_2.cursor()
conn_question1.execute('''
    CREATE TABLE  IF NOT EXISTS question41 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userid TEXT NOT NULL,
        txtfile TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''') # 만약 question1.db 파일이 존재하지 않는다면 해당 형식으로 생성함.

# question2.db 데이터베이스
conn_3 = sqlite3.connect('question42.db')
conn_question2 = conn_3.cursor()
conn_question2.execute('''
    CREATE TABLE  IF NOT EXISTS question42 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userid TEXT NOT NULL,
        txtfile TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

def add_question(txtfile):
    userid = st.session_state.get('current_user')
    if not userid:
        st.error('비로그인 상태이므로 질문을 저장할 수 없습니다.')
        return
    else:
        # Insert without the timestamp column
        conn_question1.execute('INSERT INTO question41 (userid, txtfile) VALUES (?, ?)', (userid, txtfile))
        conn_2.commit()  # Commit the transaction using conn_2, the connection to question41.db
        st.success('질문이 성공적으로 저장되었습니다!')

def add_question2(txtfile):
    userid = st.session_state.get('current_user')
    if not userid:
        st.error('비로그인 상태이므로 질문을 저장할 수 없습니다.')
        return
    else:
        # Insert without the timestamp column
        conn_question2.execute('INSERT INTO question42 (userid, txtfile) VALUES (?, ?)', (userid, txtfile))
        conn_3.commit()
        st.success('질문이 성공적으로 저장되었습니다!')

# 이미지 DB 불러오기
conn = sqlite3.connect("uploaded_files.db")
cursor = conn.cursor()

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

    tabs = ['복습, 질문', '학습목표', '워드클라우드와 핵심 단어 데이터셋 비교', '인식제고영상', '학습정리', '선생님탭']
    selected_tab = st.sidebar.radio("탭 선택", tabs)

    if selected_tab == '복습, 질문':
        log_record(4,1)
        c1, c2 = st.columns((7, 3))
        with c1:
            st.write('빈페이지')
        with c2:
            st.write('빈페이지')

    elif selected_tab == '학습목표':
        log_record(4,2)
        with st.expander('학습목표'):
                st.subheader('오늘은 이러한 것을 배워봅시다.')
                txtdata = '''
        학습목표: 
    1. <br>
    2. <br>
    3.
        '''
                st.markdown(txtdata, unsafe_allow_html=True)

    elif selected_tab == '워드클라우드와 핵심 단어 데이터셋 비교':
        log_record(4,3)
        c1, c2 = st.columns((5, 5))
        with c1:
            # SQLite 데이터베이스 연결
            conn = sqlite3.connect("uploaded_files.db")
            cursor = conn.cursor()

            def get_latest_image(user_id):
                # 해당 user_id의 최신 이미지 불러오기
                cursor.execute("""
                    SELECT file_name, file_data, timestamp 
                    FROM uploaded_files 
                    WHERE user_id = ? 
                    ORDER BY timestamp DESC 
                    LIMIT 1
                """, (user_id,))
                return cursor.fetchone()

            if 'current_user' in st.session_state:  # 로그인한 사용자가 있는지 확인
                user_id = st.session_state['current_user']
                latest_image = get_latest_image(user_id)

                if latest_image:
                    file_name, file_data, timestamp = latest_image
                    st.image(file_data, caption=f"Latest image of {user_id} - {file_name} (Uploaded at {timestamp})", use_column_width=True)
                else:
                    st.warning("현재 저장된 이미지가 없습니다.")
        with c2:
            conn = sqlite3.connect('question21.db')
            conn_question21 = conn.cursor()

             # 질문 1의 자신의 답변에 대해 볼 수 있게 하는 기능
            if st.session_state['login_status'] and 'current_user' in st.session_state:
                    user_id = st.session_state['current_user']
                    st.write("자신이 작성한 대본 보기")
                    conn_question21.execute('SELECT id, txtfile, timestamp FROM question21 WHERE userid = ? ORDER BY timestamp DESC', (user_id,))
                    questions21 = conn_question21.fetchall()
                    if questions21:
                        df_questions = pd.DataFrame(questions21, columns=["ID", "Question", "Timestamp"])
                        st.dataframe(df_questions)
                    else:
                        st.warning("현재 저장된 질문이 없습니다.")

    elif selected_tab == '인식제고영상':
        log_record(4,4)
        c1, c2 = st.columns((7, 3))
        with c1:
            url = 'https://youtu.be/qyIbtz-l6q8?si=RMZ9ZJbBdqEdcvmQ'
            st.video(url)
        with c2:
            # 동영상 소감 작성   
            with st.form('mynoteform'):
                txtString = st.text_area('영상을 보고 소감을 적어봅시다.', height=200)
                if st.form_submit_button('저장하기'): 
                    if not st.session_state['login_status']:
                        st.error('비로그인 상태이므로 메모를 저장할 수 없습니다.')
                    else:
                        if txtString != '':
                            add_question(txtString)

                        else:
                            st.error('노트가 비어 있어요 ㅠㅠㅠ')   
             # 질문 1의 자신의 답변에 대해 볼 수 있게 하는 기능
            if st.session_state['login_status'] and 'current_user' in st.session_state:
                with st.expander('자신의 답변 보기'):
                    user_id = st.session_state['current_user']
                    
                    # Display only user-specific questions for question1
                    st.write("About: 질문 탭")
                    conn_question1.execute('SELECT id, txtfile, timestamp FROM question41 WHERE userid = ? ORDER BY timestamp DESC', (user_id,))
                    questions41 = conn_question1.fetchall()
                    if questions41:
                        df_questions = pd.DataFrame(questions41, columns=["ID", "Question", "Timestamp"])
                        st.dataframe(df_questions)
                    else:
                        st.warning("현재 저장된 질문이 없습니다.")
        
    elif selected_tab == '학습정리':
        log_record(4,5)
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
            with st.form('mynoteform2'):
                txtString = st.text_area('다음 시간에는 무엇을할까요?', height=200)
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
                    conn_question2.execute('SELECT id, txtfile, timestamp FROM question42 WHERE userid = ? ORDER BY timestamp DESC', (user_id,))
                    questions42 = conn_question2.fetchall()
                    if questions42:
                        df_questions = pd.DataFrame(questions42, columns=["ID", "Question", "Timestamp"])
                        st.dataframe(df_questions)
                    else:
                        st.warning("현재 저장된 질문이 없습니다.")

    elif selected_tab == '선생님탭':
        log_record(4,6)
        if st.session_state['login_status'] and st.session_state['current_user'] == 'admin':
            # 질문1 불러오기
            st.write("About: 질문 탭")
            conn_question1.execute('SELECT id, userid, txtfile, timestamp FROM question41 ORDER BY timestamp DESC')
            questions = conn_question1.fetchall()
            if questions:
                # Create a DataFrame from the fetched questions
                df_questions = pd.DataFrame(questions, columns=["ID", "User ID", "Question", "Timestamp"])

                # Display the DataFrame
                st.dataframe(df_questions)

                # Select a question to delete by ID
                question_id_to_delete = st.selectbox("지울 질문의 ID를 선택하세요.", df_questions["ID"].tolist(), key="delete_selectbox_1")
                
                # Button to delete the selected question with a unique key
                if st.button(f"질문 삭제하기 ID: {question_id_to_delete}", key=f"delete_button_1_{question_id_to_delete}"):
                    conn_question1.execute('DELETE FROM question41 WHERE id = ?', (question_id_to_delete,))
                    conn_2.commit()  # Commit the transaction
                    st.success(f'질문 ID {question_id_to_delete}이(가) 성공적으로 삭제되었습니다!')
                    # Refresh the DataFrame after deletion
                    conn_question1.execute('SELECT id, userid, txtfile, timestamp FROM question41 ORDER BY timestamp DESC')
                    questions = conn_question1.fetchall()
                    df_questions = pd.DataFrame(questions, columns=["ID", "User ID", "Question", "Timestamp"])
                    st.dataframe(df_questions)  # Display updated DataFrame
            else:
                st.warning("현재 저장된 질문이 없습니다.")

            # 질문2 불러오기
            st.write("About: 질문2 탭")
            conn_question2.execute('SELECT id, userid, txtfile, timestamp FROM question42 ORDER BY timestamp DESC')
            questions2 = conn_question2.fetchall()
            if questions2:
                # Create a DataFrame from the fetched questions
                df_questions = pd.DataFrame(questions2, columns=["ID", "User ID", "Question", "Timestamp"])

                # Display the DataFrame
                st.dataframe(df_questions)

                # 질문2 - Select a question to delete by ID with a unique key
                question_id_to_delete2 = st.selectbox("지울 질문의 ID를 선택하세요.", df_questions["ID"].tolist(), key="delete_selectbox_2")

                # Button to delete the selected question with a unique key
                if st.button(f"질문 삭제하기 ID: {question_id_to_delete2}", key=f"delete_button_2_{question_id_to_delete2}"):
                    conn_question2.execute('DELETE FROM question42 WHERE id = ?', (question_id_to_delete,))
                    conn_3.commit()  # Commit the transaction
                    st.success(f'질문 ID {question_id_to_delete}이(가) 성공적으로 삭제되었습니다!')
                    # Refresh the DataFrame after deletion
                    conn_question2.execute('SELECT id, userid, txtfile, timestamp FROM question42 ORDER BY timestamp DESC')
                    questions2 = conn_question2.fetchall()
                    df_questions = pd.DataFrame(questions2, columns=["ID", "User ID", "Question", "Timestamp"])
                    st.dataframe(df_questions)  # Display updated DataFrame
            else:
                st.warning("현재 저장된 질문이 없습니다.")

        else:
            st.error('접근권한이 없습니다.')
else:
    st.error("로그인을 먼저하세요.")
