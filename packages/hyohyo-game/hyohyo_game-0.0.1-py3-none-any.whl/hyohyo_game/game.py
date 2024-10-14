import random

def play(choice):
    options = ['가위', '바위', '보']
    computer_choice = random.choice(options)
    
    if choice not in options:
        return "잘못된 선택입니다. 가위, 바위, 보 중 하나를 선택하세요."

    if choice == computer_choice:
        return f"무승부! 둘 다 {choice}를 선택했습니다."
    elif (choice == '가위' and computer_choice == '보') or \
         (choice == '바위' and computer_choice == '가위') or \
         (choice == '보' and computer_choice == '바위'):
        return f"이겼습니다! 컴퓨터는 {computer_choice}를 선택했습니다."
    else:
        return f"졌습니다. 컴퓨터는 {computer_choice}를 선택했습니다."