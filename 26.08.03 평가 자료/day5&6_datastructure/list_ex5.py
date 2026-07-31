students = [
    {
        '이름' : '김싸피',
        '국어' : 80,
        '영어' : 95,
        '수학' : 85
    },
    {
        '이름' : '이싸피',
        '국어' : 95,
        '영어' : 95,
        '수학' : 70
    },
    {
        '이름' : '박싸피',
        '국어' : 100,
        '영어' : 80,
        '수학' : 60
    },
    {
        '이름' : '최싸피',
        '국어' : 75,
        '영어' : 100,
        '수학' : 55
    },
]
#############################################################
# 모든 학생들의 평균 점수를 '이름 : 점수' 형태로 출력하세요(단, 소수점 두 자리까지만 출력)
subjects = ['국어','영어','수학']

for student in students:
    total = 0
    for subject in subjects:
        total = total + student[subject]
    avg_score = total/len(subjects)
    print(f'{student["이름"]} : {avg_score:.2f}점')

#############################################################
# 각 과목별 총점을 '과목명 : 점수' 형태로 출력하세요
subject_total = {}
for student in students:    # 학생 반복
    for subject in subjects:  # 과목 반복
        subject_total.setdefault(subject,0) # 초기값 세팅, 만약있다면 기존 값있다면 무시

        #새로운 과목 총점 = 과목총점 기존 + 학생 과목점수 
        subject_total[subject] = student[subject] + subject_total[subject]
print(subject_total)


#############################################################
# 각 과목별 최고점을 받은 학생의 이름을 '과목 : 이름' 형태로 출력하세요

max_students ={}    # 과목 : 학생이름 이 저장될 dictionary 
max_score = {
    '국어' : 0,
    '수학' : 0,
    '영어' : 0
}
for student in students:
    for subject in subjects:
        # 현재 학생의 과목점수와 기존 최고점 비교
        if max_score[subject] < student[subject]:   # 최고점과 학생의 과목 점수를 비교
            max_students[subject] = student['이름'] # 최고점이라면 학생의 이름을 저장
            max_score[subject] = student[subject]   # 최고점 비교를 위해 점수도 저장
print(max_students)

#####################################################
# 각 과목별 평균 점수를 '과목명 : 점수' 형태로 출력하세요
# 각 과목별 평균 점수를 구하기 위해서는 과목별 점수 합이 필요
# 딕셔너리가 적절해보임
total_scores = {
    '수학' : 0,
    '영어' : 0,
    '국어' : 0
}

for student in students:
    # 각 과목별 점수 따로 더해주기
    for subject in subjects:
        total_scores[subject] += student[subject]
        
# 모든 학생들의 점수를 다 더했다면, 과목별 총점이 구해졌을 것
for subject in subjects:
    print(f'{subject} : {total_scores[subject]/len(students)}')


