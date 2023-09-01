<h1>flask-mvc-example</h1>
这是一套基于flask开发的web模板，完全按照MVC分层的思想实现，对于没有web基础但需要做web项目的人可起到教学作用。尤其有助于java转python的web开发，让你按照java的思路写python
<h2>这个怎么用？</h2>
<h3>初始化</h3>
<p>该项目推荐使用<strong>Python3.7</strong>版本。该框架提供了一键初始化脚本，按照以下步骤即可将自定义包名、数据库连接、日志设置，等内容配置进去</p>
<ol>
<li>拉取本项目后，cd到项目根目录，确保所有文件没被占用</li>
<li>把需要的依赖项添加进<code>./requirements.txt</code>，并执行以下命令安装依赖:<br />
<code>pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r ./requirements.txt</code>
</li>
<li>执行以下命令，即可把项目自定义内容配置进去: <br />
<code>python3 initializer.py \<br />
--package-name your.package.name \<br />
--app-host your_app_host \<br />
--app-port your_app_port \<br />
--app-debug if_the_app_in_debug \<br />
--application-root context_path \<br />
--db-dialect database_dialect \<br />
--db-driver database_driver \<br />
--db-username database_username \<br />
--db-password database_password \<br />
--db-host database_host \<br />
--db-port database_port \<br />
--db-database database_name \<br />
--log-level log_level \<br />
--db-tables table1 table2 table3 ... 
</code><br />
例如: <br />
<code>python3 initializer.py \<br />
--package-name package.name \<br />
--app-host 0.0.0.0 \<br />
--app-port 5000 \<br />
--app-debug False \<br />
--application-root / \<br />
--db-dialect mysql \<br />
--db-driver pymysql \<br />
--db-username root \<br />
--db-password root \<br />
--db-host localhost \<br />
--db-port 3306 \<br />
--db-database dbname \<br />
--log-level DEBUG \<br />
--db-tables table_name1 table_name2
</code><br />
</li>
</ol>
<h3>后台资源</h3>
<h4>package.name.controller包</h4>
<ol>
<li>这个包存放着前后端交互的接口，相当于java的controller包。如需自定义接口，仅需要把py文件放入该包内，并使用<code>@bp.route</code>装饰器注册进去即可。</li>
<li>样例中已经给出了基础接口base_controller.py，如需自定义仿照此样例即可，在此包下的每个py文件构成一个蓝图，并且能够自动注册。</li>
</ol>
使用样例：<code><br />
&commat;bp.route&lpar;&quot;/api&quot;, methods=&lsqb;&quot;GET&quot;, &quot;POST&quot;&rsqb;&rpar;<br />
def foobar&lpar;&rpar; &ndash;&gt; Response&colon;<br />
&nbsp;&nbsp;&nbsp;&nbsp;...<br />
&nbsp;&nbsp;&nbsp;&nbsp;return CommonResult.ok&lpar;data&rpar;
</code>
<h4>package.name.service包</h4>
<ol>
<li>这个包存放着业务逻辑，相当于java的service包。</li>
<li>如果需要被别的模块引用，直接<code>from package.name.service import **_service</code>即可</li>
</ol>
<h4>package.name.dao包</h4>
<ol>
<li>这个包对应着数据访问层，相当于java的dao包。主要用来写sql，用法同<a href="http://www.pythondoc.com/flask-sqlalchemy/quickstart.html" target="_blank">Flask_SQLAlchemy</a>完全一样</li>
<li>如果需要被别的模块引用，直接<code>from package.name.dao import **_dao</code>即可</li>
<li>dao函数的参数是传递给SQL的参数，返回值是SQL语句。再对dao函数加上<code>@mapper(result_type=**)</code>装饰器即可取用特定<code>result_type</code>类型格式的返回值</li>
</ol>
使用样例：<code><br />
&commat;mapper&lpar;result_type=CursorResult&rpar;<br />
def foobar&lpar;param&rpar;&colon;<br />
&nbsp;&nbsp;&nbsp;&nbsp;sql = &quot;&quot;&quot;<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;select &ast;<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;from table_name<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;where id = &colon;param&semi;<br />
&nbsp;&nbsp;&nbsp;&nbsp;&quot;&quot;&quot;<br />
&nbsp;&nbsp;&nbsp;&nbsp;return sql
</code><br />
具体的<code>&commat;mapper</code>中<code>result_type</code>参数见下表
<table>
<tr>
<th>result_type</th><th>返回类型</th>
</tr>
<tr>
<td><code>sqlalchemy.engine.cursor.CursorResult</code></td><td>查询结果游标<code>CursorResult</code>类的对象</td>
</tr>
<tr>
<td><code>sqlalchemy.engine.result.MappingResult</code></td><td>查询结果<code>MappingResult</code>类的对象</td>
</tr>
<tr>
<td><code>pandas.DataFrame</code></td><td><code>DataFrame</code>二维数据表</td>
</tr>
<tr>
<td><code>pandas.Series</code></td><td><code>Series</code>一维数据列</td>
</tr>
<tr>
<td><code>numpy.ndarray</code></td><td><code>ndarray</code>二维数组</td>
</tr>
<tr>
<td><code>typing.List</code>或<code>list</code></td><td>第一条查询结果组成的一维列表</td>
</tr>
<tr>
<td><code>typing.List[typing.Dict]</code>或<code>typing.List[dict]</code></td><td>字典组成的列表，键是列名，值是数据。一个字典是一行数据</td>
</tr>
<tr>
<td><code>typing.List[typing.Tuple]</code>或<code>typing.List[tuple]</code></td><td>元组组成的列表，一个元组是一行数据</td>
</tr>
<tr>
<td><code>typing.List[typing.List]</code>或<code>typing.List[list]</code></td><td>二维列表，一行是一条数据</td>
</tr>
<tr>
<td><code>typing.List[Pojo]</code></td><td>ORM对象组成的一维列表，要求<code>Pojo</code>类继承自<code>db.Model</code></td>
</tr>
<tr>
<td><code>typing.List[T]</code></td><td>某个字段的数值组成的一维列表</td>
</tr>
<tr>
<td><code>typing.Tuple</code>或<code>tuple</code></td><td>第一条查询结果组成的一维元组</td>
</tr>
<tr>
<td><code>typing.Tuple[typing.Dict]</code>或<code>typing.Tuple[dict]</code></td><td>字典组成的元组，键是列名，值是数据。一个字典是一行数据</td>
</tr>
<tr>
<td><code>typing.Tuple[typing.Tuple]</code>或<code>typing.Tuple[tuple]</code></td><td>二维元组，一行是一条数据</td>
</tr>
<tr>
<td><code>typing.Tuple[typing.List]</code>或<code>typing.Tuple[list]</code></td><td>列表组成的元组，一个列表是一条数据</td>
</tr>
<tr>
<td><code>typing.Tuple[Pojo]</code></td><td>ORM对象组成的一维元组，要求<code>Pojo</code>类继承自<code>db.Model</code></td>
</tr>
<tr>
<td><code>typing.Tuple[T]</code></td><td>某个字段的数值组成的一维元组</td>
</tr>
<tr>
<td><code>collections.abc.Generator</code>或<code>typing.Generator</code></td><td>根据SQL语句而定，如果返回一个字段就是该字段的生成器，如果返回多个字段就是一维元组的生成器</td>
</tr>
<tr>
<td><code>typing.Generator[typing.Dict, None, None]</code>或<code>typing.Generator[dict, None, None]</code></td><td>字典组成的生成器，一个字典是一行数据。</td>
</tr>
<tr>
<td><code>typing.Generator[typing.Tuple, None, None]</code>或<code>typing.Generator[tuple, None, None]</code></td><td>一维元组组成的生成器，一个元组是一行数据。</td>
</tr>
<tr>
<td><code>typing.Generator[typing.List, None, None]</code>或<code>typing.Generator[list, None, None]</code></td><td>一维列表组成的生成器，一个列表是一行数据。</td>
</tr>
<tr>
<td><code>typing.Generator[Pojo, None, None]</code></td><td>ORM对象组成的生成器，要求<code>Pojo</code>类继承自<code>db.Model</code></td>
</tr>
<tr>
<td><code>typing.Generator[T, None, None]</code></td><td>单一字段值组成的生成器。</td>
</tr>
<tr>
<td><code>typing.Dict</code>或<code>dict</code></td><td>第一条查询结果组成的字典</td>
</tr>
<tr>
<td><code>typing.Dict[str, typing.List]</code>或<code>typing.Dict[str, list]</code></td><td>一个字典，键是列名，值是字段值组成的列表</td>
</tr>
<tr>
<td><code>typing.Dict[str, typing.Tuple]</code>或<code>typing.Dict[str, tuple]</code></td><td>一个字段，键是列名，值是字段值组成的元组</td>
</tr>
<tr>
<td><code>typing.Dict[str, T]</code></td><td>第一条查询结果组成的字典，键是列名，值是第一条数据的字段值</td>
</tr>
<tr>
<td><code>Pojo</code></td><td>第一条查询结果对应的ORM对象，要求<code>Pojo</code>类继承自<code>db.Model</code></td>
</tr>
<tr>
<td><code>T</code></td><td>泛型<code>T</code>对应的单一数值</td>
</tr>
</table>
<h4>package.name.task包</h4>
<ol>
<li>这个包用于存放定时任务，使用时只需要将自定义的定时任务放入包内。</li>
<li>然后在文件中声明<code>ID</code>, <code>FUNC</code>, <code>TRIGGER</code>等用于标志定时任务的变量即可，这些变量必须大写。其中<code>ID</code>表示定时任务的id，必须唯一。<code>FUNC</code>表示定时任务执行的函数名，对应的函数需要在文件内给出。其他标识与<a href="https://segmentfault.com/a/1190000039111644" target="_blank">Flask-APScheduler</a>的用法完全一致，直接填入即可。</li>
</ol>
<h4>package.name.config包</h4>
<ol>
<li>这个包存放着配置信息，包括但不限于数据库配置信息、日志配置信息。如需配置生效，仅需要在该包内以key-value的形式写入配置项并保持key大写。注意：环境变量的数值会覆盖配置项。</li>
<li><code>database_config.py</code>存储着数据库连接的配置信息，可直接修改。该样例默认使用MySQL数据库</li>
<li><code>logs_config.py</code>存储着日志的配置信息，可直接修改。该样例默认日志存储位置为logs目录，默认日志级别为DEBUG</li>
<li><code>eureka_config.py</code>是用于将微服务注册到eureka的配置信息，默认关闭</li>
<li><code>app_config.py</code>用于该web应用的基础配置，如host, port, 等</li>
<li><code>scheduler_config.py</code>用于定时任务的配置，如定时任务线程池、是否启用API、可信认证等</li>
</ol>
<h4>package.name.utils包</h4>
<ol>
<li>这个包是工具模块，用于存放工具类和函数</li>
</ol>
<h4>package.name.pojo包</h4>
<ol>
<li>这个包用于存放实体类，类似于java的pojo包</li>
<li>通过继承<code>db.Model</code>类，可通过jpa查询规范实现对实体对象的快速检索</li>
<li>里面每一个类必须与数据库表对应。通过<code>__tablename__</code>属性指定表名，其他<code>Column</code>类型属性与字段名一一对应</li>
</ol>
使用样例<code><br />
from sqlalchemy.sql.sqltypes import &ast;<br />
from sqlalchemy.sql.schema import Column<br />
from package.name.dao import db<br />
class TableName&lpar;db.Model&rpar;&colon;<br />
&nbsp;&nbsp;&nbsp;&nbsp;__tablename__ = &quot;table_name&quot;<br />
&nbsp;&nbsp;&nbsp;&nbsp;user_id = Column&lpar;INTEGER&comma;&nbsp;primary_key=True&rpar;<br />
&nbsp;&nbsp;&nbsp;&nbsp;teach_time = Column&lpar;DECIMAL&lpar;precision=2&comma;&nbsp;scale=0&rpar;&rpar;
</code>
<h4>package.name.vo包</h4>
<ol>
<li>这个包存储了ViewObject，是后端响应给前端的标准json数据格式</li>
</ol>
<h4>package.name.decorator包</h4>
<ol>
<li>这个包存储了一系列的装饰器函数，类似于Spring中的AOP面向切面编程</li>
<li>其中<code>pybatis.py</code>模拟了MyBatis: <br />
如需对某个函数开启事务，直接加上<code>&commat;transactional&lpar;rollback_for=&ast;&ast;&rpar;</code>即可。<br />
如需执行某条SQL，直接加上<code>&commat;mapper&lpar;result_type=&ast;&ast;&rpar;</code>即可。
</li>
<li>其中<code>unittest.py</code>实现了单元测试的功能。如需对某个函数进行单元测试，直接加上<code>&commat;test</code>，然后在函数所在的py文件里面加上<code>if __name__ == &quot;__main__&quot;&colon;</code>后，直接运行改py文件即可</li>
</ol>
使用样例<code><br />
from package.name.decorator.unittest import test<br />
&commat;test<br />
def foobar&lpar;param: int&rpar;:<br />
&nbsp;&nbsp;&nbsp;&nbsp;...<br />
&nbsp;&nbsp;&nbsp;&nbsp;return ...<br />
if name == &quot;__main__&quot;&colon;<br />
&nbsp;&nbsp;&nbsp;&nbsp;print&lpar;foobar&lpar;3&rpar;&rpar;
</code>
<h3>前台资源</h3>
<h4>static目录</h4>
<ol>
<li>该目录用于存放静态资源，存放html, css, js, 图片等资源。</li>
<li>该样例的默认主页为<code>index.html</code>，实现了类似java的swagger功能。可以在浏览器直接向指定接口发送请求，并且自定义请求路径、请求方法等信息</li>
</ol>
<h4>templates目录</h4>
该目录用于存放模板文件，类似于java的jsp。具体用法见<a href="http://www.pythondoc.com/flask/quickstart.html#id7" target="_blank">Flask</a><br />
注意：java的jsp属于动态资源
<h2>原理</h2>
<ol>
<li>你会发现，该框架中有很多放入包内自动配置的内容，其核心在于每个包下面的<code>__init__.py</code>。</li>
<li>通过使用python的反射机制，模拟了Spring的IOC控制反转的效果，实现了接口的自动注册、定时任务的自动注册、初始化指定数据库的表名字段名，等功能</li>
<li>通过使用python的装饰者模式，模拟了Spring的AOP面向切面编程，实现了事务管理器、单元测试、ORM对象关系映射，等功能</li>
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
</table>
