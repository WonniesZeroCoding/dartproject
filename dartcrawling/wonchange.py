# 원 단위 문자열로 바꾸기가 가능한지에 대한 실험


def get_wonhwa_change(num_wonhwa_amount):
    """
    돌려 받은 결과 값 영업이익을 한글로 반환 : 3자리 단위로
    -> 돈은 3자리 단위로 끊어 읽는 것이 편함 1,000 // 1,000,000
    """
    str_result = ""  # 결과 문자열 초기화
    str_sign = ""  # 부호 초기화
    num_change = num_wonhwa_amount  # 최초 값 num_change에 대입

    if num_change == 0:  # 결과가 0원이라면
        str_result = "0"

    elif num_change < 0:  # 결과가 음수라면
        str_sign = "-"  # 음수 부호 - 넣기
        num_change = abs()  # 절대값 함수 abs를 이용해 소수점 제거
