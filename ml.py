import cv2 as cv
from video_conv import super_video_format
from ultralytics import YOLO


class CntItem:
    def __init__(self):
        self.cnt = 0
        self.sum = 0
        self.max = 0.0


class YoloModel:
    def __init__(self):
        self.model = YOLO('best_last.pt')

    def multi_process(self, files):
        answers = []
        print(files)
        for file in files:
            names = {0: '-', 1: 'Beton', 2: 'Derevo', 3: 'Grunt', 4: 'Kirpich'}
            counter = {0: CntItem(), 1: CntItem(), 2: CntItem(), 3: CntItem(), 4: CntItem()}
            trimmed_clip = super_video_format(file[1], file[0], 120, 140)
            for frame in trimmed_clip.iter_frames(10):
                results = self.model(frame)
                for r in results:
                    for c in r.boxes:
                        conf = c.conf.cpu().numpy()[0]  # вероятность
                        ind = int(c.cls)  # класс
                        counter[ind].max = float(max(counter[ind].max, conf))
                        counter[ind].cnt += 1  # счетчик
                        counter[ind].sum += conf  # сумма вер.

                if cv.waitKey(1) & 0xFF == ord('q'):
                    break

            max_key = 0
            for i in range(len(list(counter))):
                if counter[i].max > counter[max_key].max:
                    max_key = i

            if max_key == 0 or counter[max_key].cnt == 0:
                ans = {
                    "filename": file[1].filename,
                    "class_name": "не определен",
                    "avg": 0
                }
            else:
                ans = {
                    "filename": file[1].filename,
                    "class_name": names[max_key],
                    "avg": counter[max_key].max
                }
            print(ans)
            answers.append(ans)
        return answers
