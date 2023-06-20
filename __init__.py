import urllib.parse, urllib.request
import http.cookiejar

def dictToList(d = None):
    return d and list(d.items())

def encodeBody(data = None):
    return data and urllib.parse.urlencode(data).encode('ascii')

def normalProxies(proxy = None):
    return proxy and {"http": f'http://{proxy}'}

def simpleCookieProcessor():
    return createCookieProcessor(createCookieJar())

def simpleProxyHandler(proxy = None):
    return createProxyHandler(normalProxies(proxy))

def simpleOpener(proxy = None):
    return createOpener(simpleProxyHandler(proxy), simpleCookieProcessor())

def createProxyHandler(args):
    return urllib.request.ProxyHandler(args)

def createCookieJar():
    return http.cookiejar.CookieJar()

def createCookieProcessor(cookie_jar):
    return urllib.request.HTTPCookieProcessor(cookie_jar)

def createOpener(proxy_handler, cookie_processor):
    return urllib.request.build_opener(proxy_handler, cookie_processor)

def createSession(headers = [], proxy = None):
    opener = simpleOpener(proxy)
    opener.addheaders = dictToList(headers)
    return opener

def sessionSend(opener, url, data = None, timeout = 10):
    return opener.open(url, data=encodeBody(data), timeout=timeout).read()

def send(url, headers = {}, timeout = 10, proxy = None, data = None):
    opener = createSession(headers, proxy)
    response = sessionSend(opener, url, encodeBody(data), timeout)
    opener.close()
    return response

def sendUTF8(url, headers = {}, timeout = 10, proxy = None, data = None):
    return send(url, headers, timeout, proxy, data).decode('utf-8')
