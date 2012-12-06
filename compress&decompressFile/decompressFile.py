import zlib, os.path as path

def decompress(fileName):
    try:
        xfile = open(fileName, 'rb')
        data = xfile.read()
        xfile.close()

        data = zlib.decompress(data)

        wfile = open(path.splitext(fileName)[0] + '.xml', 'wb+')
        wfile.write(data)
        wfile.close()
    except IOError, e:
        print e 

if __name__ == '__main__':
    decompress('flashlifeskill.x')
