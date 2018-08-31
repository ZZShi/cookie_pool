# cookie_pool
cookies池

## 介绍
该cookies池的搭建参考了[崔庆才](https://cuiqingcai.com/)大大的新书<Python3 网络爬虫开发实战>，并在此基础上对架构和部分代码做了优化，
增加了拉勾网与github的模拟登录方法，后续会根据需要增加其它网站，在此对崔大大提供的技术支持表示感谢。

## 第三方库
<br> pip install requests </br>
<br> pip install beautifulsoup4 </br>
<br> pip install redis </br>
<br> pip install flask </br>
<br> 本次数据库存储使用非关系型数据库redis，需要下载安装，官网地址：https://redis.io </br>

## 使用介绍
<br>提供了两种调用方式：</br>
<br>1、url调用：导入cookies模块，调用start_cps()方法运行cookies池，然后访问"http://127.0.0.2:5000/random"  来调用随机cookies</br>
<br>2、数据库调用：导入cookies模块，调用get_cookies_from_db()方法来获取随机cookies

## 框架介绍
<br>Cookies池主要包含六个模块，分别为模拟登录模块、生成器模块、测试器模块、接口模块、存储模块和调度模块：</br>
<br>模拟登录模块：此模块实现了拉勾网与github的模拟登录，可以根据需要添加其它网站，扩展非常方便 </br>
<br>生成器模块：调用模拟登录模块实现对各大网站的模拟登录，并保存cookies到数据库</br>
<br>测试器模块：从数据库调用cookies来测试其是否有效，若无效，则重新登录该账号获取cookies</br>
<br>接口模块：使用flask库对存储模块进行封装，提供可通过url访问的接口</br>
<br>存储模块：对redis数据库的增删查改功能进行封装，提供可供其它模块调用的API</br>
<br>调度模块：对生成器、测试器和接口进行合理调度，使代理池能够协调、高效的运行

## 运行效果
<br> 生成器运行效果： </br>
<br>  </br>
![生成器运行图片加载失败！！！](https://github.com/ZZShi/cookie_pool/blob/master/cookie_pool/result/getter.png)
<br>  </br>

<br> 测试器运行效果： </br>
<br>  </br>
![测试器运行图片加载失败！！！](https://github.com/ZZShi/cookie_pool/blob/master/cookie_pool/result/tester.png)
<br>  </br>

<br> 接口运行效果： </br>
<br>  </br>
![接口运行图片加载失败！！！](https://github.com/ZZShi/cookie_pool/blob/master/cookie_pool/result/api.png)
<br>  </br>

<br> 调度后运行效果： </br>
<br>  </br>
![调度运行图片加载失败！！！](https://github.com/ZZShi/cookie_pool/blob/master/cookie_pool/result/scheduler.png)
<br>  </br>
![调度运行图片加载失败！！！](https://github.com/ZZShi/cookie_pool/blob/master/cookie_pool/result/result.png)
<br>  </br>
![调度运行图片加载失败！！！](https://github.com/ZZShi/cookie_pool/blob/master/cookie_pool/result/result2.png)
<br>  </br>
