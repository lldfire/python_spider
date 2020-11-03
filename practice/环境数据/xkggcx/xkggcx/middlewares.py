class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = self.proxies()

    def proxies(self):
        proxyHost = 'http-dyn.abuyun.com'  # 域名地址
        proxyPort = 9020  # 端口号
        proxyUser = 'H5593W91F90T35DD'  # 通行证书
        proxyPass = '05CDAE49CD411D40'  # 密钥

        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": proxyHost,
            "port": proxyPort,
            "user": proxyUser,
            "pass": proxyPass,
        }

        proxy_handler = {
            "http": proxyMeta,
            "https": proxyMeta,
        }
        # return proxy_handler
        return proxyMeta
