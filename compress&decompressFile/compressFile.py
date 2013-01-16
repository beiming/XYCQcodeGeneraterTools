import zlib, os, os.path as path

def compress(fileName):
    try:
        xfile = open(fileName, 'rb')
        data = xfile.read()
        xfile.close()

        data = zlib.compress(data, 9)

        wfile = open(path.splitext(fileName)[0] + '.x', 'wb+')
        wfile.write(data)
        wfile.close()
    except IOError, e:
        print e 

def getFiles():
    filesList = os.listdir(os.getcwd())
    filesList = [compress(fileName) for fileName in filesList if path.splitext(fileName)[1] == '.xml']

if __name__ == '__main__':
    getFiles();
    #compress('flashlifeskill.xml')
