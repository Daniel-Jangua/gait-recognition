from ftplib import FTP

class FTPService():

    def __init__(self, host, user, passwd):
        self.ftp = FTP(host)
        self.ftp.login(user, passwd)
        print('FTP Connected.')
    
    def list_recent_videos(self):
        files = self.ftp.nlst()
        return files
    
    def get_videos_and_clean(self):
        print('Listing files.')
        files = self.list_recent_videos()
        for file in files:
            if '.avi' in file:
                handle = open('./videos/' + file.split('/')[-1], 'wb')
                print('Getting file: ' + file)
                if self.ftp.size(file) > 0:
                    print('File {} has 0 bytes.'.format(file))
                    self.ftp.retrbinary('RETR %s' % file, handle.write)
                print('Deleting file: ' + file)
                self.ftp.delete(file)

if __name__ == '__main__':
    ftp_service = FTPService('192.168.0.109', 'esp', 'esp')
    ftp_service.get_videos_and_clean()
