

def get_urls():
    info_urls = []
    with open('./info_urls.txt','r') as urlfile:
        lines = urlfile.readlines()
        #判断url格式是否正确
        print(len(lines))

        for j in range(0,1000):
            info_urls.append(lines[j])

            #break
        print('总共%s条url' % (j+1))

    return info_urls

print(get_urls())