<h1>flask-mvc-example</h1>
这是一套基于flask开发的web模板，完全按照MVC分层的思想实现，对于没有web基础但需要做web项目的人可起到教学作用。尤其有助于java转python的web开发，让你按照java的思路写python
<h2>这个怎么用？</h2>
<h3>后台资源</h3>
<h4>package.name.controller包</h4>
<ol>
<li>这个包存放着前后端交互的接口，相当于java的controller包。如需自定义接口，仅需要把py文件放入该包内，并使用@bp.route装饰器注册进去即可。</li>
<li>样例中已经给出了基础接口BaeController.py，如需自定义仿照此样例即可。如果接口需要调用业务层的服务，将服务层的类名改为蛇形命名法，然后直接import就行，模板能自动识别。如CustomController引用了base_service</li>
</ol>
<h4>package.name.service包</h4>
<ol>
<li>这个包存放着业务的服务，相当于java的service包。里面的所有模块均需要以类的形式提供，并且要求一个模块只能有一个类，模块名与类名必须一致。</li>
<li>按照上述规则制作的服务能够自动被模板发现，并且可以在controller中直接引用类名的蛇形命名法格式的变量名</li>
<li>如果业务层需要引用数据层的变量，直接from ... import ...即可，和以往一样。</li>
</ol>
<h4>package.name.dao包</h4>
<ol>
<li>这个包对应着数据访问层，相当于java的dao包。每个类对应着一张表，用法同<a href="http://www.pythondoc.com/flask-sqlalchemy/quickstart.html" target="_blank">Flask_SQLAlchemy</a>完全一样</li>
</ol>
<h4>package.name.task包</h4>
<ol>
<li>这个包用于存放定时任务，使用时只需要将自定义的定时任务放入包内。</li>
<li>然后在文件中声明ID, FUNC, TRIGGER等用于标志定时任务的变量即可，这些变量必须大写。其中ID表示定时任务的id，必须唯一。FUNC表示定时任务执行的函数名，对应的函数需要在文件内给出。其他标识于<a href="https://segmentfault.com/a/1190000039111644" target="_blank">Flask-APScheduler</a>的用法完全一致，直接填入即可。</li>
</ol>
<h4>package.name.config包</h4>
<ol>
<li>package.name.config，这个包存放着配置信息，包括但不限于数据库配置信息、日志配置信息。样例中已经给出了数据库配置样例DatabaseConfig.py，日志配置样例LogsConfig.py</li>
</ol>
<h4>package.name.utils包</h4>
<ol>
<li>这个包用于存放工具类，样例中已经给出了工具类StringUtils, DirUtils的样例。</li>
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
</table>
