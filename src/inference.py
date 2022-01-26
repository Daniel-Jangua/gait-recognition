import os, cv2, requests, time, shutil
from threading import Thread
from ftp_service import FTPService

class Inference(Thread):

    def __init__(self, http, main_window):
        Thread.__init__(self)
        self.http = http
        self.main_window = main_window
        self.ftp = FTPService('192.168.0.109', 'esp', 'esp')
    
    def run(self):
        while(True):
            self.ftp.get_videos_and_clean()
            videos = os.listdir('./videos')
            for video in videos:
                folder = './videos/'+video.split('.')[0]
                os.mkdir(folder)
                self.pre_process(folder, './videos/'+video)
                descriptor = self.create_descriptors(folder)
                shutil.rmtree(folder)
                print(descriptor) #TODO: executar kNN e salvar resultado no banco de dados -> salvar video em assets/last_det.avi
                os.remove('./videos/'+video)
                if not descriptor:
                    continue
            time.sleep(30)

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
