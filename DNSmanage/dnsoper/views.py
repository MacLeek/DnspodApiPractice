#/usr/bin/python
#coding: utf8
#todo:使用缓存优化

from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.core.urlresolvers import reverse
from api import *
import os
import sys 
reload(sys) 
sys.setdefaultencoding('utf8') 
# app specific files

#views start from here

#登录
def login(request):
    msg=''
    #如果已经session中存在登录，直接跳转到用户中心
    if request.session.get('is_login') == True:
        return HttpResponseRedirect("/dnsoper/usercenter")
    #没有登录，或者登录失败，则进入登录页面
    else:
        if request.method == "POST":
            user = UserDetail(email=request.POST['username'], password=request.POST['password'])
            if user().get("status", {}).get("code") == "1":
                msg='登录成功!'
                request.session['email'] = request.POST['username']
                request.session['password'] = request.POST['password']
                request.session['is_login'] = True
                request.session['username'] = user().get("info").get("user")["nick"]
                return HttpResponseRedirect("/dnsoper/usercenter")
            else:
                msg='登录失败!请确保您的用户名或密码是否正确'
    t=get_template('dnsoper/login.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))

#用户信息
def userCenter(request):
    userdetails={}
    #已经登录则显示用户中心
    if request.session.get('is_login') == True:
        user = UserDetail(email=request.session['email'], password=request.session['password'])
        userdetails=user().get("info").get("user")
    #否则跳转到登录页面
    else:
        return HttpResponseRedirect("/dnsoper/login")
    t=get_template('dnsoper/usercenter.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))

#todo:1.超过三千域名后分页 2.删除域名使用jquery post,不然会多次调用urlilb
def myDomains(request):
    domains = {}
    msg = ''
    if request.session.get('is_login') == True:
        if request.method == "POST":
            domainids=request.POST.getlist('check')
            if request.POST.has_key('del'):
                for domainid in domainids:
                    result = DomainRemove(email=request.session['email'], password=request.session['password'],domain_id=domainid)
                    msg = result().get("status").get("message")
            elif request.POST.has_key('status'):
                for domainid in domainids:
                    result = DomainStatus(request.POST['status'],email=request.session['email'], password=request.session['password'],domain_id=domainid)
                    msg = result().get("status").get("message")
        Domains = DomainList(email=request.session['email'], password=request.session['password'])
        domains=Domains().get("domains")
    else:
        return HttpResponseRedirect("/dnsoper/login")
    t=get_template('dnsoper/mydomains.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))

#增加域名
def addDomain(request):
    status = ''
    msg = ''
    if request.session.get('is_login') == True:
        if request.method == "POST":
            result = DomainCreate(email=request.session['email'], password=request.session['password'],domain=request.POST['domain'])
            if result().get("status").get("code") == "1":
                msg = '域名添加成功'
                return HttpResponseRedirect("/dnsoper/mydomains")
            #失败显示错误信息
            else:
                msg = result().get("status").get("message")
    else:
        return HttpResponseRedirect("/dnsoper/login")
    t=get_template('dnsoper/adddomain.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))

def modDomain(request):
    pass

#域名视图
def domainview(request,domainid):
    msg = ''
    if request.session.get('is_login') == True:
        if request.method == "POST":
            recordids=request.POST.getlist('check')
            #assert False
            for recordid in recordids:
                result = RecordRemove(email=request.session['email'], password=request.session['password'],domain_id=domainid,record_id=recordid)
                #添加成功跳转回域名视图
                if result().get("status").get("code") == "1":
                    msg = '记录删除成功'
                    return HttpResponseRedirect("/dnsoper/domain/"+domainid)
                #失败显示错误信息
                else:
                    msg = result().get("status").get("message")
        Domains = RecordList(email=request.session['email'], password=request.session['password'],domain_id=domainid)
        records = Domains().get("records")
    else:
        return HttpResponseRedirect("/dnsoper/login")
    t=get_template('dnsoper/domain.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))

#增加记录
def addRecord(request,domainid):
    status = ''
    msg = ''
    if request.session.get('is_login') == True:
        if request.method == "POST":
            result = RecordCreate(request.POST['sub_domain'], request.POST['record_type'].encode("utf8"), request.POST['record_line'].encode("utf8"), request.POST['value'], request.POST['ttl'], domain_id=domainid, email=request.session['email'], password=request.session['password'])
            #添加成功跳转回域名视图
            if result().get("status").get("code") == "1":
                msg = '记录添加成功'
                return HttpResponseRedirect("/dnsoper/domain/"+domainid)
            #失败显示错误信息
            else:
                msg = result().get("status").get("message")
    else:
        return HttpResponseRedirect("/dnsoper/login")
    t=get_template('dnsoper/addrecord.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))

#修改记录
def modRecord(request,domainid,recordid):
    status = ''
    msg = ''
    if request.session.get('is_login') == True:
        if request.method == "POST":
            result = RecordModify(recordid,sub_domain=request.POST['sub_domain'], record_type=request.POST['record_type'].encode("utf8"), record_line=request.POST['record_line'].encode("utf8"), value=request.POST['value'], ttl=request.POST['ttl'], domain_id=domainid,email=request.session['email'], password=request.session['password'])
            #添加成功跳转回域名视图
            if result().get("status").get("code") == "1":
                msg = '记录添加成功'
                return HttpResponseRedirect("/dnsoper/domain/"+domainid)
            #失败显示错误信息
            else:
                Record = RecordInfo(email=request.session['email'], password=request.session['password'],domain_id=domainid,record_id=recordid)
                record = Record().get("record")
                msg = result().get("status").get("message")
        else:
            Record = RecordInfo(email=request.session['email'], password=request.session['password'],domain_id=domainid,record_id=recordid)
            record = Record().get("record")
    else:
        return HttpResponseRedirect("/dnsoper/login")
    t=get_template('dnsoper/modrecord.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))

#注销用户
def logout(request):
    try:
        del request.session["is_login"]
        del request.session["email"]
        del request.session["password"]
        del request.session["username"]
    except KeyError:
        pass
    return HttpResponseRedirect("/dnsoper/login")

def exportRecords(request,domainid):
    if request.session.get('is_login') == True:
        Domains = RecordList(email=request.session['email'], password=request.session['password'],domain_id=domainid)
        records = Domains().get("records")
        content="主机|类型|线路|记录值|MX优先级|TTL\n"
        for record in records:
            #记录有空格用半角引出
            if record["value"].find(' ') != -1:
                record["value"] = '"'+record["value"]+'"'
            content+=record["name"].encode("utf8")+"   "+record["type"].encode("utf8")+"   "+record["line"].encode("utf8")+"   "+record["value"].encode("utf8")+"   "+record["mx"].encode("utf8")+"   "+record["ttl"].encode("utf8")+"\n"
        #如果使用sae服务器部署
        if 'SERVER_SOFTWARE' in os.environ:
            import sae.storage       
            s = sae.storage.Client()
            test = sae.storage.Object(content)
            url = s.put('media', 'export'+str(domainid), test)
            HttpResponseRedirect(url)
        #本地
        else:
            HERE = os.path.dirname(__file__)
            f=open(HERE+'/../static/export'+str(domainid)+'.txt','wb')
            f.write(content)
            f.close()
        return HttpResponseRedirect("/static/export"+str(domainid)+".txt")
    else:
        return HttpResponseRedirect("/dnsoper/login")

def importRecords(request,domainid):
    msg=''
    if request.session.get('is_login') == True:
        if request.method == "POST":
            try:
                content = request.FILES['file']
                data = ''.join(content.readlines())
                records = data.split("\n")
                records=records[1:]
                #items = records[0].split('  ')
                #a=items[1]
                for i in range(len(records)-1):
                    items=records[i].split('  ')
                    sub_domain = items[1]
                    record_type = str(items[1])
                    record_line = items[2]
                    value = items[3]
                    ttl = items[4]
                    result = RecordCreate(sub_domain,record_type, record_line.encode("utf8"), value.encode("utf8"), ttl.encode("utf8"), domain_id=domainid, email=request.session['email'], password=request.session['password'])            
                    msg=msg+records[i]+':'+result().get("status").get("message")+"<br>"
                #return HttpResponseRedirect("/dnsoper/domain/"+domainid)
            except:
                pass
        t=get_template('dnsoper/importrecords.html')
        c=RequestContext(request,locals())
        return HttpResponse(t.render(c))

    else:
        return HttpResponseRedirect("/dnsoper/login")

