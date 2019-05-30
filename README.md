# DreamMultiDevices
基于Python/Airtest/Unittest的自动化多设备测试

1.本框架由无声编写，落落测试。
须事先安装如下环境：python3.6以上、airtest、pocoui、BeautifulReport、unittest。须在系统里有适用的adb.exe环境变量。
下载以后，丢到python\Lib\site-packages\ 目录下就好了。

2.config.ini。整个项目的配置文件。
    
    [config]
    packName填写待测试包名，str；
    deviceslist填写测试设备名，以逗号分隔，（PS：如不想使用配置，留空即可，则读取当前所有已连接的设备）元组；
    apkpath填写待测试应用的安装地址，须使用绝对路径，str；
    testcase填写期望测试的用例id，须是一个int元组，RunTestCase函数会比对testcase元组与TestCase目录下的TC_*.py文件，在元组内的用例才会被测试；
    needclickinstall和needclickstartapp 填写True或False，设置是否需要安装点击或运行点击，不为True则不执行；
    timeoutperaction填写全局sleep时间，int；
    timeoutofstartapp填写安装app等待时间，int；
    iteration填写权限脚本循环次数，int。
    
    [TestCaseforDevice]
    按设备配置执行用例，不填则默认全部
    
        
3.start.py。可以使用pycharm运行，也可以在cmd运行。当通过cmd运行时，请务必先cd到根目录，否则会出现找不到模块的情况。

4.core/index。index是整个框架的索引，负责根据devices分发进程，让每个设备各自去运行enterprocess()函数。该()函数里进行设备的初始化，在确保初始化成功、安装包成功的情况下，启动待测试apk并调用RunTestCase函数，进行测试用例的分发。

5.core/MultiADB Madb类，集成了各个与device有关的方法。

6.tools/PushApk2Devices负责安装apk到设备上，会先判断待测包是否已存在，存在则删除并重装，重装时会自动调用inputThread进行安装权限的点击。这里的代码需要用户自行完成，具体写法请参考inputThread里已经提供的示范代码。

7.tools/StartApp。StartApp负责启动apk，然后会进行应用开启权限的点击，此处代码也需要用户自行完成。

8.core/RunTestCase。RunTestCase是运行测试用例的分发函数，读取之前配置表上的testcase元组并与TestCase目录下的文件进行比对，一致的则列入测试范围。

9.TestCase目录。本目录下放置所有的待测试用例。用例须以TC_开头，用例采用标准的unittest格式。每条用例的执行结果会是一个suite对象，并在全部执行完以后，聚合到RunTestCase的report对象上。

10.TestCast/TC_******.py 单个用例的执行文件，由用户自行编写，最后须符合unittest格式。特别要说明一点，BeautifulReport的默认截图方法是异常时触发语法糖截图。使用时略有不便，我新增了GetScreen()函数，可以在任意需要时实时截图。

11.Report/Html报告。RunTestCase使用BeautifulReport库进行报告输出。输入内容在\Report目录下。以设备名和时间命名。相关截图则存储在Report\Screen目录下。



