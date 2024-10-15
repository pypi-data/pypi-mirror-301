# 安装环境
基础环境安装
``` 
conda create --name quantguard python=3.10.6
conda activate quantguard

```
安装poetry包管理工具

```
pip install poetry

# 解决 poetry publish 问题
pip install urllib3==1.26.6
```

安装项目依赖
```
poetry install
```

开发过程中安装具体某个包
```
poetry add xxx包名
```

发布
```
poetry build
poetry publish
```

启动项目

本地测试
```
请在config目录下创建settings.local.yml填写自己的配置
```
启动
```
quantguard server
```

生成环境安装
```
pip install quantguard==0.1.24 -i https://pypi.Python.org/simple 
```

## 安装superset

卸载本地安装的pandas，因为安装superset容易产生冲突（测试只支持pandas 2.0.3）
```
poetry remove pandas
poetry add apache-superset
```

### 初始化db
```
设置 superset SECRET_KEY, 详见superset_config.py文件
```

### Create an admin user in your metadata database (use `admin` as username to be able to load the examples)
export FLASK_APP=superset
superset db upgrade
superset fab create-admin

### Load some data to play with
superset load_examples

### Create default roles and permissions
superset init

### To start a development web server on port 8088, use -p to bind to another port
superset run -p 8088 --with-threads --reload --debugger