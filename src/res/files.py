#coding=utf-8
# from res_base import *
# from base     import *
import  os , string   , logging
import  interface
_logger = logging.getLogger()

# class links(interface.resource):
#     links_map={}
#     def __init__(self,map):
#         self.ori_map = map
#
#     def _before(self,context):
#         links_map={}
#         for k ,v in self.ori_map.items():
#             k=  env_exp.value(k)
#             v=  env_exp.value(v)
#             self.links_map[k] = v
#     def _config(self,context):
#         cmdtpl ="if test -L $DST ; then rm -rf  $DST ; fi ; dirname $DST | xargs mkdir -p ; ln -s  $SRC $DST"
#         for k ,v in self.links_map.items():
#             cmd = Template(cmdtpl).substitute(DST=k,SRC =v)
#             self.execmd(cmd)
#     def _check(self,context):
#         for k ,v in self.links_map.items():
#             self._check_print(os.path.exists(k),k);
#
#     def _clean(self,context):
#         cmdtpl ="if test -e $DST ; then rm -rf  $DST ; fi "
#         for k ,v in self.links_map.items():
#             cmd = Template(cmdtpl).substitute(DST=k,SRC =v)
#             self.execmd(cmd)


class link(interface.resource):
    """
    !R.link :
        dst: "/home/q/system/mysys"
        src: "$${PRJ_ROOT}/src/apps/console"
    """
    _force   = False
    _dst     = ""
    _src     = ""
    def _before(self,context):
        self.dst = env_exp.value(self.dst)
        self.src = env_exp.value(self.src)

    def _config(self,context):
        cmdtpl = ""
        if self.force is True :
            cmdtpl ="if test -L $DST ; then rm -rf  $DST ; fi ; dirname $DST | xargs mkdir -p ; ln -s  $SRC $DST"
        else :
            cmdtpl ="if ! test -L $DST ; then   dirname $DST | xargs mkdir -p ;  ln -s   $SRC $DST ; fi;  "
        cmd = Template(cmdtpl).substitute(DST=self.dst,SRC =self.src)
        self.execmd(cmd)

    def _clean(self,context):
        self._check_print(os.path.exists(self.dst),self.dst);
        cmdtpl ="if test -e $DST ; then rm -rf  $DST ; fi ; "
        cmd = Template(cmdtpl).substitute(DST=self.dst)
        self.execmd(cmd)

    def _check(self,context):
        self._check_print(os.path.exists(self.dst),self.dst)

    def _info(self):
        return self.src

# class copy(resource,restag_file):
#     """
#     !R.copy:
#         dst: "/home/q/system/mysys/a.txt"
#         src: "$${PRJ_ROOT}/src/apps/console/a.txt"
#     """
#     _dst=None
#     _src=None
#     _force=True
#
#     def _before(self,context):
#         self.dst = env_exp.value(self.dst)
#         self.src = env_exp.value(self.src)
#
#     def _config(self,context):
#         cmdtpl = ""
#         if self.force is True :
#             cmdtpl ="if test -e $DST ; then rm -rf  $DST ; fi ; dirname $DST | xargs mkdir -p ; cp -r  $SRC $DST"
#         else :
#             cmdtpl ="if ! test -e $DST ; then   dirname $DST | xargs mkdir -p ; cp -r  $SRC $DST ; fi;  "
#         cmd = Template(cmdtpl).substitute(DST=self.dst,SRC =self.src)
#         self.execmd(cmd)
#     def _check(self,context):
#         self._check_print(os.path.exists(self.dst),self.dst)
#     def _clean(self,context):
#         cmdtpl ="if test -e $DST ; then rm -rf  $DST ; fi ; "
#         cmd = Template(cmdtpl).substitute(DST=self.dst,SRC =self.src)
#         self.execmd(cmd)
#
# class path(resource,restag_file):
#     """
#     建立path
#     !R.path:
#         dst: "/home/q/system/mysys/"
#         keep: True
#     """
#     _arr        = []
#     _dst        = None
#     _keep       = False
#     _chmod      = "a+w"
#     _auto_sudo  = False
#
#     def _before(self,context):
#         self.paths= []
#         if not self.dst is None:
#             self.paths.append( env_exp.value(self.dst))
#         for v in self.arr:
#             v=  env_exp.value(v)
#             self.paths.append( v )
#     def _checkWrite(self,dst) :
#         while  True  :
#             if os.path.exists(dst) :
#                 return  os.access(dst, os.W_OK)
#             else :
#                 dst = os.path.dirname(dst)
#             if dst == "/"  or dst == "" or dst == "."  or dst == "./"  or dst ==  None :
#                 break
#         return False
#
#
#
#     def _config(self,context):
#         for v in self.paths :
#             if os.path.exists(v)  and self._checkWrite(v) :
#                 continue
#             else :
#                 if not self._checkWrite(v) :
#                     if self.auto_sudo :
#                         self.sudo = True
#                     if not self.sudo :
#                         raise error.rigger_exception( "%s 没有写权限（尝试sudo失败）" %(v) )
#             cmdtpl ="if test ! -e $DST; then   mkdir -p $DST ; fi ;   chmod $CHMOD  $DST; "
#             cmd = Template(cmdtpl).substitute(DST=v,CHMOD=self.chmod)
#             self.execmd(cmd)
#     def _check(self,context):
#         for v in self.paths :
#             self._check_print(os.path.exists(v),v)
#
#     def _clean(self,context):
#         if self.keep :
#             return
#         cmdtpl ="if  test -e $DST ; then rm -rf  $DST ; fi ;  "
#         for v in self.paths :
#             cmd = Template(cmdtpl).substitute(DST=v)
#             self.execmd(cmd)
#
#     def _info(self):
#         if self.dst is None:
#             return ""
#         return self.dst
#
#     def _depend(self,m,context):
#         for v in self.paths :
#             m._check_writeable(v)
#
# class file_merge(resource,restag_file):
#     """
#     文件合并,把src目录下，符合filter的文件内容合并到src文件
#     !R.file_merge
#         dst : "$${PRJ_ROOT}/conf/used/my.conf
#         src : "$${PRJ_ROOT}/conf/option/a/:$${PRJ_ROOT}/conf/option/b/"
#         filter: ".*\.conf"
#
#     """
#     _dst        = None
#     _src        = None
#     _filter     = ".*\.conf"
#     _note       = "#"
#     _mod        = "a+w"
#     def _before(self,context):
#         self.dst        = env_exp.value(self.dst)
#         self.src        = env_exp.value(self.src)
#         self.note       = env_exp.value(self.note)
#         self.mod        = env_exp.value(self.mod)
#         self.filter     = env_exp.value(self.filter)
#     def _config(self,context):
#         with open(self.dst, 'w+') as self.dstfile :
#             srclist = self.src.split(":")
#             for src in srclist:
#                 if not os.path.exists(src):
#                     raise error.rigger_exception("path not exists: %s" %src)
#                 os.path.walk(src,self.proc_file,None)
#         if os.getuid() == os.stat(self.dst).st_uid :
#             # 其它人可以进行修改；
#             self.execmd("chmod %s %s " %(self.mod, self.dst))
#
#
#     def reload(self,context):
#         self._config(context)
#
#     def _check(self,context):
#         self._check_print(os.path.exists(self.dst),self.dst)
#     def _clean(self,context):
#         cmdtpl ="if  test -e $DST ; then rm -f $DST ;fi"
#         cmd = Template(cmdtpl).substitute(DST=self.dst)
#         self.execmd(cmd)
#
#     def proc_file(self,arg,dirname,names):
#         names = sorted(names)
#         for n in names:
#             if re.match(self.filter, n):
#                 src_path = os.path.join(dirname , n )
#                 self.dstfile.write("\n%s file: %s\n" %(self.note,src_path))
#                 self.dstfile.write("%s ------------------------------\n" %(self.note))
#                 if not os.path.exists(src_path) :
#                     warn_msg = "file_merge %s not exists" %src_path
#                     print("warning:  %s" %warn_msg)
#                     _logger.warning(warn_msg)
#                     continue
#                 with open(src_path,'r') as srcfile :
#                     for line in srcfile:
#                         self.dstfile.write(line)
#
# class merge(resource,restag_file):
#     """
#     文件合并,把src目录下，符合filter的文件内容合并到src文件
#     !R.file_merge
#         dst : "$${PRJ_ROOT}/conf/used/my.conf
#         files:
#             - "$${PRJ_ROOT}/a.conf"
#             - "$${PRJ_ROOT}/b.conf"
#     """
#     _files = []
#     _dst = None
#
#     def _before(self,context):
#         self.efiles= []
#         self.dst = env_exp.value(self.dst)
#         for v in self.files:
#             v=  env_exp.value(v)
#             self.efiles.append( v )
#     def _config(self,context):
#         self.execmd(Template("cat /dev/null > $DST; " ).substitute(DST=self.dst))
#         cmdtpl ="cat $SRC >> $DST ;"
#         for v in self.efiles:
#             cmd = Template(cmdtpl).substitute(SRC=v,DST=self.dst)
#             self.execmd(cmd)
#     def _check(self,context):
#         self._check_print(os.path.exists(self.dst),self.dst)
#     def _clean(self,context):
#         cmdtpl ="if  test -e $DST ; then rm -f $DST ; fi  "
#         cmd = Template(cmdtpl).substitute(DST=self.dst)
#         self.execmd(cmd)
#
# class file_tpl(resource,restag_file):
#     """模板文件替换"""
#     _dst    = ""
#     _tpl    = ""
#     _mod    = "a+w"
#
#     def _before(self,context):
#         self.dst        = env_exp.value(self.dst)
#         self.tpl        = env_exp.value(self.tpl)
#         self.mod        = env_exp.value(self.mod)
#
#     def _config(self,context):
#         tpl_builder.build(self.tpl,self.dst)
#         self.execmd("chmod %s %s " %(self.mod, self.dst))
#     def path(self,context):
#         return  self.dst
#     def _check(self,context):
#         self._check_print(os.path.exists(self.dst),self.dst)
#     def _clean(self,context):
#         cmdtpl ="if test -e $DST ; then rm -rf  $DST ; fi "
#         cmd = Template(cmdtpl).substitute(DST=self.dst)
#         self.execmd(cmd)
#     def _info(self):
#         return self.dst
#     def _depend(self,m,context):
#         m._check_writeable(self.dst)
#
#
# class tpl(resource,restag_file):
#     _dst = ""
#     _tpl = ""
#     def _before(self,context):
#         self.dst  = env_exp.value(self.dst)
#         self.tpl  = env_exp.value(self.tpl)
#
#     def _config(self,context):
#         import tpl.tplngin
#         tpl.tplngin.tplworker().execute(self.tpl,self.dst)
#     def _check(self,context):
#         self._check_print(os.path.exists(self.dst),self.dst)
#     def _clean(self,context):
#         cmdtpl ="if test -e $DST ; then rm -rf  $DST ; fi "
#         cmd = Template(cmdtpl).substitute(DST=self.dst)
#         self.execmd(cmd)
#     def _info(self):
#         return self.dst
#     def _depend(self,m,context):
#         m._check_writeable(self.dst)