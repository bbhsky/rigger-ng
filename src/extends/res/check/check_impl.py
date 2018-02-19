#coding=utf8
import re,logging
import interface,utls.rg_var,utls.rg_json
import utls.dbc , utls.check
import copy
import hashlib
from utls.rg_io import  rgio , run_struct,rg_logger
from utls.tpl.tpl_var import safe_env_porp
from impl.rg_utls import *
from utls.rg_sh  import shexec
from utls.rg_var import value_of
from impl.rg_utls import *
from res.base   import *

def cacu_file_sha(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.sha256()
    f = file(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
    hash_code = myhash.hexdigest()
    f.close()
    return str(hash_code).lower()

def cacu_md5(data):
    myhash = hashlib.md5()
    myhash.update(data)
    hash_code = myhash.hexdigest()
    return str(hash_code).lower()

def have_cmd(expect,dst) :
    arr = dst.split(',')
    for i in arr :
        if i.strip()  == expect.strip() :
            return True
    return False

def assert_value(value,expect,is_raise=True):
    if value.strip() != expect.strip() :
        if is_raise :
            raise interface.rigger_exception("value: %s , expect: %s " %(value,expect))
        return False ;
    return True

class assert_base(interface.resource,res_utls) :
    def _allow(self,context):
        return True
    def _config(self,context):
        if have_cmd('conf',self.run) :
            self.assert_do(context)
    def _start(self,context) :
        if have_cmd('start',self.run) :
            self.assert_do(context)

    def _check(self,context):
        if have_cmd('check',self.run) :
            result = self.assert_do(context,False)
            self._check_print(result,self.file)

class assert_file_sha(assert_base) :
    """
    sha use sha256, centos: sha256sum
    !R.assert_file_sha
    file  : ""
    sha   : ""
    run   : "check"  "check,conf,start"
    """
    name = "assert_file_sha"
    run  = "check"
    def assert_do(self,context,is_raise = True):
        dst        = res_utls.value(self.file)
        sha        = res_utls.value(self.sha)
        dst_sha    = cacu_file_sha(dst)
        if sha != dst_sha:
            if is_raise :
                raise interface.rigger_exception("file MD5: %s , expect MD5 : %s " %(dst_sha,sha))
            return False
        return True

class assert_url_code(assert_base):
    """
    !R.assert_url_code
    url  : ""
    head : ""
    code : "200"
    run  : "check"  "check,conf,start"
    """
    name = "assert_url_sha"
    code = "200"
    run  = "check"


    def assert_do(self,context,is_raise=True):
        value  = self.do_curl(context)
        expect = res_utls.value(self.code)
        return assert_value(value,expect,is_raise)
    def do_curl(self,context) :
        self.url  = res_utls.value(self.url)
        self.file = context.run_path +"/" +  cacu_md5(self.url) + ".http_code"
        cmd = "curl -I -s -m 10 -w %{http_code} \"$URL\" -X GET -o /dev/null > $OUT"
        cmd = Template(cmd).substitute(URL=self.url,OUT=self.file)
        shexec.execmd(cmd)
        code = open(self.file).readline()
        return code




class assert_url_sha(assert_base) :
    """
    sha use sha256, centos: sha256sum
    !R.assert_file_sha
    url  : ""
    head  : ""
    sha   : ""
    run   : "check"  "check,conf,start"
    """
    name = "assert_url_sha"
    head = ""
    run  = "check"

    def assert_do(self,context,is_raise=True):
        value  = self.do_curl(context)
        expect = res_utls.value(self.sha)
        return assert_value(value,expect,is_raise)

    def do_curl(self,context) :
        self.url  = res_utls.value(self.url)
        self.head = res_utls.value(self.head)
        self.file = context.run_path +"/" +  cacu_md5(self.url) + ".http_out"
        cmd = "curl -m 10 -s \"$URL\" -X GET -o $OUT"
        shexec.execmd(Template(cmd).substitute(URL=self.url,OUT=self.file))
        return  cacu_file_sha(self.file)

