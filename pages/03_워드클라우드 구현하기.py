import streamlit as st # 웹 송출 모듈
import pandas as pd
import sqlite3 # 데이터베이스 연결 관련 모듈
from datetime import datetime

######################## 데이터베이스 관련 #############################

# SQLite 데이터베이스 연결, 최우선 순위!
# user.db 데이터베이스
conn = sqlite3.connect('users.db')
conn_user = conn.cursor()

# question31.db 데이터베이스
conn_1 = sqlite3.connect('question31.db')
conn_question1 = conn_1.cursor()
conn_question1.execute('''
    CREATE TABLE  IF NOT EXISTS question31 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userid TEXT NOT NULL,
        txtfile TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

# question32.db 데이터베이스 - 사실 tab3에는 존재하지 않으나 추후 추가할 것을 대비.
conn_2 = sqlite3.connect('question32.db')
conn_question2 = conn_2.cursor()
conn_question2.execute('''
    CREATE TABLE  IF NOT EXISTS question32 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userid TEXT NOT NULL,
        txtfile TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

# question33.db 데이터베이스
conn_3 = sqlite3.connect('question33.db')
conn_question3 = conn_3.cursor()
conn_question3.execute('''
    CREATE TABLE  IF NOT EXISTS question33 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userid TEXT NOT NULL,
        txtfile TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

def add_question3(txtfile):
    userid = st.session_state.get('current_user')
    if not userid:
        st.error('비로그인 상태이므로 질문을 저장할 수 없습니다.')
        return
    else:
        # Insert without the timestamp column
        conn_question3.execute('INSERT INTO question33 (userid, txtfile) VALUES (?, ?)', (userid, txtfile))
        conn_3.commit()
        st.success('질문이 성공적으로 저장되었습니다!')

def add_question2(txtfile):
    userid = st.session_state.get('current_user')
    if not userid:
        st.error('비로그인 상태이므로 질문을 저장할 수 없습니다.')
        return
    else:
        # Insert without the timestamp column
        conn_question2.execute('INSERT INTO question32 (userid, txtfile) VALUES (?, ?)', (userid, txtfile))
        conn_2.commit()
        st.success('질문이 성공적으로 저장되었습니다!')

def add_question(txtfile):
    userid = st.session_state.get('current_user')
    if not userid:
        st.error('비로그인 상태이므로 질문을 저장할 수 없습니다.')
        return
    else:
        # Insert without the timestamp column
        conn_question1.execute('INSERT INTO question31 (userid, txtfile) VALUES (?, ?)', (userid, txtfile))
        conn_1.commit()  # Commit the transaction using conn_2, the connection to question31.db
        st.success('질문이 성공적으로 저장되었습니다!')

# SQLite 데이터베이스 연결 (파일명: uploaded_files.db)
conn = sqlite3.connect("uploaded_files.db")
cursor = conn.cursor()
        
######################## 로그인 상태 확인 #############################

# 로그인 중인 유저의 정보를 가져오는 함수
def get_current_user_info(userid):
    conn_user.execute('SELECT name, email, user_type FROM users WHERE userid = ?', (userid,))
    return conn_user.fetchone()  # (name, email, user_type) 형태로 반환됨

if 'login_status' not in st.session_state: # 만약 사용자가 비로그인 상태라면.. login_status는 False.
    st.session_state['login_status'] = False

if 'uploaded_files' not in st.session_state:
    st.session_state['uploaded_files'] = []

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
    st.subheader('3차시: 데이터셋 기반으로 워드클라우드 해보기')
    # 모든 탭 메뉴를 사이드바에 라디오 버튼으로 표시
    tabs = ['복습, 질문', '학습목표', '워드클라우드란', '워드 클라우드 생성기', '코랩으로 워드 클라우드 만들기', '학습정리', '선생님탭']
    selected_tab = st.sidebar.radio("탭 선택", tabs)

    if selected_tab == '복습, 질문':
        log_record(3,1)
        st.subheader("전차시 복습")
        c1, c2 = st.columns((7, 3))
        with c1:
            st.image('./images/01_studied_thing.png')
            st.image('./images/01_studied_thing_answer.png')
        with c2:
            # 공부할거 같은 내용을 답변    
            with st.form('mynoteform'):
                txtString = st.text_area('어떤 것을 학습할 것 같나요?', height=200)
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
                    conn_question1.execute('SELECT id, txtfile, timestamp FROM question31 WHERE userid = ? ORDER BY timestamp DESC', (user_id,))
                    questions11 = conn_question1.fetchall()
                    if questions11:
                        df_questions = pd.DataFrame(questions11, columns=["ID", "Question", "Timestamp"])
                        st.dataframe(df_questions)
                    else:
                        st.warning("현재 저장된 질문이 없습니다.")

    elif selected_tab == '학습목표':
        log_record(3,2)
        st.subheader("학습목표")
        c1, c2 = st.columns((7, 3))
        with c1:
            st.image('./images/02_learning_index.png')

    elif selected_tab == '워드클라우드란':
        log_record(3,3)
        st.subheader("워드 클라우드란?")
        c1, c2 = st.columns((7, 3))
        with c1:
            st.image('./images/03_what_is_this.png')
            st.image('./images/03_wordcloud1.png')
            st.image('./images/03_wordcloud2.png')
            st.image('./images/03_wordcloud3.png')
            st.image('./images/03_wordcloud4.png')
        with c2:
            # 워드 클라우드에 관한 내용을 메모하도록 유도    
            with st.form('mynoteform'):
                txtString = st.text_area('학습 메모', height=200)
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
                    conn_question2.execute('SELECT id, txtfile, timestamp FROM question32 WHERE userid = ? ORDER BY timestamp DESC', (user_id,))
                    questions22 = conn_question2.fetchall()
                    if questions22:
                        df_questions = pd.DataFrame(questions22, columns=["ID", "Question", "Timestamp"])
                        st.dataframe(df_questions)
                    else:
                        st.warning("현재 저장된 질문이 없습니다.")
    
    elif selected_tab == '워드 클라우드 생성기':
        log_record(3,4)
        st.subheader("<실습 1> 워드 클라우드 생성기")
        st.markdown("[구글 드라이브 링크 (팀 공유 폴더)](https://drive.google.com/drive/folders/1eSEK2nEWM030_td1KuDUQiC1kOpm4cmP)", unsafe_allow_html=True)
        c1, c2 = st.columns((7, 3))
        with c1:
            st.image('./images/04_generator1.png')
            st.image('./images/04_generator2.png')

        import streamlit.components.v1 as components
        url = 'https://wordcloud.kr/'
        components.iframe(url, width=1024, height=1200)

    elif selected_tab == '코랩으로 워드 클라우드 만들기':
        log_record(3,4)
        st.subheader("<실습 2> 코랩으로 워드 클라우드 만들기")
        st.markdown("[구글 드라이브 링크 (팀 공유 폴더)](https://drive.google.com/drive/folders/1eSEK2nEWM030_td1KuDUQiC1kOpm4cmP)", unsafe_allow_html=True)
        c1, c2 = st.columns((7, 3))
        with c1:
            st.image('./images/05_python1.png')
            st.image('./images/05_discuss.png')
            st.image('./images/05_python2.png')
            st.image('./images/05_python3.png')

    elif selected_tab == '학습정리':
        log_record(3,5)
        c1, c2 = st.columns((7, 3))
        with c1:
            st.image('./images/06_final1.png')
            st.image('./images/06_final2.png')

        with c2:
            # 공부할거 같은 내용을 답변    
            with st.form('mynoteform'):
                txtString = st.text_area('수업을 마치며 소감..', height=200)
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
                    conn_question3.execute('SELECT id, txtfile, timestamp FROM question33 WHERE userid = ? ORDER BY timestamp DESC', (user_id,))
                    questions33 = conn_question3.fetchall()
                    if questions33:
                        df_questions = pd.DataFrame(questions33, columns=["ID", "Question", "Timestamp"])
                        st.dataframe(df_questions)
                    else:
                        st.warning("현재 저장된 질문이 없습니다.")

    elif selected_tab == '자료제출':
        log_record(3,6)

        # 테이블 생성 (user_id, file_name, file_data, timestamp)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS uploaded_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            file_name TEXT NOT NULL,
            file_data BLOB NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()
        
        uploaded_file = st.file_uploader("이미지를 업로드하세요.", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            st.success("파일이 업로드되었습니다.")
            
            # 파일 데이터를 바이너리 형식으로 변환
            file_data = uploaded_file.read()
            
            # 데이터베이스에 업로드 정보 저장
            cursor.execute("INSERT INTO uploaded_files (user_id, file_name, file_data, timestamp) VALUES (?, ?, ?, ?)", 
                        (user_id, uploaded_file.name, file_data, datetime.now()))
            conn.commit()
            st.write(f"{user_id}님이 업로드한 파일이 데이터베이스에 저장되었습니다.")

    elif selected_tab == '선생님탭':
        log_record(3,7)
        if st.session_state['login_status'] and st.session_state['current_user'] == 'admin':
            with st.expander('이 탭이 무엇인지 궁금하신가요?'):
                st.subheader('여기는..')
                txtdata = '''
                선생님 권한을 가진 admin 유저가 학생들의 답을 볼 수 있는 공간입니다.
                '''
                st.markdown(txtdata, unsafe_allow_html=True)

            # 질문1 불러오기
            st.write("About: 질문 탭")
            conn_question1.execute('SELECT id, userid, txtfile, timestamp FROM question31 ORDER BY timestamp DESC')
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
                    conn_question1.execute('DELETE FROM question31 WHERE id = ?', (question_id_to_delete,))
                    conn_2.commit()  # Commit the transaction
                    st.success(f'질문 ID {question_id_to_delete}이(가) 성공적으로 삭제되었습니다!')
                    # Refresh the DataFrame after deletion
                    conn_question1.execute('SELECT id, userid, txtfile, timestamp FROM question31 ORDER BY timestamp DESC')
                    questions = conn_question1.fetchall()
                    df_questions = pd.DataFrame(questions, columns=["ID", "User ID", "Question", "Timestamp"])
                    st.dataframe(df_questions)  # Display updated DataFrame

            # 질문2 불러오기
            st.write("About: 질문2 탭")
            conn_question2.execute('SELECT id, userid, txtfile, timestamp FROM question32 ORDER BY timestamp DESC')
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
                    conn_question2.execute('DELETE FROM question2 WHERE id = ?', (question_id_to_delete,))
                    conn_3.commit()  # Commit the transaction
                    st.success(f'질문 ID {question_id_to_delete}이(가) 성공적으로 삭제되었습니다!')
                    # Refresh the DataFrame after deletion
                    conn_question2.execute('SELECT id, userid, txtfile, timestamp FROM question32 ORDER BY timestamp DESC')
                    questions2 = conn_question2.fetchall()
                    df_questions = pd.DataFrame(questions2, columns=["ID", "User ID", "Question", "Timestamp"])
                    st.dataframe(df_questions)  # Display updated DataFrame
            else:
                st.warning("현재 저장된 질문이 없습니다.")

            # 데이터베이스에서 업로드된 파일을 가져오기
            cursor.execute("SELECT user_id, file_name, file_data, timestamp FROM uploaded_files")
            records = cursor.fetchall()

            # records를 DataFrame으로 변환
            df = pd.DataFrame(records, columns=["user_id", "file_name", "file_data", "timestamp"])

            # DataFrame을 Streamlit에 출력 (file_data 열은 표시하지 않도록 제외)
            st.dataframe(df.drop(columns=["file_data"]))

            # 데이터베이스 연결 종료
            conn.close()

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

        else:
            st.error('접근권한이 없습니다.')
else:
    st.error("로그인을 먼저하세요.")
