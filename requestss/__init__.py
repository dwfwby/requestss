import urllib.parse, urllib.request
import http.cookiejar

class request:
    def __init__(this, proxy = {}, needCookie = 0):
        this._setProxy(proxy)
        this._createCookieJar()
        this._createCookieProcessor(needCookie)
        this._createOpener()
    
    def get(this, url, headers = []):
        return this.send(url, headers)
    
    def post(this, url, headers = [], data = {}):
        return this.send(url, headers, data)
    
    def send(this, url, headers, data = {}):
        data = this._normalBody(data)
        this.setHeaders(headers)
        return this._opener.open(url, data=data)

    def readCookie(this, content):
        return content.headers.get_all('Set-Cookie')

    def setHeaders(this, headers):
        this._opener.addheaders = this._normalHeaders(headers)
    
    def _normalHeaders(this, headers):
        return headers and list(headers.items())
    
    def _normalBody(this, data = None):
        return (data or None) and urllib.parse.urlencode(data).encode('ascii')
    
    def _normalProxies(this, proxy = None):
        return proxy and {"http": f'http://{proxy}',"https": f'http://{proxy}'}
    
    def _setProxy(this, proxy = None):
        this._createProxyHandler(this._normalProxies(proxy))
    
    def _createProxyHandler(this, args):
        this._proxy_handler = urllib.request.ProxyHandler(args)
    
    def _createCookieJar(this):
        this._cj = http.cookiejar.CookieJar()
    
    def _createCookieProcessor(this, status):
        this._cproc = urllib.request.HTTPCookieProcessor(this._cj) if status else None
    
    def _createOpener(this):
        this._opener = urllib.request.build_opener(this._proxy_handler, this._cproc)
