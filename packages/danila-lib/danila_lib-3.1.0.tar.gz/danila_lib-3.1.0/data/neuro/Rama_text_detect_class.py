import json
import os

import cv2
import torch
import zipfile
import requests
from urllib.parse import urlencode

from data.neuro.letters_in_image import Letters_In_Image
from data.result.Image_text_areas import Image_text_areas
from data.result.Text_area import Text_area

"""module for detecting text in rama"""
class Rama_text_detect_class:
    """class for detecting text in rama"""
    # reads yolov5 taught model from yandex-disk and includes it in class example
    def __init__(self, local, model_path, yolo_path):
        """reads yolov5 taught model from yandex-disk and includes it in class example"""
        if local:
            self.model = torch.hub.load(yolo_path, 'custom', model_path, source='local')
        else:
            base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
            public_key = model_path  # Сюда вписываете вашу ссылку
            # Получаем загрузочную ссылку
            final_url = base_url + urlencode(dict(public_key=public_key))
            response = requests.get(final_url)
            download_url = response.json()['href']
            # Загружаем файл и сохраняем его
            download_response = requests.get(download_url)
            zip_path = 'rama_text_detect.zip'
            # print(download_response.content)
            with open(zip_path, 'wb') as f:
                f.write(download_response.content)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall()
            weights_file_path = 'rama_text_detect.pt'
            self.model = torch.hub.load(yolo_path, 'custom', weights_file_path, source='local')
    # find text areas on img from img_path with yolov5, returns yolojson
    def work_img(self, img_path):
        """find text areas on img from img_path with yolov5, returns yolojson"""
        results = self.model([img_path], size=256)
        json_res = results.pandas().xyxy[0].to_json(orient="records")
        res2 = json.loads(json_res)
        return res2
    # find text areas on img from img_path with yolov5, returns dict with rects for each text class
    def text_detect(self, img_path):
        """find text areas on img from img_path with yolov5, returns dict with rects for each text class"""
        json_res = self.work_img(img_path)
        image_text_areas = Image_text_areas()
        image_text_areas_list = Letters_In_Image.get_letters_in_image_from_yolo_json(json_res)
        image_text_areas_list.sort_letters()
        image_text_areas_list.delete_intersections()
        json_res_1 = []
        for image_text_areas_list_el in image_text_areas_list.letters:
            dict = {}
            dict['confidence'] = image_text_areas_list_el.confidence
            dict['xmin'] = image_text_areas_list_el.rect.xmin
            dict['xmax'] = image_text_areas_list_el.rect.xmax
            dict['ymin'] = image_text_areas_list_el.rect.ymin
            dict['ymax'] = image_text_areas_list_el.rect.ymax
            if image_text_areas_list_el.letter == 'number':
                dict['class'] = 0
            elif image_text_areas_list_el.letter == 'prod':
                dict['class'] = 1
            elif image_text_areas_list_el.letter == 'text':
                dict['class'] = 2
            elif image_text_areas_list_el.letter == 'year':
                dict['class'] = 3
            json_res_1.append(dict)
        for text_area_json in json_res_1:
            if text_area_json['confidence']>0.25:
                text_area = Text_area(text_area_json)
                image_text_areas.add_area(text_area)
        image_text_areas.correct_intersections()
        return image_text_areas
    # draw img_text_areas on img, returns opencv img
    def draw_text_areas_in_opencv(self, image_text_areas, img):
        """draw img_text_areas on img, returns opencv img"""
        colors = [(0,0,255), (0,255,0), (255,255,255), (255,0,0)]
        for class_im in image_text_areas.areas:
            for rect in image_text_areas.areas[class_im]:
                cv2.rectangle(img, (rect.xmin, rect.ymin), (rect.xmax, rect.ymax), color=colors[class_im.value], thickness=2)
                cv2.putText(img, class_im.name, (rect.xmin, rect.ymin), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color=colors[class_im.value], thickness=1)
        return img

