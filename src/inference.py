import os, cv2, requests, time, shutil
from datetime import datetime
from threading import Thread
from db_service import DbService
from ftp_service import FTPService
from knn import KNNClassifier

class Inference(Thread):

    def __init__(self, http, main_window):
        Thread.__init__(self)
        self.http = http
        self.main_window = main_window
        self.ftp = FTPService('192.168.0.109', 'esp', 'esp')
        #self.db = DbService('database.gait')
    
    def run(self):
        time.sleep(30)
        while(True):
            self.ftp.get_videos_and_clean()
            videos = os.listdir('./videos')
            for video in videos:
                folder = './videos/'+video.split('.')[0]
                os.mkdir(folder)
                self.pre_process(folder, './videos/'+video)
                descriptor = self.create_descriptors(folder)
                shutil.rmtree(folder)
                if not descriptor:
                  continue 
                knn = KNNClassifier(1, str(descriptor), 100.0)
                detected_id = knn.classify()
                self.register_log(detected_id)
                shutil.copyfile('./videos/'+video, './assets/last_det.avi')
                os.remove('./videos/'+video)
            if len(videos) > 0:
                self.main_window.update_logs()
            time.sleep(30)

    def register_log(self, id_func):
        db = DbService('database.gait')
        query = """SELECT nivel_acesso FROM funcionarios, cargos
                    WHERE funcionarios.id_cargo = cargos.id_cargo
                    AND id_funcionario = {}""".format(id_func)
        _, result = db.execute_query(query)
        n_acesso = result[0][0]
        aut = 1
        if n_acesso > 0:
            aut = 0
        query = """INSERT INTO log_det (id_funcionario, autorizado, data_det)
                    VALUES ({}, {}, '{}')""".format(id_func, aut, str(datetime.now()).split('.')[0])
        db.execute_query(query)

    def pre_process(self, folder, video):
        video_cap = cv2.VideoCapture(video)
        success, image = video_cap.read()
        count = 0
        while success:
            cv2.imwrite(folder + '/' + str(count) + '.jpg', image)
            success, image = video_cap.read()
            count += 1
    
    def create_descriptors(self, folder):
        payload={}
        frames = os.listdir(folder)
        files = []
        for frame in frames:
            files.append(('files', (frame, open(folder + '/' + frame, 'rb'), 'image/jpeg')))
        headers = {}
        response = requests.request("POST", self.http + '/extractfeatures/', headers=headers, data=payload, files=files)
        if response.status_code == 200:
            return response.json()
        return False
