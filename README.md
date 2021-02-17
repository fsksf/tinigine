# tinigine

模块化、微内核量化回测引擎

# 安装

## 源码安装
```bash
git clone git@github.com:fsksf/tinigine.git
cd tinigine
pip install -e .
```

# 命令

## 更新表结构
```bash
alembic revision --autogenerate -m "commit message"
alembic upgrade head
```

## 查看所有命令
```bash
>>> tinigine
<<<  
Usage: tinigine [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.
  --version   Show the version and exit.

Commands:
  dft-data-update  data_from_tushare: 初始化、更新数据
  dft-gen-config   data_from_tushare: 初始化config文件
  gen-config       生成配置文件

```