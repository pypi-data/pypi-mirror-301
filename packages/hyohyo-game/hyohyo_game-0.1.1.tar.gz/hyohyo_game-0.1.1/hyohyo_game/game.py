import random


## 가위바위보 게임
def rock_paper_scissors():
    choices = ["가위", "바위", "보"]
    computer_choice = random.choice(choices)

    print("가위, 바위, 보 중 하나를 고르세요!")
    player_choice = input("당신의 선택: ")

    print(f"컴퓨터의 선택: {computer_choice}")

    if player_choice == computer_choice:
        print("비겼습니다!")
    elif (player_choice == "가위" and computer_choice == "보") or \
         (player_choice == "바위" and computer_choice == "가위") or \
         (player_choice == "보" and computer_choice == "바위"):
        print("당신이 이겼습니다!")
    else:
        print("당신이 졌습니다!")
    

## 숫자 업앤다운 게임
def guess_the_number():
    number_to_guess = random.randint(1, 100)
    attempts = 0

    print("1부터 100 사이의 숫자를 맞춰보세요!")

    while True:
        player_guess = int(input("숫자를 입력하세요: "))
        attempts += 1

        if player_guess < number_to_guess:
            print("더 큰 숫자입니다.")
        elif player_guess > number_to_guess:
            print("더 작은 숫자입니다.")
        else:
            print(f"정답입니다! {attempts}번 만에 맞추셨습니다.")
            break


## 숫자야구 3자리 게임
def generate_number():
    digits = random.sample(range(0, 10), 3)
    return ''.join(map(str, digits))

def check_guess(secret, guess):
    strikes = sum(1 for i in range(3) if secret[i] == guess[i])
    balls = sum(1 for i in range(3) if secret[i] != guess[i] and guess[i] in secret)
    return strikes, balls

def number_baseball():
    secret_number = generate_number()
    attempts = 0

    print("숫자 야구 게임을 시작합니다! 3자리 숫자를 맞춰보세요.")

    while True:
        guess = input("숫자를 입력하세요: ")
        if len(guess) != 3 or not guess.isdigit():
            print("3자리 숫자를 입력해주세요.")
            continue

        attempts += 1
        strikes, balls = check_guess(secret_number, guess)

        print(f"{strikes} 스트라이크, {balls} 볼")

        if strikes == 3:
            print(f"정답입니다! {attempts}번 만에 맞추셨습니다.")
            break


