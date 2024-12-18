#수정하지말고 써

#finalRock.py의 이미지 경로를 모든 컴퓨터를 대상으로 수정


#wishRock_19.py

import os

import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import PhotoImage, Text, ttk
from elevenlabs import play
from elevenlabs.client import ElevenLabs
from pathlib import Path
from PIL import Image, ImageTk
from pydantic import BaseModel

client = ElevenLabs(
    api_key="sk_c4e012b0f5bca4111c1ee2fb1db327a581e2a3475150f5ee",
)

# 전역 변수 초기화
entry_1 = None
entry_8 = None
generate_button = None
voice_generated = False  # 목소리 생성 여부를 나타내는 변수
inactivity_timer = None  # 비활동 타이머
next_button = None
voice_generating = False  # 음성 생성 중 여부
status_label = None  # 상태 라벨
timer_id = None  # 타이머 ID

# 비활동 타이머 함수
def start_inactivity_timer():
    global inactivity_timer
    if inactivity_timer is not None:
        window.after_cancel(inactivity_timer)
    inactivity_timer = window.after(30000, reset_to_scene_1)

# 비활동 상태를 감지하고 타이머 리셋
def reset_to_scene_1():
    global scene_num, voice_generated
    if voice_generated:
        scene_num = 1
        load_scene(f"scene_{scene_num}.png")
        voice_generated = False
        hide_all_inputs()

# Tkinter 윈도우 설정
window = tk.Tk()
window.title("WishRock")
window.geometry("1280x720")
window.minsize(640, 360)
window.configure(bg="#FFFFFF")

# 전체화면 모드 활성화
window.attributes("-fullscreen", True)

# ESC 키로 전체화면 모드 해제
window.bind("<Escape>", lambda event: window.attributes("-fullscreen", False))

# 기본 변수들 설정
scene_num = 1
scenes = [f"scene_{i}.png" for i in range(1, 18)]

# 캔버스 설정
canvas = tk.Canvas(window, bg="#FFFFFF", height=720, width=1280, bd=0, highlightthickness=0, relief="ridge")
canvas.pack(fill="both", expand=True)

''' 경로 설정 - 내 컴퓨터만을 위함함
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:/Users/yesju/OneDrive/바탕 화면/wishRock")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
'''

# 경로 설정 - 모든 컴퓨터를 위함
OUTPUT_PATH = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(OUTPUT_PATH, "wishRock")

def relative_to_assets(path: str) -> Path:
    return Path(ASSETS_PATH) / Path(path)

# 숨기기 기능
def hide_all_inputs():
    """모든 입력 요소와 버튼 숨기기."""
    if entry_1:
        entry_1.place_forget()
    if generate_button:
        generate_button.place_forget()
    if entry_8:
        entry_8.place_forget()
    if next_button:
        next_button.place_forget()

# 상태 라벨을 업데이트하는 함수
def update_status_label(message):
    status_label.config(text=message)

# 10초 후 상태 메시지 표시 함수
def show_input_prompt():
    update_status_label("듣고 싶은 문장을 입력하세요.")

# 목소리 생성 함수
def generate_voice():
    global voice_generated, voice_generating
    text = entry_1.get("1.0", "end-1c")
    
    if not text.strip():
        update_status_label("듣고 싶은 문장을 입력하세요.")  # 텍스트가 없을 때 메시지 표시
        return

    if voice_generating:  # 이미 음성을 생성 중일 때
        return  # 아무 동작도 하지 않음

    voice_generating = True  # 음성 생성 시작
    generate_button.config(state=tk.DISABLED)  # 버튼 비활성화
    update_status_label("음성이 생성 중입니다...")  # 상태 업데이트

    try:
        audio = client.generate(
            text=text,
            voice="Kp8K3ZlvqyVzkQBQ2IXJ",
            model="eleven_multilingual_v2"
        )
        play(audio)
        voice_generated = True
    except Exception as e:
        print(f"음성 생성 중 오류 발생: {e}")
    
    voice_generating = False  # 음성 생성 종료
    generate_button.config(state=tk.NORMAL)  # 버튼 활성화
    update_status_label("또 듣고 싶다면 버튼을 다시 눌러보세요.")  # 상태 업데이트

# 텍스트 입력 시 상태 라벨 숨기기
def on_text_change(event):
    global timer_id
    if entry_1.get("1.0", "end-1c").strip():  # 텍스트가 입력된 경우
        update_status_label("")  # 상태 라벨 숨김
        if timer_id:  # 타이머가 설정되어 있으면 취소
            canvas.after_cancel(timer_id)
            timer_id = None
    else:
        # 아무 입력도 없을 때는 타이머를 시작
        if not timer_id:
            timer_id = canvas.after(10000, show_input_prompt)  # 10초 후 메시지 표시

# 씬 17 기능
def create_input_text_button():
    global canvas, entry_1, generate_button, status_label

    # 프레임 생성 (스크롤바를 포함하기 위함)
    text_frame = tk.Frame(canvas)
    text_frame.place(relx=0.5, rely=0.4, anchor='center', width=875.0, height=124.0)

    # Text 위젯 생성
    entry_1 = Text(
        text_frame,
        bd=2,
        bg="#D0A6A7",
        fg="#3D2A2D",
        highlightthickness=0,
        wrap='word',  # 줄바꿈을 단어 단위로
        font=("Arial Rounded MT Bold", 14),
        relief="ridge",
        padx=10,
        pady=10,
        height=6,  # 텍스트 박스 높이 조정
        width=65  # 너비 조정 (적절한 값으로 설정)
    )
    entry_1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # 스크롤바 추가
    scrollbar = tk.Scrollbar(text_frame, command=entry_1.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    entry_1.config(yscrollcommand=scrollbar.set)

    # 텍스트 변경 이벤트 바인딩
    entry_1.bind("<KeyRelease>", on_text_change)

    entry_1.tag_configure("center", justify='center')

    # 텍스트를 중앙 정렬하는 함수
    def center_text(event):
        # 현재 텍스트를 가져와서 중앙 정렬을 적용
        entry_1.tag_add("center", "1.0", "end")

    # 키가 눌릴 때마다 중앙 정렬 적용
    entry_1.bind("<KeyRelease>", center_text)

    # 음성 생성 버튼 스타일 설정
    style = ttk.Style()
    style.configure("TButton", background="#C2A6A8", foreground="#3D2A2D", borderwidth=3, relief="ridge")

    # 음성 생성 버튼 수정
    generate_button = ttk.Button(
        canvas,
        text="다 적은 후, 저를 눌러 들어보세요.",
        style="TButton",
        command=generate_voice
    )
    generate_button.place(
        relx=0.5,
        rely=0.55,
        anchor='center',
        width=875.0,
        height=44.0
    )

    # 상태 표시 라벨 추가
    status_label = tk.Label(canvas, text="", bg="#D0A6A7", fg="#3D2A2D", font=("Arial Rounded MT Bold", 12))
    status_label.place(relx=0.5, rely=0.65, anchor='center')

    # 초기 상태 메시지 (타이머 시작)
    update_status_label("")  # 초기 상태는 비워둡니다.
    global timer_id
    timer_id = canvas.after(10000, show_input_prompt)  # 10초 후 메시지 표시

# 씬 8 기능
def create_dream_input_text_button():
    global canvas, entry_8, next_button
    entry_8 = Text(
        bd=2,
        bg="#D0A6A7",
        fg="#3D2A2D",
        highlightthickness=0,
        wrap='word',
        font=("Arial Rounded MT Bold", 14),
        relief="ridge",
        padx=10,
        pady=50
    )
    entry_8.place(
        relx=0.5,
        rely=0.4,
        anchor='center',
        width=875.0,
        height=124.0
    )
    
    # 중앙 정렬을 위한 태그 설정
    entry_8.tag_configure("center", justify='center')
    entry_8.bind("<KeyRelease>", lambda event: entry_8.tag_add("center", "1.0", "end"))
    
    # Button 스타일 설정
    style = ttk.Style()
    style.configure("TButton", background="#C2A6A8", foreground="#3D2A2D", borderwidth=3, relief="ridge")
    
    # Button 생성 (꿈 입력 후 다음 씬으로 넘어가기)
    next_button = ttk.Button(
        canvas,
        text="꿈을 적은 후 이 버튼을 눌러 주세요.",
        style="TButton",
        command=next_scene_from_dream
    )
    next_button.place(
        relx=0.5,
        rely=0.55,
        anchor='center',
        width=875.0,
        height=44.0
    )

def load_scene(scene_name):
    image_path = f"C:/Users/yesju/OneDrive/바탕 화면/wishRock/{scene_name}"
    try:
        img = Image.open(image_path)

        # 창 크기에 맞춰 리사이즈
        window_width = window.winfo_width()
        window_height = window.winfo_height()
        resized_image = img.resize((window_width, window_height))
        tk_image = ImageTk.PhotoImage(resized_image)
        canvas.create_image(0, 0, anchor="nw", image=tk_image)
        canvas.image = tk_image  # 이미지 참조 유지
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")

# 창 크기 변경 시 리사이즈
def resize_image(event):
    load_scene(f"scene_{scene_num}.png")

# 다음 씬으로 넘어가는 함수 (scene_8에서 사용)
def next_scene_from_dream():
    global scene_num, entry_8
    text = entry_8.get("1.0", "end-1c").strip()

    if text:
        scene_num = 9
        load_scene(f"scene_{scene_num}.png")
        hide_all_inputs()  # 모든 입력 요소와 버튼 숨김
    else:
        print("꿈을 입력해주세요.")

# 장면 전환 함수
def next_scene(event=None):
    global scene_num
    if 0 <= scene_num < 8 or 9 <= scene_num < 17:
        scene_num += 1
        load_scene(f"scene_{scene_num}.png")

        if scene_num == 17:
            create_input_text_button()
        elif scene_num == 8:
            create_dream_input_text_button()
        elif scene_num == 9:
            hide_all_inputs()  # scene_9로 넘어갈 때 입력 박스와 버튼 숨김

        start_inactivity_timer()

# Enter 키로 씬 전환 및 음성 생성
def handle_keypress(event):
    if event.keysym == 'Return':  # Enter 키
        if scene_num == 8:
            next_scene_from_dream()
        elif scene_num == 17:  # 음성 생성 씬
            generate_voice()

# 첫 장면 로드
load_scene(scenes[0])

# 창 크기 변경 시 리사이즈
window.bind("<Configure>", resize_image)

# 클릭 시 다음 장면으로 이동
window.bind("<Button-1>", next_scene)

# 비활동 감지 이벤트 바인딩
window.bind("<Key>", lambda event: start_inactivity_timer())
window.bind("<Motion>", lambda event: start_inactivity_timer())

# Enter 키 이벤트 바인딩
window.bind("<Return>", handle_keypress)

# 메인 루프 실행
window.mainloop()
