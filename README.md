<h1><a href="https://github.com/GoogleLLP/Flask-SSM" target="_blank">Flask-SSM</a></h1>
一款模仿SpringFramework的Python的web后端框架，基于Flask二次封装。通过Python反射模拟了Java的IOC控制反转，通过Python装饰者模式模拟了Java的AOP面向切面编程。具有接口自动发现、定时任务自动注册、事务管理器、单元测试，等功能。简化web后端开发流程，聚焦业务逻辑，让你按照Spring的习惯写Python
<h2>使用方法</h2>
首先使用以下命令安装该框架<br />
<code>pip&nbsp;install&nbsp;Flask-SSM</code><br />
使用教程请参考<a href="https://github.com/GoogleLLP/Flask-SSM" target="_blank">此地址</a>中的<code>test.demo</code>包，这是一个具有典型MVC结构的最小web应用。
<h3>创建基础环境</h3>
<ol>
<li>
如<code>test.demo</code>包所示，在<code>test.demo.__init__.py</code>中定义<code>SpringApplication</code>类的对象。<br />
<code>sp&nbsp;=&nbsp;SpringApplication&lpar;&rpar;</code>
</li>
<li>
如<code>app.py</code>所示，在<code>app.py</code>中导入该对象，然后对其进行初始化。<br />
<code>from&nbsp;test.demo&nbsp;import&nbsp;sp</code><br />
<code>app&nbsp;=&nbsp;Flask&lpar;sp.base_package.__package__&rpar;</code><br />
<code>sp.init_app&lpar;app&rpar;</code><br />
<code>app.run&lpar;&rpar;</code>
</li>
</ol>
<h3>应用配置项</h3>
<ol>
<li>
如<code>test.demo.config</code>包所示，在<code>test.demo.config.__init__.py</code>中导入<code>Configuration</code>类，该包内的配置项能自动识别。<br/>
<code>from&nbsp;flask_ssm.springframework.context.annotation&nbsp;import&nbsp;Configuration</code>
</li>
<li>
建议将同一类别的配置写在同一模块内。如<code>test.demo.config.app_config</code>所示：<br />
<code>APP_HOST&nbsp;=&nbsp;&quot;0.0.0.0&quot;</code>&nbsp;&#35;&nbsp;定义了应用的域<br />
<code>APP_PORT&nbsp;=&nbsp;5000</code>&nbsp;&#35;&nbsp;定义了应用的端口<br />
<code>APPLICATION_ROOT&nbsp;=&nbsp;&quot;/&quot;</code>&nbsp;&#35;&nbsp;定义了应用的根路径<br />
<code>USE_RELOADER&nbsp;=&nbsp;False</code>&nbsp;&#35;&nbsp;是否开启热更新<br />
<code>DEBUG&nbsp;=&nbsp;False</code>&nbsp;&#35;&nbsp;是否处于debug模式<br />
<code>APP_THREAD&nbsp;=&nbsp;False</code>&nbsp;&#35;&nbsp;是否开启多线程<br />
<code>APP_PROCESS&nbsp;=&nbsp;1</code>&nbsp;&#35;&nbsp;进程个数<br />
</li>
</ol>
需要注意的是：
<ul>
<li>其中，配置项的key必须保持大写，才能被识别。</li>
<li>如果环境变量中有与key同名变量，变量值自动覆盖配置项。</li>
</ul>
<h3>web接口层</h3>
<ol>
<li>
如<code>test.demo.controller</code>包所示，在<code>test.demo.controller.__init__.py</code>中导入<code>Controller</code>类，该包内的全部<code>Blueprint</code>类能被自动注册，从而实现接口的自动发现。<br />
<code>from&nbsp;flask_ssm.springframework.stereotype&nbsp;import&nbsp;Controller</code>
</li>
<li>
如<code>test.demo.controller.base_controller</code>所示，对需要注册的接口直接加上<code>&commat;RequestMapping&lpar;value=**&comma;&nbsp;method=**&rpar;</code>或<code>&commat;GetMapping&lpar;value=**&rpar;</code>或<code>&commat;PostMapping&lpar;value=**&rpar;</code>
</li>
<li>
如<code>test.demo.controller.customize_controller</code>所示，如果响应体是json格式，使用<code>&commat;ResponseBody</code>把函数返回值映射为json格式写入响应体中。注意，由于Python装饰器有前后执行顺序区别，因此<code>&commat;ResponseBody</code>要加在<code>&commat;RequestMapping</code>后面<br />
<code>&commat;RequestMapping&lpar;&quot;/hello_world&quot;&comma;&nbsp;[RequestMethod.POST]&rpar;</code><br />
<code>&commat;ResponseBody</code><br />
<code>def&nbsp;hello_world&lpar;param&rpar;:</code><br />
<code>&nbsp;&nbsp;&nbsp;&nbsp;result&nbsp;=&nbsp;base_service.run&lpar;param&rpar;</code><br />
<code>&nbsp;&nbsp;&nbsp;&nbsp;return&nbsp;CommonResult.ok&lpar;data=result&rpar;</code><br />
</li>
<li>
如<code>test.demo.controller.customize_controller</code>所示，对该模块内的全局异常处理函数加上<code>&commat;ExceptionHandler&lpar;value=**&rpar;</code><br />
<code>&commat;ExceptionHandler&lpar;Exception&rpar;</code><br />
<code>def&nbsp;custom_error_handler&lpar;e&rpar;:</code><br />
<code>&nbsp;&nbsp;&nbsp;&nbsp;return&nbsp;str&lpar;e&rpar;</code>
</li>
</ol>
<h3>业务逻辑层</h3>
<ol>
<li>
如<code>test.demo.service</code>包所示，在<code>test.demo.service.__init__.py</code>中导入<code>Service</code>类。<br />
<code>from&nbsp;flask_ssm.springframework.stereotype&nbsp;import&nbsp;Service</code>
</li>
<li>
对于涉及数据修改的函数，使用<code>&commat;Transactional&lpar;rollback_for=**&rpar;</code>修饰，并使用<code>rollback_for</code>指定回滚的异常类型，从而开启事务。
</li>
<li>
如<code>test.demo.service.base_service</code>所示，对于需要进行单元测试的函数，使用<code>&commat;Test</code>修饰该函数，并作为入口运行。<br />
<code>@Test</code><br />
<code>def&nbsp;run&lpar;param&rpar;:</code><br />
<code>&nbsp;&nbsp;&nbsp;&nbsp;result&nbsp;=&nbsp;tablename_dao.query_one&lpar;param&rpar;</code><br />
<code>&nbsp;&nbsp;&nbsp;&nbsp;return&nbsp;str&lpar;result&rpar;</code><br />
<code>if&nbsp;__name__&nbsp;==&nbsp;&quot;__main__&quot;:</code><br />
<code>&nbsp;&nbsp;&nbsp;&nbsp;print&lpar;run&lpar;&quot;Hello&nbsp;World&quot;&rpar;&rpar;</code>
</li>
</ol>
<h3>数据交互层</h3>
<ol>
<li>
如<code>test.demo.dao</code>包所示，在<code>test.demo.dao.__init__.py</code>中导入<code>Repository</code>类，可以使用注解式数据查询。<br />
<code>from&nbsp;flask_ssm.springframework.stereotype&nbsp;import&nbsp;Repository</code>
</li>
<li>
如<code>test.demo.dao.tablename_dao</code>所示，对于查询函数，使用<code>&commat;Mapper&lpar;result_type=**&rpar;</code>修饰，并使用<code>result_type</code>指定返回类型。函数的参数为传入SQL语句的参数，返回值为SQL语句，即可实现返回对象的自动封装。<br />
<code>&commat;Mapper&lpar;result_type=str&rpar;</code><br />
<code>def&nbsp;query_one&lpar;param&rpar;:</code><br />
<code>&nbsp;&nbsp;&nbsp;&nbsp;sql&nbsp;=&nbsp;&quot;&quot;&quot;</code><br />
<code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;select&nbsp;:param&semi;</code><br />
<code>&nbsp;&nbsp;&nbsp;&nbsp;&quot;&quot;&quot;</code><br />
<code>&nbsp;&nbsp;&nbsp;&nbsp;return&nbsp;sql</code>
</li>
</ol>
<h3>定时任务</h3>
<ol>
<li>
如<code>test.demo.task</code>包所示，在<code>test.demo.task.__init__.py</code>中导入<code>Scheduled</code>类，可以实现该包内的定时任务自动注册。<br />
<code>from&nbsp;flask_ssm.springframework.scheduling.annotation&nbsp;import&nbsp;Scheduled</code>
</li>
<li>
如<code>test.demo.task.my_task</code>所示，在模块中声明ID, FUNC, TRIGGER等用于标志定时任务的变量即可，这些变量必须大写。其中ID表示定时任务的id，必须唯一。FUNC表示定时任务执行的函数名，对应的函数需要在文件内给出。其他标识与<a href="https://segmentfault.com/a/1190000039111644" target="_blank">Flask-APScheduler</a>的用法完全一致，直接填入即可。<br />
<code>ID&nbsp;=&nbsp;&quot;scheduled_task&quot;</code>&nbsp;&#35;&nbsp;ID必须唯一<br />
<code>FUNC&nbsp;=&nbsp;&quot;my_func&quot;</code>&nbsp;&#35;&nbsp;生效的函数名<br />
<code>TRIGGER&nbsp;=&nbsp;&quot;interval&quot;</code>&nbsp;&#35;&nbsp;触发条件，interval表示定时间间隔触发<br />
<code>SECONDS&nbsp;=&nbsp;5</code>&nbsp;&#35;&nbsp;触发时间间隔设定5秒<br />
<code>REPLACE_EXISTING&nbsp;=&nbsp;True</code>&nbsp;&#35;&nbsp;重启替换持久化<br />
<code>def&nbsp;my_func():</code>&nbsp;&#35;&nbsp;定时执行的函数<br />
<code>&nbsp;&nbsp;&nbsp;&nbsp;current_app.logger.info(&quot;触发定时任务&quot;&nbsp;+&nbsp;ID)</code>
</li>
</ol>
<h3>ORM对象</h3>
<ol>
<li>
如<code>test.demo.pojo.pojo_demo</code>所示，每一个ORM映射对象需要使用类进行定义，并使用<code>&commat;TableName&lpar;value=**&rpar;</code>修饰，使用<code>value</code>指定表名。类的属性需要与表的字段对应，并使用<code>Column</code>类封装。<br />
<code>@TableName&lpar;&quot;table_name&quot;&rpar;</code><br />
<code>class&nbsp;Pojo:</code><br />
<code>&nbsp;&nbsp;&nbsp;&nbsp;user_id&nbsp;=&nbsp;Column&lpar;INTEGER&comma;&nbsp;primary_key=True&rpar;</code><br />
<code>&nbsp;&nbsp;&nbsp;&nbsp;teach_time&nbsp;=&nbsp;Column&lpar;DECIMAL&lpar;precision=2&comma;&nbsp;scale=0&rpar;&rpar;</code>
</li>
</ol>
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
<tr>
<td>3.1.0.0</td><td>新增装饰器<code>&commat;TableName</code>&semi;&nbsp;装饰器<code>&commat;Test</code>新增统计运行时间的功能，并输出到日志&semi;&nbsp;修复若干BUG</td><td>2023年11月10日</td>
</tr>
<tr>
<td>3.2.0.0</td><td>新增安装脚本&semi;&nbsp;框架上传至pypi官方源</td><td>2023年11月11日</td>
</tr>
<tr>
<td>3.3.0.0</td><td>新增<code>&commat;RequestMapping</code>&comma;&nbsp;<code>&commat;ExceptionHandler</code>装饰器&semi;&nbsp;修改包结构</td><td>2023年11月12日</td>
</tr>
<tr>
<td>3.4.0.0</td><td>新增<code>&commat;GetMapping</code>&comma;&nbsp;<code>&commat;PostMapping</code>装饰器</td><td>2023年11月13日</td>
</tr>
<tr>
<td>3.5.0.0</td><td><code>&commat;RequestMapping</code>装饰器实现参数注入功能，现在可以直接把请求参数写入接口的函数形参。</td><td>2023年11月14日</td>
</tr>
<tr>
<td>3.5.1.0</td><td>优化执行逻辑，提升执行效率</td><td>2023年11月14日</td>
</tr>
<tr>
<td>3.6.0.0</td><td>新增<code>&commat;ResponseBody</code>装饰器&comma;&nbsp;修复若干BUG</td><td>2023年11月19日</td>
</tr>
</table>
