import numpy as np
from rapidocr_onnxruntime import RapidOCR

class OCRProcessor:
    def __init__(self):
        self.engine = RapidOCR()

    def recognize(self, img_path):
        result, elapse = self.engine(img_path)
        converted_data = []
        for item in result:
            new_item = []
            for part in item:
                if isinstance(part, np.float32):
                    new_item.append(float(part))
                else:
                    new_item.append(part)
            converted_data.append(new_item)
        
        text_datalist = []
        for i in range(len(converted_data)):
            text_datalist.append({
                "coordinates": converted_data[i][0],
                "text": converted_data[i][1], 
                "confidence": converted_data[i][2]
            })
        text_list = self.calculate_sameLines(text_datalist)
        result = [' '.join(line) for line in text_list]
        return {"result": result, "elapse": elapse, "status": "success"}

    @staticmethod
    def calculate_sameLines(data):
        tolerance = 15  # 允许的y坐标差值
        data.sort(key=lambda x: x['coordinates'][0][1])  # 按照y坐标排序

        result = []
        current_line = []
        for item in data:
            left_mid = (item['coordinates'][3][1] - item['coordinates'][0][1]) / 2 + item['coordinates'][0][1]
            right_mid = (item['coordinates'][2][1] - item['coordinates'][1][1]) / 2 + item['coordinates'][1][1]
            if abs(left_mid - right_mid) < 1:
                pass
            if not current_line or abs(item['coordinates'][0][1] - current_line[0]['coordinates'][0][1]) < tolerance:
                if current_line and item['coordinates'][0][0] > current_line[-1]['coordinates'][-1][0]:
                    current_line[-1]['text'] += ' ' + item['text']
                else:
                    current_line.append(item)
            else:
                result.append([t['text'] for t in current_line])
                current_line = [item]

        result.append([t['text'] for t in current_line])
        return result
