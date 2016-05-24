#### 整体说明

***

使用说明：

* 把xxxx的online目录(现网配置共享)挂载到本地(可以当本地目录使用)

  ```shell
  # 出现错误的话 yum install "cifs*"
  # 挂载online目录
  mount -t cifs //XXXX/online /data/scguo/online  -o username=XXX,password=XXX
  ```


* 把上线包拷贝到对应的目录
* 对比线上和构建包的配置文件输出不同项，需要自己选择和修改

##### ddiff.py

配置对比工具(ddiff.py),对比线上目录和构建目录的不同;

```shell
#使用示例 online为线上目录 package为构建包目录
python ddiff.py online package
```

1. 发现线上目录多余的配置文件,并提供删除的语句;
2. 发现构建包新增的配置文件,并提供复制语句;
3. 发现线上包与构建包不一致的文件;
4. 对比properties配置文件;
   1. 发现新增配置项;
   2. 发现删除配置项;
   3. 发现修改配置项;




```shell
# 输出实例
python ddiff.py conf1 conf2

线上目录: conf1
构建目录: conf2

校验参数成功,程序将自动对比

--查找线上多余文件--
----------> conf1/config/biz/dubbo.properties
            删除 rm conf1/config/biz/dubbo.properties
--多余文件查找完成--


--查找新增文件--
----------> conf2/config/dbaccess/redis/redis-config-SortedII.properties
            增加 cp conf2/config/dbaccess/redis/redis-config-SortedII.properties conf1/config/dbaccess/redis/redis-config-SortedII.properties
--新增文件查找完成--


--查找修改文件--
----------> conf1/config/biz/nettyhttp.properties <vs> conf2/config/biz/nettyhttp.properties
            详情 diff conf1/config/biz/nettyhttp.properties conf2/config/biz/nettyhttp.properties
            使用构建 cp conf2/config/biz/nettyhttp.properties conf1/config/biz/nettyhttp.properties
--修改文件查找完成--


--对比属性文件--
----------> 发现配置不同 conf1/config/biz/nettyhttp.properties <vs> conf2/config/biz/nettyhttp.properties
            删除的属性   max_thread_num 999
            配置的值不同 thread_num 99(线上) vs 9(构建包)
            新增的配置   min_thread_num 1
--对比属性文件完成--
```
