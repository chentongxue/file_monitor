## 文件变化监控器

### 作用  
可通过配置需要监控的目录，对目录下的文件进行监控。  
当新增内容中出现给定的关键词，可发送告警信息至企业微信机器人。

### 安装依赖
```shell script
pip install -r requirements.txt -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com
```

### 配置项  
复制 `config.ini` 为 `config.cfg`
```
TASKS = [
    {
        "directory": r'path to directory',  # 需要监控的目录
        "suffix": ".log",  # 需要监控的文件后缀
        "keywords": ["Error"],    # 需要监控的告警关键词
    }
]

# BOT_API = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key='  # 可选， 企业微信机器人 web hook api，不填此项则不通知
ALERT_CD = 3 # 告警间隔(秒)

```


### 启动
```shell script
python manager.py
```

