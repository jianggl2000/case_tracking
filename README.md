## case_tracking
焦急等待中想参考自己申请前后其它申请的进展？这个python工具可用于追踪个人申请前后其它cases。
使用方法参考，
> python3 case_tracking.py --help

### 关键参数：
> --loc MSC --my 2191580000 --type I-485

查询 MSC2191580000 前500个, 和后500个中I-485申请，并将结果总结写到log.txt文件中。

> -v

显示每个case结果

### 运行及结果解释
> python3 case_tracking.py --loc MSC --my 2191580000 --type I-485 -n 100
```
Search 100 cases BEFORE MSC2191580000, from MSC2191579900 to MSC2191579999, for I-485
                MSC2191579928: Fees Were Waived
                MSC2191579940: Fees Were Waived
Received: 19; Fingerprinted: 0; Transferred: 0; Rejected: 11; RFIE: 0; Others: 2; Total: 32/100
```
此处为MSC2191580000前100个case中I485进展，一共32个485申请，19个Received, 11个Rejected, 2个其它情况，具体内容显示在上方："Fees were Waived".
```
Search for 100 cases AFTER MSC2191580000, from MSC2191580000 to MSC2191580099, for I-485
                MSC2191580009: Fees Were Waived
                MSC2191580006: Fees Were Waived
                MSC2191580012: Fees Were Waived
                MSC2191580007: Fees Were Waived
                MSC2191580010: Fees Were Waived
                MSC2191580011: Fees Were Waived
                MSC2191580049: Case Transferred To Another Office
                MSC2191580052: Case Transferred To Another Office
                MSC2191580046: Case Transferred To Another Office
                MSC2191580055: Case Transferred To Another Office
                MSC2191580073: Fees Were Waived
                MSC2191580088: Fees Were Waived
                MSC2191580074: Fees Were Waived
                MSC2191580089: Fees Were Waived
                MSC2191580093: Fees Were Waived
Received: 19; Fingerprinted: 0; Transferred: 0; Rejected: 4; RFIE: 0; Others: 15; Total: 38/100
```
此处为MSC2191580000和其后100个case中I485进展

其它参数，
```
optional arguments:
  -h, --help            show this help message and exit
  --start START, --my START
                        Start id
  --range RANGE, -n RANGE
                        Search range
  --loc LOC             Process location, default is MSC
  --type TYPE           Petition type, default is I-485
  --seq                 Start with sequential version
  -v                    print all status
  -verr                 print all error message
```
##### 基于以下代码修改
https://github.com/cczhong11/check_uscis_script
安装请参考此网站
