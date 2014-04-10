from django.conf.urls.defaults import *
from views import *
urlpatterns = patterns('',
                       (r'login/$', login),
                       (r'logout/$', logout),
                       (r'usercenter/$', userCenter),
                       (r'mydomains/$', myDomains),
                       (r'adddomain/$', addDomain),
                       (r'moddomain/$', modDomain),
                       (r'domain/(?P<domainid>[^/]+)/$', domainview),
                       (r'addrecord/(?P<domainid>[^/]+)/$', addRecord),
                       (r'modrecord/(?P<domainid>[^/]+)/(?P<recordid>[^/]+)/$', modRecord),
                       (r'export/(?P<domainid>[^/]+)/$', exportRecords),
                       (r'import/(?P<domainid>[^/]+)/$', importRecords),
                       )