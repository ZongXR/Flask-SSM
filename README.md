<h1>flask-mvc-example</h1>
这是一套基于flask开发的web模板，完全按照MVC分层的思想实现，对于没有web基础但需要做web项目的人可起到教学作用。尤其有助于java转python的web开发，让你按照java的思路写python
<h2>这个怎么用？</h2>
<h3>后台资源</h3>
<h4>package.name.controller包</h4>
<ol>
<li>这个包存放着前后端交互的接口，相当于java的controller包。如需自定义接口，仅需要把py文件放入该包内，并使用<code>@bp.route</code>装饰器注册进去即可。</li>
<li>样例中已经给出了基础接口base_controller.py，如需自定义仿照此样例即可，在此包下的每个py文件构成一个蓝图，并且能够自动注册。</li>
</ol>
<h4>package.name.service包</h4>
<ol>
<li>这个包存放着业务的服务，相当于java的service包。里面的所有模块均需要以模块的形式提供，以此保证单例模式。</li>
<li>如果需要被别的模块引用，直接<code>from package.name.service import **_service</code>即可</li>
</ol>
<h4>package.name.dao包</h4>
<ol>
<li>这个包对应着数据访问层，相当于java的dao包。主要用来写sql，用法同<a href="http://www.pythondoc.com/flask-sqlalchemy/quickstart.html" target="_blank">Flask_SQLAlchemy</a>完全一样</li>
<li>如果需要被别的模块引用，直接<code>from package.name.dao import **_dao</code>即可</li>
</ol>
<h4>package.name.task包</h4>
<ol>
<li>这个包用于存放定时任务，使用时只需要将自定义的定时任务放入包内。</li>
<li>然后在文件中声明ID, FUNC, TRIGGER等用于标志定时任务的变量即可，这些变量必须大写。其中ID表示定时任务的id，必须唯一。FUNC表示定时任务执行的函数名，对应的函数需要在文件内给出。其他标识与<a href="https://segmentfault.com/a/1190000039111644" target="_blank">Flask-APScheduler</a>的用法完全一致，直接填入即可。</li>
</ol>
<h4>package.name.config包</h4>
<ol>
<li>package.name.config，这个包存放着配置信息，包括但不限于数据库配置信息、日志配置信息。样例中已经给出了数据库配置样例database_config.py，日志配置样例logs_config.py</li>
</ol>
<h4>package.name.utils包</h4>
<ol>
<li>这个包用于存放工具模块，样例中已经给出了工具dir_utils.py的样例。</li>
</ol>
<h4>package.name.pojo包</h4>
<ol>
<li>这个包用于存放实体类，通过继承flask_sqlalchemy的Model类，可实现对实体对象的快速query</li>
</ol>
<h4>package.name.vo包</h4>
<ol>
<li>这个包存储了ViewObject，是后端响应给前端的标准json数据格式</li>
</ol>
<h3>前台资源</h3>
<h4>static目录</h4>
该目录用于存放静态资源，存放html, css, js, 图片等资源。样例中已经给出了主页及用到的js文件。
<h4>template目录</h4>
该目录用于存放模板文件，类似于java的jsp。具体用法见<a href="http://www.pythondoc.com/flask/quickstart.html#id7" target="_blank">Flask</a><br />
注意：java的jsp属于动态资源
<h2>原理</h2>
你会发现，该模板中有很多放入包内自动配置的内容。而使这些自动生效的根源就在于每个包下面把的__init__.py，通过该文件实现了免配置自动生效的效果。从而模拟出来类似于java的控制反转和依赖注入的效果。
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
</table>
