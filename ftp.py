from ftplib import FTP as Ftplib


class FTP:
    def connent(self):
        self.ftp = Ftplib('host')
        self.ftp.login('login', 'password')
        self.ftp.cwd('public_html')

    def disconnent(self):
        self.ftp.quit()
        self.ftp.close()

    def delete(self, file):
        self.ftp.delete(file)

    def getFiles(self):
        return self.ftp.nlst()

    def copy(self, file):
        try:
            self.ftp.cwd('used_keys')
            self.ftp.storbinary('STOR ' + file, '')
        except AttributeError:
            pass

    def create(self, file):
        try:
            self.ftp.storbinary('STOR ' + file, '')
        except AttributeError:
            pass
