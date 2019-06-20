### mysmzdm
#### 我的什么值得买

对搜索关键字的好价帖子进行监控，并将最新的帖子购买链接发送到邮箱。

##### 使用
1. 克隆本仓库，并在根目录下执行。
    ```
    python WhenToBuy.py 命令行参数
    ```
2. 获取 docker 镜像, 并使用 docker 运行。
    ```
    docker run -d lindseyzlp/my-experiment:mysmzdm 命令行参数
    ```
##### 命令行参数
-h 帮助   
-k 要查找的内容,默认是 switch   
-s [必填] 发送邮件的qq邮箱地址   
-p [必填] 发送邮件的qq邮箱授权码（如何获得授权码请参考：https://service.mail.qq.com/cgi-bin/help?subtype=1&&id=28&&no=1001256）  
-r [必填] 接收邮件的地址，可以与发送邮箱相同  
    
