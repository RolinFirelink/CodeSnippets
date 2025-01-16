from time import sleep

import pyautogui
import cv2
import numpy as np
import time
import os

# 定义客户框和玩家菜品框的屏幕坐标
player_dish_box = (1099, 790, 136, 48)
customer_boxes = [
    (927, 583, 142, 47),
    (1110, 579, 150, 51),
    (1301, 581, 147, 50),
    (1487, 579, 150, 54)
]

# 模板图片路径
template_dir = r"绝对路径"

def get_screenshot_array(region):
    """获取指定区域截图为NumPy数组"""
    screenshot = pyautogui.screenshot(region=region)
    screenshot_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return screenshot_np

def match_template(image, template):
    """匹配截图与模板，返回匹配度"""
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)
    return max_val

def load_templates(directory):
    """加载模板图片"""
    templates = {}
    for filename in os.listdir(directory):
        if filename.endswith(".jpg"):
            template_path = os.path.join(directory, filename)
            templates[filename] = cv2.imread(template_path, cv2.IMREAD_COLOR)
    return templates

templates = load_templates(template_dir)

def get_target_index(image, templates):
    """匹配图像与模板并计算目标下标"""
    for filename, template in templates.items():
        match_score = match_template(image, template)
        if match_score >= 0.8:
            print(f"匹配到模板: {filename}, 匹配度: {match_score}")
            target_index = int(os.path.splitext(filename)[0]) % 5
            return target_index
    print("未匹配到任何模板")
    return None

def find_and_match_dish(player_dish_index, customer_boxes, templates):
    """匹配客户框"""
    for index, box in enumerate(customer_boxes):
        customer_image = get_screenshot_array(box)
        customer_index = get_target_index(customer_image, templates)
        if customer_index is not None and customer_index == player_dish_index:
            print(f"匹配到客户框 {index + 1}，执行点击操作。")
            pyautogui.click(box[0] + box[2] // 2, box[1] + box[3] // 2)
            # sleep(0.25)
            return True
    return False

def main_loop():
    """主循环"""
    while True:
        player_image = get_screenshot_array(player_dish_box)
        player_dish_index = get_target_index(player_image, templates)

        if player_dish_index is None:
            print("玩家菜品未匹配，切换菜品。")
            pyautogui.rightClick()
            # time.sleep(0.1)
            continue

        print(f"当前玩家菜品目标下标：{player_dish_index}")
        matched = find_and_match_dish(player_dish_index, customer_boxes, templates)

        if not matched:
            print("没有匹配的客户，切换菜品。")
            pyautogui.rightClick()

        # time.sleep(0.1)

if __name__ == "__main__":
    try:
        time.sleep(1.5)
        main_loop()
    except Exception as e:
        print(f"程序终止，原因: {e}")
