def xyxy_to_yolo_str(x1, y1, x2, y2, img_width, img_height, obj_class):
    # Tọa độ trung tâm
    x_center = (x1 + x2) / 2 / img_width
    y_center = (y1 + y2) / 2 / img_height
    # Chiều rộng và chiều cao
    width = (x2 - x1) / img_width
    height = (y2 - y1) / img_height

    # Tạo chuỗi YOLO: "class x_center y_center width height"
    yolo_str = f"{obj_class} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"

    return yolo_str


def yolo_str_to_xyxy(yolo_str, img_width, img_height):
    # Tách chuỗi YOLO thành các giá trị
    yolo_data = yolo_str.split()
    obj_class = yolo_data[0]  # Lớp đối tượng (class)
    x_center = float(yolo_data[1])
    y_center = float(yolo_data[2])
    width = float(yolo_data[3])
    height = float(yolo_data[4])

    # Chuyển từ YOLO sang tọa độ góc
    x_min = (x_center - width / 2) * img_width
    x_max = (x_center + width / 2) * img_width
    y_min = (y_center - height / 2) * img_height
    y_max = (y_center + height / 2) * img_height

    return obj_class, x_min, y_min, x_max, y_max


if __name__ == "__main__":
    # Convert bbox to Yolo và ngược lại:
    x_min = 50
    y_min = 100
    x_max = 200
    y_max = 300
    img_width = 640
    img_height = 480
    obj_class = 0

    yolo_str = xyxy_to_yolo_str(
        x_min, y_min, x_max, y_max, img_width, img_height, obj_class
    )
    print(yolo_str)  # "0 0.195312 0.416667 0.234375 0.416667"

    yolo_str = "0 0.195312 0.416667 0.234375 0.416667"
    img_width = 640
    img_height = 480

    obj_class, x_min, y_min, x_max, y_max = yolo_str_to_xyxy(
        yolo_str, img_width, img_height
    )
    print(obj_class, x_min, y_min, x_max, y_max)  # 0 50.0 100.0 200.0 300.0
