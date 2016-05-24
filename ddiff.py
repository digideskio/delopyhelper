#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os,sys,filecmp

# 参数校验
def check(args):
    if len(args) == 3:
        des = args[1]
        src = args[2]
        print "线上目录: " + des
        print "构建目录: " + src
        return os.path.exists(des) and os.path.isdir(des) and os.path.exists(src) and os.path.isdir(src)
    else:
        print "使用示例: python ddiff.py 线上配置目录 构建包配置目录"
        print "比较 线上配置目录与构建包配置目录的不同."
        return False

# 遍历目录获取所有的文件
def walk_dir(dir,topdown=True):
    dirArrays = []
    rootPath = ""
    for root, dirs, files in os.walk(dir, topdown):
        if rootPath == "":
            rootPath = root
        for name in files:
            absPath = root+"/"+name
            absPath = absPath[len(rootPath)+1:]
            dirArrays.append(absPath)
    return dirArrays

# 显示新增配置文件
def find_new(desfiles,srcfiles):
    print "\n--查找线上多余文件--"
    for dfile in desfiles:
        if not dfile in srcfiles:
            print "----------> " + des + "/" +  dfile
            print "            " + "删除 rm " + des + "/" +  dfile
    print "--多余文件查找完成--\n"

# 显示删除配置文件
def find_rem(desfiles,srcfiles):
    print "\n--查找新增文件--"
    for sfile in srcfiles:
        if not sfile in desfiles:
            print "----------> " + src + "/" + sfile
            print "            " + "增加 cp " + src + "/" + sfile + " " + des + "/" + sfile
    print "--新增文件查找完成--\n"

# 找出两边都存在的文件
def find_both(desfiles,srcfiles):
    samefiles = []
    for dfile in desfiles:
        if dfile in srcfiles:
            samefiles.append(dfile)
    return samefiles

# 找出不一致文件
def find_modify(bothfiles):
    print "\n--查找修改文件--"
    for name in bothfiles:
        if not filecmp.cmp(des+"/"+name,src+"/"+name):
            print "----------> " + des+"/"+name + " <vs> " + src+"/"+name
            print "            详情 " + "diff " + des+"/"+name + " " + src+"/"+name
            print "            使用构建 " + "cp " + src+"/"+name + " " + des+"/"+name
    print "--修改文件查找完成--\n"

# 读取properties文件生成map
def build_map(filename):
    properties = {}
    for line in open(filename):
        line = line.strip()
        if not line.startswith("#"):
            kvs = line.split("=")
            if len(kvs) == 2:
                properties[kvs[0].strip()]=kvs[1].strip()
    return properties

# 对比两个map
def map_cmp(desmap,srcmap):
    for k,v in desmap.items():
        if k in srcmap:
            if not srcmap[k] == v:
                print "            配置的值不同 " + k + " " + v + "(线上) vs " + srcmap[k] + "(构建包)"
        else:
            print "            删除的属性   " + k + " " + v
    for k,v in srcmap.items():
        if not k in desmap:
            print "            新增的配置   " + k + " " + v

# 对比properties
def properties_cmp(bothfiles):
    print "\n--对比属性文件--"
    for bfile in bothfiles:
        if bfile.endswith(".properties"):
            if not filecmp.cmp(des+"/"+bfile,src+"/"+bfile):
                print "----------> 发现配置不同 " + des+"/"+bfile + " <vs> " + src+"/"+bfile
                desmap = build_map(des+"/"+bfile)
                srcmap = build_map(src+"/"+bfile)
                map_cmp(desmap,srcmap)
    print "--对比属性文件完成--\n"

# 脚本主体
if  check(sys.argv):
    print "\n校验参数成功,程序将自动对比"
    des = sys.argv[1]
    src = sys.argv[2]
    desfiles = walk_dir(des)
    srcfiles = walk_dir(src)
    find_new(desfiles,srcfiles)
    find_rem(desfiles,srcfiles)
    bothfiles = find_both(desfiles,srcfiles)
    find_modify(bothfiles)
    properties_cmp(bothfiles)
else:
    print "\n校验失败,程序将推出"
