<h1><a href="https://github.com/ZongXR/Flask-SSM" target="_blank">Flask-SSM</a></h1>
一款模仿SpringFramework的Python的web后端框架，基于Flask二次封装。通过Python反射模拟了Java的IOC控制反转，通过Python装饰者模式模拟了Java的AOP面向切面编程。具有接口自动发现、定时任务自动注册、事务管理器、单元测试，等功能。简化web后端开发流程，聚焦业务逻辑，让你按照Spring的习惯写Python
<h2>使用方法</h2>
首先使用以下命令安装该框架<br />
<code>pip&nbsp;install&nbsp;Flask-SSM</code><br />
使用教程请参考<a href="https://github.com/ZongXR/Flask-SSM" target="_blank">此地址</a>中的<code><a href="./test/demo" target="_blank">test.demo</a></code>包，这是一个具有典型MVC结构的最小web应用。
<h3>创建基础环境</h3>
<ol>
<li>
如<code><a href="./test/demo" target="_blank">test.demo</a></code>包所示，在<code><a href="./test/demo/__init__.py" target="_blank">test.demo.__init__.py</a></code>中定义<code>SpringApplication</code>类的对象。
<pre>sp = SpringApplication()</pre>
</li>
<li>
如<code><a href="./app.py" target="_blank">app.py</a></code>所示，在<code><a href="./app.py" target="_blank">app.py</a></code>中导入该对象，然后对其进行初始化。
<pre>
from test.demo import sp
app = Flask(sp.base_package.__package__)
sp.init_app(app)
app.run()
</pre>
</li>
</ol>
<h3>应用配置项</h3>
<ol>
<li>
如<code><a href="./test/demo/config" target="_blank">test.demo.config</a></code>包所示，在<code><a href="./test/demo/config/__init__.py" target="_blank">test.demo.config.__init__.py</a></code>中导入<code>Configuration</code>类，该包内的配置项能自动识别。
<pre>from flask_ssm.springframework.context.annotation import Configuration</pre>
</li>
<li>
建议将同一类别的配置写在同一模块内。如<code><a href="./test/demo/config/app_config.py" target="_blank">test.demo.config.app_config</a></code>所示：
<pre>
APP_HOST = '0.0.0.0'           # 应用的host，一般保持0.0.0.0
APP_PORT = 5000                # 应用占用的端口
APP_STATIC = "static"          # 静态资源目录
APP_TEMPLATES = "templates"    # 渲染模板目录
APP_RELOADER = False           # 是否开启热更新
APPLICATION_ROOT = '/'         # 应用挂载servlet-path路径
DEBUG = False                  # 是否处于DEBUG模式
APP_THREAD = False             # 是否开启多线程
APP_PROCESS = 1                # 进程个数
</pre>
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
如<code><a href="./test/demo/controller" target="_blank">test.demo.controller</a></code>包所示，在<code><a href="./test/demo/controller/__init__.py" target="_blank">test.demo.controller.__init__.py</a></code>中导入<code>Controller</code>类，标记该包内所有模块的函数为web接口。
<pre>from flask_ssm.springframework.stereotype import Controller</pre>
</li>
<li>
如<code><a href="./test/demo/controller/base_controller.py" target="_blank">test.demo.controller.base_controller</a></code>所示，对需要注册的接口直接加上<code>&commat;RequestMapping&lpar;value=**&comma;&nbsp;method=**&rpar;</code>或<code>&commat;GetMapping&lpar;value=**&rpar;</code>或<code>&commat;PostMapping&lpar;value=**&rpar;</code>。
</li>
<li>
如<code><a href="./test/demo/controller/customize_controller.py" target="_blank">test.demo.controller.customize_controller</a></code>所示，如果需要json格式的响应体，在<code>&commat;RequestMapping</code>后面加上<code>&commat;ResponseBody</code>，把函数返回值映射为json格式写入响应体中。
<pre>
@RequestMapping("/hello_world", [RequestMethod.POST])
@ResponseBody
def hello_world(param):
    result = base_service.run(param)
    return CommonResult.ok(data=result)
</pre>
</li>
<li>
如果某个模块的接口均为restful风格，那么只需要在该模块引入<code>RestController</code>，而忽略<code>&commat;ResponseBody</code>装饰器
<pre>from flask_ssm.springframework.web.bind.annotation import RestController</pre>
</li>
<li>
如<code><a href="./test/demo/controller/customize_controller.py" target="_blank">test.demo.controller.customize_controller</a></code>所示，对该模块内的全局异常处理函数加上<code>&commat;ExceptionHandler&lpar;value=**&rpar;</code>
<pre>
@ExceptionHandler(Exception)
def custom_error_handler(e):
    return str(e)
</pre>
</li>
</ol>
<h3>业务逻辑层</h3>
<ol>
<li>
如<code><a href="./test/demo/service" target="_blank">test.demo.service</a></code>包所示，在<code><a href="./test/demo/service/__init__.py" target="_blank">test.demo.service.__init__.py</a></code>中导入<code>Service</code>类。
<pre>from flask_ssm.springframework.stereotype import Service</pre>
</li>
<li>
对于涉及数据修改的函数，使用<code>&commat;Transactional&lpar;rollback_for=**&rpar;</code>修饰，并使用<code>rollback_for</code>指定回滚的异常类型，从而开启事务。
</li>
<li>
如<code><a href="./test/demo/service/base_service.py" target="_blank">test.demo.service.base_service</a></code>所示，对于需要进行单元测试的函数，使用<code>&commat;Test</code>修饰该函数，并作为入口运行。
<pre>
@Test
def run(param):
    result = tablename_dao.query_one(param)
    return str(result)
if __name__ == "__main__":
    print(run("Hello World"))
</pre>
</li>
</ol>
<h3>数据交互层</h3>
<ol>
<li>
如<code><a href="./test/demo/dao" target="_blank">test.demo.dao</a></code>包所示，在<code><a href="./test/demo/dao/__init__.py" target="_blank">test.demo.dao.__init__.py</a></code>中导入<code>Repository</code>类，可以使用注解式数据查询。
<pre>from flask_ssm.springframework.stereotype import Repository</pre>
</li>
<li>
如<code><a href="./test/demo/dao/tablename_dao.py" target="_blank">test.demo.dao.tablename_dao</a></code>所示，对于查询函数，使用<code>&commat;Mapper&lpar;result_type=**&rpar;</code>修饰，并使用<code>result_type</code>指定返回类型。函数的参数为传入SQL语句的参数，返回值为SQL语句，SQL语句的参数部分同MyBatis的用法，即可实现返回对象的自动封装。
<pre>
@Mapper(result_type=str)
def query_one(param):
    sql = """
        select #{param};
    """
    return sql
</pre>
</li>
</ol>
<h3>定时任务</h3>
<ol>
<li>
如<code><a href="./test/demo/task" target="_blank">test.demo.task</a></code>包所示，在<code><a href="./test/demo/task/__init__.py" target="_blank">test.demo.task.__init__.py</a></code>中导入<code>Scheduled</code>类，可以实现该包内的定时任务自动注册。
<pre>from flask_ssm.springframework.scheduling.annotation import Scheduled</pre>
</li>
<li>
如<code><a href="./test/demo/task/my_task.py" target="_blank">test.demo.task.my_task</a></code>所示，在模块中声明<code>FUNC</code>, <code>TRIGGER</code>等用于标志定时任务的变量即可，这些变量必须大写。<code>FUNC</code>表示定时任务执行的函数名，对应的函数需要在文件内给出，置空禁用定时任务。其他标识与<a href="https://segmentfault.com/a/1190000039111644" target="_blank">Flask-APScheduler</a>的用法完全一致，直接填入即可。
<pre>
FUNC = "my_func"           # 生效的函数名，如需禁用可设为None
TRIGGER = "interval"       # 触发条件，interval表示定时间间隔触发
SECONDS = 5                # 触发时间间隔设定5秒
REPLACE_EXISTING = True    # 重启替换持久化
def my_func():             # 定时执行的函数
    current_app.logger.info("触发定时任务")
</pre>
</li>
</ol>
<h3>ORM对象</h3>
<ol>
<li>
如<code><a href="./test/demo/pojo/pojo_demo.py" target="_blank">test.demo.pojo.pojo_demo</a></code>所示，每一个ORM映射对象需要使用类进行定义，并使用<code>&commat;TableName&lpar;value=**&rpar;</code>修饰，使用<code>value</code>指定表名。类的属性需要与表的字段对应，并使用<code>Column</code>类封装。
<pre>
@TableName("table_name")
class Pojo:
    user_id = Column(INTEGER, primary_key=True)
    teach_time = Column(DECIMAL(precision=2, scale=0))
</pre>
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
<tr>
<td>3.7.0.0</td><td>新增<code>RestController</code>类</td><td>2023年11月27日</td>
</tr>
<tr>
<td>3.7.1.0</td><td>新增<code>&commat;PutMapping</code>&comma;&nbsp;<code>&commat;DeleteMapping</code>&comma;&nbsp;<code>&commat;PatchMapping</code>装饰器</td><td>2023年11月30日</td>
</tr>
<tr>
<td>3.7.1.1</td><td>fix some bugs</td><td>2023年12月11日</td>
</tr>
<tr>
<td>3.7.1.2</td><td>去除不必要的依赖</td><td>2023年12月13日</td>
</tr>
<tr>
<td>3.7.2.0</td><td>定时任务默认使用文件名作为<code>ID</code>;&nbsp;<code>FUNC</code>为空时禁用定时任务;&nbsp;优化执行逻辑，提升运行效率</td><td>2023年12月21日</td>
</tr>
<tr>
<td>3.7.2.1</td><td>fix some bugs</td><td>2023年12月25日</td>
</tr>
<tr>
<td>3.7.2.2</td><td>SQL语句兼容MyBatis的#&lcub;param&rcub;形式;&nbsp;fix some bugs</td><td>2023年12月26日</td>
</tr>
<tr>
<td>3.7.2.3</td><td>SQL语句兼容MyBatis的$&lcub;param&rcub;形式</td><td>2023年12月26日</td>
</tr>
<tr>
<td>3.7.2.4</td><td>fix some bugs</td><td>2023年12月29日</td>
</tr>
<tr>
<td>3.7.2.5</td><td>change github username</td><td>2023年12月29日</td>
</tr>
<tr>
<td>3.7.2.6</td><td>change github username</td><td>2023年12月29日</td>
</tr>
<tr>
<td>3.7.3.0</td><td>兼容Python&nbsp;3.10</td><td>2024年7月12日</td>
</tr>
<tr>
<td>3.7.3.1</td><td>fix some bugs</td><td>2024年7月12日</td>
</tr>
<tr>
<td>3.7.3.2</td><td>fix some bugs</td><td>2024年7月13日</td>
</tr>
<tr>
<td>3.7.3.3</td><td>fix some bugs</td><td>2024年7月25日</td>
</tr>
<tr>
<td>3.7.3.4</td><td>fix some bugs</td><td>2024年7月27日</td>
</tr>
<tr>
<td>3.8.0.0</td><td>集成Flask-Pydantic，现在可以使用type&nbsp;hints对API及SQL的参数类型进行校验</td><td>2024年7月31日</td>
</tr>
<tr>
<td>3.8.0.1</td><td>修复使用外部web服务器运行带来的BUG</td><td>2024年8月2日</td>
</tr>
<tr>
<td>3.8.0.2</td><td>修复数据库null在numpy和pandas中识别为None的BUG; 修复把任意对象封装为json的方法的BUG</td><td>2025年4月1日</td>
</tr>
<tr>
<td>3.8.0.3</td><td>修复连接多个数据源引发的BUG</td><td>2025年4月6日</td>
</tr>
<tr>
<td>3.8.1.0</td><td>增加日志和启动参数的默认配置项; 适配Flask扩展编写规范; 前端请求使用fetch API替换ajax</td><td>2025年4月9日</td>
</tr>
<tr>
<td>3.9.0.0</td><td>fix some bugs; 新增templates和static目录的配置项; 取消对Flask-Pydantic的依赖</td><td>2025年4月14日</td>
</tr>
<tr>
<td>3.9.1.0</td><td>新增<code>@Validated</code>装饰器，统一管理参数类型校验; fix some bugs</td><td>2025年4月17日</td>
</tr>
<tr>
<td>3.9.1.1</td><td>fix some bugs</td><td>2025年4月17日</td>
</tr>
<tr>
<td>3.9.1.2</td><td>fix some bugs</td><td>2025年4月17日</td>
</tr>
<tr>
<td>3.9.2.0</td><td>fix some bugs</td><td>2025年6月16日</td>
</tr>
<tr>
<td>3.9.2.1</td><td>美化前端页面; fix some bugs</td><td>2025年6月18日</td>
</tr>
<tr>
<td>3.9.2.2</td><td>fix some bugs</td><td>2025年6月19日</td>
</tr>
<tr>
<td>3.9.2.3</td><td>fix some bugs</td><td>2025年6月24日</td>
</tr>
<tr>
<td>3.9.2.4</td><td>fix some bugs</td><td>2025年6月26日</td>
</tr>
<tr>
<td>3.9.2.5</td><td>fix some bugs</td><td>2025年6月27日</td>
</tr>
<tr>
<td>3.10.0.0</td><td>完善<code>@Transactional</code>装饰器的使用, 新增<code>propagation</code>参数; 修改<code>@Validated</code>装饰器校验类型失败时的抛出异常类型; 完善枚举类型</td><td>2025年7月4日</td>
</tr>
<tr>
<td>3.10.1.0</td><td>升级SQLalchemy, 解决若干BUG; <code>@Mapper</code>装饰器兼容polars的Series和DataFrame; 使用环境变量设置项时进行警告</td><td>2025年7月10日</td>
</tr>
<tr>
<td>3.10.1.1</td><td>修改Flask-SQLalchemy的配置项</td><td>2025年7月14日</td>
</tr>
<tr>
<td>3.10.2.0</td><td>优化执行逻辑; 修复数据库连接无法关闭的BUG; 修复前端页面的显示BUG</td><td>2025年8月2日</td>
</tr>
<tr>
<td>3.10.3.0</td><td>执行<code>INSERT</code>、<code>UPDATE</code>、<code>DELETE</code>语句, 如果把<code>result_type</code>设置为<code>int</code>可以返回受影响行数</td><td>2025年8月3日</td>
</tr>
<tr>
<td>3.10.3.1</td><td>Flask-SQLalchemy升级版本至3.1.1</td><td>2025年8月4日</td>
</tr>
<tr>
<td>3.10.4.0</td><td>优化执行逻辑</td><td>2025年8月5日</td>
</tr>
<tr>
<td>3.10.5.0</td><td>修复数据库增删改无法返回行数的BUG</td><td>2025年8月18日</td>
</tr>
<tr>
<td>3.10.6.0</td><td>fix some bugs</td><td>2025年8月18日</td>
</tr>
<tr>
<td>3.10.7.0</td><td>修复事务管理器的BUG</td><td>2025年8月21日</td>
</tr>
</table>
