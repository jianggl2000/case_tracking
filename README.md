## case_tracking
焦急等待中想参考自己申请前后其他人申请的进展，这个python工具用于追踪个人申请前后其它cases申请的进展。使用方法参考，
> python3 case_tracking.py --help

### 关键参数：
> --loc MSC --start 2191580000 --type I-485
查询 MSC2191580000 前500个, 和后500个I-485申请，并将总结结果写到log.txt文件中。

> -v
显示每个结果

其它参数，
```
optional arguments:
  -h, --help            show this help message and exit
  --start START, --from START
                        Start id
  --range RANGE, -n RANGE
                        Search range
  --loc LOC             Process location, default is MSC
  --type TYPE           Petition type, default is I-485
  --seq                 Start with sequential version
  -v                    print all status
  -verr                 print all error message
```
##### 根据以下代码修改
https://github.com/cczhong11/check_uscis_script
