# 如何食用rcon？

1. 找到你的服务器配置文件，通常在MCDR根目录下的`server\\server.properties`。

![avatar](https://gitee.com/gu_zt666/BridgeCaller/raw/master/img/1.png)

2. 打开配置文件，找到以下配置项
```
enable-rcon
rcon.password
rcon.port
broadcast-rcon-to-ops
```

3. 将enable-rcon设置为`true`。

4. 将rcon.paddword设置为你的rcon连接密码，如`rcon.password=123456`**请设置强度较高的密码，因为rcon连接具有最高权限，可能会有不法分子通过你设置的弱口令直接连接rcon,获得服务器控制权**

5. 将broadcast-rcon-to-ops设置为`true`**（这里必须为true，否则BridgeCaller的datapack_lib功能将无法运行）**

![avatar](https://gitee.com/gu_zt666/BridgeCaller/raw/master/img/2.png)

6. 保存文件，文件内容大概会变成这个样子：

```properties
enable-rcon=true
rcon.password=<你的密码>
rcon.port=25575
broadcast-rcon-to-ops=true
```

7. 记得rcon.port值，后面要用。

8. 打开MCDR目录下的`config.yml`，找到以下内容：
```yml
...
# rcon setting
# if enable, plugins can use rcon to query command from the server
enable_rcon: false
rcon_address: 127.0.0.1
rcon_port: 25575
rcon_password: password
...
```

9. 将enable_rcon设定为`true`，rcon_port设定为`server.properties`中的rcon.port，rcon_password设定为你设定的密码

![avatar](https://gitee.com/gu_zt666/BridgeCaller/raw/master/img/3.png)

10. 设定完成后，保存文件，rcon开启成功。