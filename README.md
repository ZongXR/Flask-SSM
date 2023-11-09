<h1>Flask-SSM</h1>
这是在flask基础上，二次开发的web框架Flask-SSM，完全按照MVC分层的思想实现，对于没有web基础但需要做web项目的人可起到教学作用。尤其有助于java转python的web开发，让你按照java的思路写python
<h2>使用方法</h2>
<p># TODO 待更新。。。</p>
<h2>版本更新</h2>
<table>
<tr>
<th>版本</th><th>更新内容</th><th>更新日期</th>
</tr>
<tr>
<td>1.0.0.0</td><td>完成模板搭建，实现MVC分层，现在可以自助接入自定义内容。</td><td>2022年1月2日</td>
</tr>
<tr>
<td>1.1.0.0</td><td>完善模板，现在可以在controller下自建多级包</td><td>2022年1月9日</td>
</tr>
<tr>
<td>1.1.1.0</td><td>完善模板，现在可以在service下自建多级包</td><td>2022年1月10日</td>
</tr>
<tr>
<td>1.1.2.0</td><td>完善模板，现在可以在task下自建多级包</td><td>2022年1月11日</td>
</tr>
<tr>
<td>1.1.2.1</td><td>添加模板目录</td><td>2021年1月30日</td>
</tr>
<tr>
<td>1.2.0.0</td><td>service层设置为单例模式;补充SQLalchemy的点查询demo</td><td>2022年7月14日</td>
</tr>
<tr>
<td>1.3.0.0</td><td>分离pojo和dao</td><td>2022年7月16日</td>
</tr>
<tr>
<td>1.3.1.0</td><td>输出更多日志</td><td>2022年7月16日</td>
</tr>
<tr>
<td>1.3.2.0</td><td>增加ViewObject; 增加logs目录</td><td>2022年8月5日</td>
</tr>
<tr>
<td>1.4.0.0</td><td>修改前端页面，可自定义请求方式、mime值、url、请求正文; 更改数据库用户名密码; 输出更多日志</td><td>2022年8月5日</td>
</tr>
<tr>
<td>1.4.1.0</td><td>修改前端页面样式</td><td>2022年8月5日</td>
</tr>
<tr>
<td>1.5.0.0</td><td>新增自定义异常及全局、局部异常处理</td><td>2022年8月5日</td>
</tr>
<tr>
<td>1.5.1.0</td><td>优化导入包路径</td><td>2022年8月5日</td>
</tr>
<tr>
<td>1.5.2.0</td><td>将多个Controller分布到不同的蓝图</td><td>2022年8月7日</td>
</tr>
<tr>
<td>1.6.0.0</td><td>将蓝图注册与初始化解耦，自动将py模块注册为蓝图; 异常handler增加日志输出</td><td>2022年8月7日</td>
</tr>
<tr>
<td>1.7.0.0</td><td>规范命名; service使用模块自动单例模式</td><td>2022年8月10日</td>
</tr>
<tr>
<td>1.7.0.1</td><td>优化代码; 更新使用说明</td><td>2022年8月11日</td>
</tr>
<tr>
<td>1.8.0.0</td><td>现在不需要把BluePrint对象命名为bp，也能实现蓝图的自动注册</td><td>2022年8月13日</td>
</tr>
<tr>
<td>1.8.0.1</td><td>fix some bugs</td><td>2022年8月13日</td>
</tr>
<tr>
<td>1.9.0.0</td><td>解耦task、controller、config、utils各个子模块，不需要的模块直接删除即可；fix some bugs</td><td>2022年12月28日</td>
</tr>
<tr>
<td>2.0.0.0</td><td>优化代码，提升执行效率</td><td>2022年12月28日</td>
</tr>
<tr>
<td>2.1.0.0</td><td>修复BUG; 新增事务管理器; 新增工具类</td><td>2023年4月27日</td>
</tr>
<tr>
<td>2.2.0.0</td><td>新增运行入口; 新增docker部署运行方式</td><td>2023年5月22日</td>
</tr>
<tr>
<td>2.2.1.0</td><td>暴露端口5000</td><td>2023年5月22日</td>
</tr>
<tr>
<td>2.2.2.0</td><td>排除目录<code>docs</code>, <code>sql</code></td><td>2023年5月22日</td>
</tr>
<tr>
<td>2.2.2.1</td><td>add some exclude path</td><td>2023年5月22日</td>
</tr>
<tr>
<td>2.2.2.2</td><td>修复数据库连接包含特殊字符导致无法连接的BUG</td><td>2023年5月26日</td>
</tr>
<tr>
<td>2.3.0.0</td><td>新增单元测试功能; 前端新增PUT和DELETE请求方式; 规范dao的用法</td><td>2023年5月26日</td>
</tr>
<tr>
<td>2.3.0.1</td><td>fix some bugs</td><td>2023年5月29日</td>
</tr>
<tr>
<td>2.4.0.0</td><td>add initializer</td><td>2023年5月30日</td>
</tr>
<tr>
<td>2.4.0.1</td><td>fix some bugs</td><td>2023年5月30日</td>
</tr>
<tr>
<td>2.4.0.2</td><td>fix some bugs</td><td>2023年5月31日</td>
</tr>
<tr>
<td>2.4.0.3</td><td>fix some bugs</td><td>2023年6月1日</td>
</tr>
<tr>
<td>2.5.0.0</td><td>add mapper decorator; fix some bugs; add unit test example; change dao function usage</td><td>2023年6月2日</td>
</tr>
<tr>
<td>2.5.1.0</td><td><code>@mapper</code>新增<code>np.ndarray</code>类型支持, 新增其他自定义参数, 修复注释错误; <code>@test</code>优化执行逻辑</td><td>2023年6月3日</td>
</tr>
<tr>
<td>2.6.0.0</td><td>config包自动配置，现在仅需要在其中写入键值对即可自动生效</td><td>2023年6月24日</td>
</tr>
<tr>
<td>2.7.0.0</td><td>将配置信息全部写入config包内; 新增eureka注册功能</td><td>2023年6月24日</td>
</tr>
<tr>
<td>2.7.1.0</td><td>新增HOST, PORT等配置项; 初始化脚本新增<code>--app-host</code>, <code>--app-port</code>, <code>--app-debug</code>, <code>--application-root</code>选项</td><td>2023年6月24日</td>
</tr>
<tr>
<td>2.7.2.0</td><td>initializer的<code>--application-root</code>选项修改<code>index.html</code></td><td>2023年6月25日</td>
</tr>
<tr>
<td>2.7.3.0</td><td>fix some bugs</td><td>2023年6月26日</td>
</tr>
<tr>
<td>2.7.4.0</td><td>允许使用同名环境变量对配置项覆盖; fix some bugs</td><td>2023年6月27日</td>
</tr>
<tr>
<td>2.7.5.0</td><td>更换eureka客户端; fix some bugs</td><td>2023年6月29日</td>
</tr>
<tr>
<td>2.7.6.0</td><td>增加多线程、多进程配置项</td><td>2023年7月1日</td>
</tr>
<tr>
<td>2.7.6.1</td><td>fix some bugs</td><td>2023年7月14日</td>
</tr>
<tr>
<td>2.8.0.0</td><td>新增上传文件功能</td><td>2023年7月17日</td>
</tr>
<tr>
<td>2.8.1.0</td><td>传输文件使用临时文件，避免磁盘IO</td><td>2023年7月18日</td>
</tr>
<tr>
<td>2.8.2.0</td><td>增加定时任务配置项; 主页新增"清屏"按钮</td><td>2023年7月20日</td>
</tr>
<tr>
<td>2.8.2.1</td><td>开启定时任务调度持久化; fix some bugs</td><td>2023年7月20日</td>
</tr>
<tr>
<td>2.8.2.2</td><td>fix some bugs</td><td>2023年7月21日</td>
</tr>
<tr>
<td>2.8.2.3</td><td>fix some bugs; 修改数据库配置项</td><td>2023年7月23日</td>
</tr>
<tr>
<td>2.8.2.4</td><td>启用自动重新加载</td><td>2023年7月24日</td>
</tr>
<tr>
<td>2.8.2.5</td><td>修正不规范的命名</td><td>2023年7月26日</td>
</tr>
<tr>
<td>2.8.2.6</td><td>修复<code>pybatis</code>的空指针异常</td><td>2023年7月28日</td>
</tr>
<tr>
<td>2.8.2.7</td><td>fix some bugs; 优化代码执行逻辑</td><td>2023年8月11日</td>
</tr>
<tr>
<td>2.9.0.0</td><td>优化代码执行逻辑; 修改定时任务默认配置项; <code>@mapper</code>新增<code>Generator</code>的定义</td><td>2023年8月28日</td>
</tr>
<tr>
<td>2.9.1.0</td><td>fix some bugs; 更新<code>pybatis</code>的用法</td><td>2023年8月31日</td>
</tr>
<tr>
<td>2.9.1.1</td><td>删除<code>CursorResultUtils.py</code>; 更新说明文档</td><td>2023年9月1日</td>
</tr>
<tr>
<td>2.9.1.2</td><td>fix some bugs</td><td>2023年9月14日</td>
</tr>
<tr>
<td>2.9.2.0</td><td>更新<code>pybatis</code>用法; 更新说明文档</td><td>2023年9月15日</td>
</tr>
<tr>
<td>2.9.3.0</td><td>更新主页, 新增表单提交功能</td><td>2023年9月20日</td>
</tr>
<tr>
<td>2.9.4.0</td><td>新增对mime值选项的悬停提示, 提示内容为后端接收参数方式</td><td>2023年9月21日</td>
</tr>
<tr>
<td>2.9.4.1</td><td>fix some bugs</td><td>2023年9月25日</td>
</tr>
<tr>
<td>2.9.5.0</td><td>修改前端页面样式</td><td>2023年10月12日</td>
</tr>
<tr>
<td>2.9.6.0</td><td>基于反射技术给定时任务加入上下文，修复定时任务中缺失上下文的BUG; 修复前端页面多次请求参数错误的BUG</td><td>2023年10月31日</td>
</tr>
<tr>
<td>3.0.0.0</td><td>彻底分离框架与业务逻辑，构建框架Flask-SSM</td><td>2023年11月9日</td>
</tr>
</table>
