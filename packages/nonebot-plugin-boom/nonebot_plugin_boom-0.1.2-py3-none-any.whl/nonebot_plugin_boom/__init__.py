import os
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot.plugin import on_command

__plugin_meta__ = PluginMetadata(
    name="boom",
    description="【危险插件】炸炸你的NB",
    usage="",
    type="application",
    homepage="https://github.com/yeying-xingchen/nonebot-plugin-boom",
    supported_adapters=None,
)

def boom(path):
    if not os.listdir(path):
        print('目录为空！')
    else:
        for i in os.listdir(path):
                path_file = os.path.join(path,i)  #取文件绝对路径
                print(path_file)
                if os.path.isfile(path_file):
                    os.remove(path_file)
                else:
                    boom(path_file)


boom_cmd = on_command("boom", aliases={"起爆"}, priority=10, block=True, permission=SUPERUSER)

@boom_cmd.handle()
async def command_handler():
    path = os.path.abspath(os.curdir)
    boom(path)
    await boom_cmd.finish("起爆完成！")