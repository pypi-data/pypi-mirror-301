import random
import time
from datetime import datetime
import requests
import sys
import os
from IPython.display import clear_output

import pytz

import warnings
warnings.filterwarnings('ignore') 

class Competition:
    def __init__(self, username, course_name, course_round, competition_name):
        self.username = username
        self.course_name = course_name  # 과정명 추가
        self.course_round = course_round # 차수 추가
        self.competition_name = competition_name # 대회명
        self.questions = self.__fetch_questions()  # 질문 데이터를 저장할 변수

    def __fetch_questions(self, include_ground_truth=False):
        """정답값을 포함할지 여부를 결정하는 매개변수 추가"""
        url = "http://49.247.167.182/questions"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                questions = response.json()  # JSON 응답을 Python dict로 변환
                # 만약 정답값을 제외하고 싶다면, 'ground_truth' 키를 삭제
                if not include_ground_truth:
                    for question_id, question_data in questions.items():
                        if 'ground_truth' in question_data:
                            del question_data['ground_truth']
                return questions
            else:
                print(f"Error: Failed to fetch questions. Status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
            
    def __evaluate_answers(self):
        from datasets import Dataset
        from ragas import evaluate 
        from ragas.metrics import answer_correctness 

        """사용자 답변을 평가하는 비공개 함수"""
        # 서버에서 ground_truth 포함된 질문을 가져옴
        questions_with_ground_truth = self.__fetch_questions(include_ground_truth=True)

        if questions_with_ground_truth is None:
            print("채점서버와 연결과정에서 문제가 발생하였습니다.")
            return None

        # ground_truth와 question 리스트를 준비
        ground_truths = [q['ground_truth'] for q in questions_with_ground_truth.values()]
        questions_list = [q['question'] for q in questions_with_ground_truth.values()]
        answers_list = [str(q['answer']) for q in self.questions.values()]  # 사용자가 입력한 답변

        data_samples = {
            'question': questions_list,
            'answer': answers_list,
            'ground_truth': ground_truths
        }
        dataset = Dataset.from_dict(data_samples)

        # RAGAS 라이브러리를 사용한 평가
        score = evaluate(dataset, metrics=[answer_correctness], show_progress=False)
        return score['answer_correctness']  # 여러 개일 경우 평균 반환

    def submit(self):
        """사용자 이름, 과정명, 점수, 함수 호출 시간을 서버로 전송"""
        url = "http://49.247.167.182/submission"
        kst = pytz.timezone('Asia/Seoul')
        timestamp = datetime.now(kst).strftime("%Y-%m-%d %H:%M:%S.%f")  # 현재 시간 ISO 형식으로 변환
        
        if not self.username or not self.course_name:
            print("이름 또는 과정명이 설정되지 않았습니다.")
            return 

        score = self.__evaluate_answers()
        if score is None:
            print("점수를 계산할 수 없습니다.")
            return
        
        payload = {
            "username": self.username,
            "course_name": self.course_name,  # 과정명 추가
            "course_round": self.course_round, # 차수 추가
            "score": score,
            "submission_time": timestamp,
            "competition_name": self.competition_name,
        }
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                self.__show_progress()
                sys.stdout.write(f"\r평가 결과 {self.course_name} 과정의 {self.username}님의 점수는 {score} 입니다.")
            else:
                print(f"Error: Failed to submit data. Status code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred while submitting: {e}")


    def __clear_screen(self):
        """현재 환경에 맞춰 출력창을 지우는 함수"""
        # Jupyter Notebook인 경우
        try:
            clear_output(wait=True)
        except NameError:
            # 콘솔/터미널 환경인 경우
            os.system('cls' if os.name == 'nt' else 'clear')

    def __show_progress(self):
        """총 10초 동안 랜덤하게 진행률을 표시하는 함수 (리프레시 방식)"""
        sys.stdout.write(f"\r제출이 성공적으로 처리되었습니다.")
        time.sleep(1)
        sys.stdout.flush()

        total_blocks = 10  # 총 블록 수
        progress = 0  # 진행률 (0에서 100%)
        blocks_filled = 0  # 채워진 블록 수

        while progress < 100:
            time.sleep(1)  # 1초 대기
            increment = random.randint(5, 20)  # 랜덤하게 진행률 증가
            progress = min(progress + increment, 100)  # 진행률은 100%를 넘지 않도록

            # 채워질 블록의 개수를 계산
            new_blocks_filled = int((progress / 100) * total_blocks)

            # 진행률 표시 (채워진 블록은 ■, 나머지는 공백)
            if new_blocks_filled > blocks_filled:
                blocks_filled = new_blocks_filled
                progress_bar = '■' * blocks_filled + ' ' * (total_blocks - blocks_filled)
                sys.stdout.write(f"\r 평가중 : [{progress_bar}] {progress:.0f}%")  # \r로 출력 리프레시
                sys.stdout.flush()
