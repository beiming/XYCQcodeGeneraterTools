import zlib, os.path as path

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

if __name__ == '__main__':
    compress('flashlifeskill.xml')
