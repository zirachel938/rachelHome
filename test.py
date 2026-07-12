import os
import random
import sys
import time

# 尝试导入 colorama 库以支持 Windows 终端颜色，如果没有则忽略
try:
    import colorama

    colorama.init()
except ImportError:
    pass

# 屏幕宽度和高度
WIDTH = 80
HEIGHT = 25

# 字符集（日文半角、数字、英文字母）
CHARS = [
    "1",
    "0",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "X",
    "Y",
    "Z",
    "*",
    "#",
    "$",
    "@",
    " ",
]


def matrix_effect():
    # 初始化每一列的雨滴位置
    # -10 表示一开始在屏幕上方隐藏处
    columns = [random.randint(-20, 0) for _ in range(WIDTH)]

    # 清屏
    os.system("cls" if os.name == "nt" else "clear")

    try:
        while True:
            # 每一帧的屏幕缓冲区
            screen = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

            for col in range(WIDTH):
                pos = columns[col]

                # 如果当前列的雨滴已经落到屏幕内
                if pos >= 0:
                    # 绘制雨滴头部（白色，最亮）
                    if pos < HEIGHT:
                        screen[pos][col] = (
                            f"\033[1;37m{random.choice(CHARS)}\033[0m"
                        )

                    # 绘制雨滴身体（绿色）
                    for i in range(1, 8):  # 尾巴长度为 8
                        prev_pos = pos - i
                        if 0 <= prev_pos < HEIGHT:
                            # 越往后颜色越暗
                            color_code = (
                                "32" if i < 4 else "2"
                            )  # 32是亮绿，2是暗绿
                            screen[prev_pos][col] = (
                                f"\033[0;{color_code}m{random.choice(CHARS)}\033[0m"
                            )

                # 更新雨滴位置（向下移动）
                columns[col] += 1

                # 如果雨滴完全落出屏幕，或者有概率随机重置
                if columns[col] >= HEIGHT or (
                    columns[col] > 0 and random.random() < 0.05
                ):
                    columns[col] = random.randint(-10, 0)

            # 拼接并打印整张屏幕
            output = "\n".join("".join(row) for row in screen)
            # 使用 \033[H 将光标移动到左上角，避免闪烁
            sys.stdout.write("\033[H" + output)
            sys.stdout.flush()

            # 控制帧率
            time.sleep(0.05)

    except KeyboardInterrupt:
        # 按 Ctrl+C 退出时清理屏幕并显示退出信息
        os.system("cls" if os.name == "nt" else "clear")
        print("Matrix simulation stopped. Goodbye Neo.")


if __name__ == "__main__":
    matrix_effect()
