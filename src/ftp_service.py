from ftplib import FTP

class FTPService():

    def __init__(self, host, user, passwd):
        self.ftp = FTP(host)
        self.ftp.login(user, passwd)
    
    def list_recent_videos(self):
        files = self.ftp.nlst()
        return files
    
    def get_videos_and_clean(self):
        files = self.list_recent_videos()
        for file in files:
                handle = open('./videos/' + file.split('/')[-1], 'wb')
                print('Getting file: ' + file)
                self.ftp.retrbinary('RETR %s' % file, handle.write)
                print('Deleting file: ' + file)
                self.ftp.delete(file)

if __name__ == '__main__':
    ftp_service = FTPService('192.168.0.109', 'esp', 'esp')
    ftp_service.get_videos_and_clean()
