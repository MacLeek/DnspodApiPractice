import urllib2, urllib
try: import json
except: import simplejson as json
import re

class ApiCn:
    def __init__(self, email, password, **kw):
        self.base_url = "https://dnsapi.cn"
        
        self.params = dict(
            login_email=email,
            login_password=password,
            format="json",
            lang="cn"
        )
        self.params.update(kw)
        self.path = None
    
    def request(self, **kw):
        self.params.update(kw)
        if not self.path:
            """Class UserInfo will auto request path /User.Info."""
            name = re.sub(r'([A-Z])', r'.\1', self.__class__.__name__)
            self.path = "/" + name[1:]
        #headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/json", "User-Agent": "dnspod-python/0.01 (im@chuangbo.li; DNSPod.CN API v2.8)"}
        req=urllib2.Request(self.base_url+self.path)
        opener=urllib2.build_opener(urllib2.HTTPCookieProcessor())
        response = opener.open(req, urllib.urlencode(self.params)) 
        data = response.read()
        ret = json.loads(data)
        #if ret.get("status", {}).get("code") == "1":
        return ret
        
    __call__ = request

class UserInfo(ApiCn):
    pass

class UserDetail(ApiCn):
    pass

class DomainCreate(ApiCn):
    def __init__(self, domain, **kw):
        kw.update(dict(domain=domain))
        ApiCn.__init__(self, **kw)

class DomainList(ApiCn):
    pass

class _DomainApiBase(ApiCn):
    def __init__(self, domain_id, **kw):
        kw.update(dict(domain_id=domain_id))
        ApiCn.__init__(self, **kw)

class DomainRemove(_DomainApiBase):
    pass

class DomainStatus(_DomainApiBase):
    def __init__(self, status, **kw):
        kw.update(dict(status=status))
        _DomainApiBase.__init__(self, **kw)

class RecordList(_DomainApiBase):
    pass

class RecordCreate(_DomainApiBase):
    def __init__(self, sub_domain, record_type, record_line, value, ttl, mx=None, **kw):
        kw.update(dict(
            sub_domain=sub_domain,
            record_type=record_type,
            record_line=record_line,
            value=value,
            ttl=ttl,
        ))
        if mx:
            kw.update(dict(mx=mx))
        _DomainApiBase.__init__(self, **kw)

class RecordModify(RecordCreate):
    def __init__(self, record_id, **kw):
        kw.update(dict(record_id=record_id))
        RecordCreate.__init__(self, **kw)

class _RecordBase(_DomainApiBase):
    def __init__(self, record_id, **kw):
        kw.update(dict(record_id=record_id))
        _DomainApiBase.__init__(self, **kw)

class RecordRemove(_RecordBase):
    pass
    
class RecordInfo(_RecordBase):
    pass
