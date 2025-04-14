import mysql.connector
from mysql.connector import Error

# 1. 연결 함수 (conn, cursor 반환)
def create_conn():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='python_test'
        )
        if conn.is_connected():
            print('MySQL 연결 성공')
            cursor = conn.cursor()
            return conn, cursor
    except Error as e:
        print('연결 실패:', e)
        return None, None

# 2. 사용자 입력 후 INSERT 수행
def create_user():
    conn, cursor = create_conn()
    
    if not conn or not cursor:
        return

    try:
        # 사용자로부터 정보 입력 받기
        username = input("사용자 ID를 입력하세요: ")
        password = input("비밀번호를 입력하세요: ")
        name = input("이름을 입력하세요: ")
        email = input("이메일을 입력하세요: ")

        # INSERT 쿼리 작성 및 실행
        sql = """
        INSERT INTO users (username, password, name, email)
        VALUES (%s, %s, %s, %s)
        """
        user_data = (username, password, name, email)
        cursor.execute(sql, user_data)
        conn.commit()
        print(f"사용자 '{username}' 추가 완료!")
    except Error as e:
        print("사용자 추가 실패:", e)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("연결 종료됨")

# create_user()

# SELECT문 유저 조회회
def get_user():
    conn, cursor = create_conn()
    
    if not conn or not cursor:
        return

    try:
        cursor.execute("SELECT * FROM users;")
        result = cursor.fetchall() # fetchone 특정 하나만 가져올때때
        for row in result:
            print(row)

    except Error as e:
        print("조회 실패:", e)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# get_user()

# UPDATE문 사용자 변경경
def update_user():
    conn, cursor = create_conn()
    
    if not conn or not cursor:
        return

    try:
        # 사용자 입력
        username = input("수정할 사용자 ID를 입력하세요: ")
        new_name = input("새 이름을 입력하세요: ")
        new_email = input("새 이메일을 입력하세요: ")

        # UPDATE 쿼리 실행
        sql = "UPDATE users SET name = %s, email = %s WHERE username = %s"
        user_data = (new_name, new_email, username)
        cursor.execute(sql, user_data)
        conn.commit()

        if cursor.rowcount > 0:
            print(f"사용자 ID {username} 정보가 수정되었습니다.")
        else:
            print(f"사용자 ID {username}를 찾을 수 없습니다.")
    except Error as e:
        print("사용자 정보 수정 실패:", e)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("연결 종료됨")
# update_user()

# DELETE문
def delete_user():
    conn, cursor = create_conn()
    
    if not conn or not cursor:
        return

    try:
        # 사용자 입력
        username = input("삭제할 사용자 ID를 입력하세요: ")

        # DELETE 쿼리 실행
        sql = "DELETE FROM users WHERE username = %s"
        cursor.execute(sql, (username,))
        conn.commit()

        if cursor.rowcount > 0:
            print(f"사용자 ID '{username}' 삭제 완료.")
        else:
            print(f"사용자 ID '{username}'를 찾을 수 없습니다.")
    except Error as e:
        print("사용자 삭제 실패:", e)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("연결 종료됨")
# delete_user()

# 6. 메뉴 루프
def run_menu():
    while True:
        print("\n====== 사용자 관리 시스템 ======")
        print("1. 사용자 추가")
        print("2. 사용자 전체 조회")
        print("3. 사용자 정보 수정")
        print("4. 사용자 삭제")
        print("0. 종료")
        choice = input("메뉴를 선택하세요: ")

        if choice == "1":
            create_user()
        elif choice == "2":
            get_user()
        elif choice == "3":
            update_user()
        elif choice == "4":
            delete_user()
        elif choice == "0":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 다시 선택해주세요.")

# 프로그램 실행
run_menu()