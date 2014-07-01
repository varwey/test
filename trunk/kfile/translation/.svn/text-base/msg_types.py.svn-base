# -*- coding: utf-8 -*-
import jinja2

msg_dict = {}


class MsgType(object):
    template = u"未知动作"
    _template = None

    @classmethod
    def get_code(cls):
        return cls.__name__

    @classmethod
    def get_class_by_code(cls, code):
        return msg_dict[code]

    @classmethod
    def get_display(cls, params):
        if not cls._template:
            cls._template = jinja2.Template(cls.template)
        return cls._template.render(**params)


class FILE_CREATE(MsgType):
    template = u'{{ user }} 创建了文件 {{ file_path }}'


class FILE_UPDATE(MsgType):
    template = u'{{ user }} 更新了文件 {{ file_path }}'


class FILE_DELETE(MsgType):
    template = u'{{ user }} 删除了文件 {{ file_path }}'


class FILE_REPLACE(MsgType):
    template = u'{{ user }} 替换了文件 {{ file_path }}'


class FILE_UPDATE_CONTENT(MsgType):
    template = u'{{ user }} 编辑了文件 {{ file_path }}'


class FILE_CHANGE_SOURCE(MsgType):
    template = u'{{ user }} 更改文件 {{ old_source }} 名称 为 {{ new_source}}'


class FILE_DOWNLOAD(MsgType):
    template = u'{{ user }} 下载了文件 {{ file_path }}'


class FILE_BATCH_DOWNLOAD(MsgType):
    template = u'{{ user }} 批量下载了 {{ count }} 个文件'


class FILE_MACHINE_TRANSLATE(MsgType):
    template = u'{{ user }} 提交了 {{ num }}个文件，共 {{ count }} 个词条去机器翻译成 {{ lang }} 语言版本'


class FILE_HUMAN_TRANSLATE(MsgType):
    template = u'{{ user }} 提交了 {{ num }}个文件，共 {{ count }} 个词条去人工翻译成 {{ lang }} 语言版本：新增 {{ add }} 个，重复 {{ exist }} 个'


class FILE_MARK_GLOSSARY(MsgType):
    template = u'{{ user }} 将 {{ file_count }} 个文件中共 {{ count }} 个词条标记为 {{ glossary }}'

#词条相关
class ENTRY_CREATE(MsgType):
    template = u'{{ user }} 创建了词条 {{ word }}'


class ENTRY_DELETE(MsgType):
    template = u'{{ user }} 删除了词条 {{ word }}'


class ENTRY_DELETE_MULTI(MsgType):
    template = u'{{ user }} 删除了 {{ cnt }} 个词条' \
               u'{% if words %}：' \
               u'{% for w in words %}{{ w|safe }}{% if loop.index != loop.length %}，{% endif %}{% endfor %}' \
               u'{% endif %}'


class ENTRY_HUMAN_TRANSLATE(MsgType):
    template = u'{{ user }} 提交了 {{ count }} 个词条去人工翻译成 {{ lang }} 语言版本：新增 {{ add }} 个，重复 {{ exist }} 个'


class ENTRY_MACHINE_TRANSLATE(MsgType):
    template = u'{{ user }} 提交了 {{ count }} 个词条去机器翻译成 {{ lang }} 语言版本'


class ENTRY_MARK_GLOSSARY(MsgType):
    template = u'{{ user }} 将 {{ count }} 个词条标记为 {{ glossary }}'


class ENTRY_MARK_GLOSSARY_ONE(MsgType):
    template = u'{{ user }} 将 {{ entry }} 标记为 {{ glossary }}'


class TAG_CREATE(MsgType):
    template = u'{{ user }} 创建了分类 {{ tag }}'


class TAG_DELETE(MsgType):
    template = u'{{ user }} 删除了分类 {{ tag }}'


class TAG_APPOINT(MsgType):
    template = u'{{ user }} 将词条 {{ word }} 指定分类为 {{ tag }}'

#暂时没有用到此类型
class TAG_CLEAR(MsgType):
    pass


class GLOSSARY(MsgType):
    try:
        if u'{{ flag }}' == u'count':
            template = u'{{ user }} 将 {{ count }} 个词条指定为 {{ glossary }}'
    except Exception as e:
        template = u'{{ user }} 将词条 {{ word }} 指定为 {{ glossary }}'


class IMPORT_EXCEL(MsgType):
    template = u'{{ user }} 选择了 {{ count }} 个词条进行导入'


class SUCCESS_IMPORT(MsgType):
    template = u'{{ user }} 导入词条结果：新增 {{ count }} 个，重复 {{ repeat }} 个，更新 {{ update }} 个'


class EXPORT_EXCEL(MsgType):
    template = u'{{ user }} 导出了 {{ lang }} 语言版本的词条'


class ADD_NEW_TRANSLATE(MsgType):
    template = u'{{ user }} 为词条 {{ entry }} 增加了 {{ tar_lang }} 语言的翻译结果 {{ target }}'


class ENABLE_TRANSLATE(MsgType):
    template = u'{{ user }} 为词条 {{ entry }} 使用了 {{ tar_lang }} 语言的翻译结果 {{ target }}'


class UPDATE_TRANSLATE(MsgType):
    template = u'{{ user }} 为词条 {{ entry }} 更新了 {{ tar_lang }} 语言的用户翻译结果 {{ target }}'

#域名相关
class DOMAIN_CREATE(MsgType):
    template = u'{{ user }} 创建了域名 {{ URL }}'


class DOMAIN_DELETE(MsgType):
    template = u'{{ user }} 删除了域名 {{ URL }}'


class STATUS_UPDATE(MsgType):
    template = u'{{ user }} {{ status }}了 {{ URL }} 等{{ count }}个域名'


class DOMAIN_NAME_CHANGE(MsgType):
    template = u'{{ user }} 更改 {{ URL }} 的名称为{{ name }}'


class VERIFY_CNAME(MsgType):
    template = u'{{ user }} 设置了 {{ URL }} 的CNAME为 {{ CNAME }} 并通过验证'


class CLEAR_CNAME(MsgType):
    template = u'{{ user }} 清除了 {{ URL }} 的CNAME'

#链接相关
class LINK_CREATE(MsgType):
    template = u'{{ user }} 创建了链接 {{ URL }}'


class LINK_DELETE(MsgType):
    template = u'{{ user }} 删除了链接 {{ URL }}'


class LINK_UPDATE(MsgType):
    template = u'{{ user }} 将链接 {{ OLD_URL }} 更新为 {% if URL %} {{ URL }} {% else %} 空 {% endif %}'


class REP_LINK_CREATE(MsgType):
    template = u'{{ user }} 为链接 {{ URL }} 创建了 {{ lang }} 版本的替换链接 {{ REP_URL }}'


class REP_LINK_UPDATE(MsgType):
    template = u'{{ user }} 将链接 {{ URL }} 的 {{ lang }} 版本链接 {{ OLD_URL }} 更新为 {% if NEW_URL %} {{ NEW_URL }} {% else %} 空 {% endif %}'

#本地化相关
class LOCAL_DELETE(MsgType):
    template = u'{{ user }} 删除了HTML替换 {{ localize }}'

# 字符串替换
class STR_CREATE(MsgType):
    template = u'{{ user }} 创建了{{ is_regex }}字符串 {{ string }}'


class STR_DELETE(MsgType):
    template = u'{{ user }} 删除了{{ is_regex }}字符串 {{ string }}'


class ORIGIN_STR_UPDATE(MsgType):
    template = u'{{ user }} 将原字符串 {{ origin }} 替换为 {{ string }}'


class REP_STR_UPDATE(MsgType):
    template = u'{{ user }} 将字符串 {{ origin }} 的 {{ lang }} 版本替换为 {{ string }}'

#设置相关
class ADD_TAR_LANG(MsgType):
    #添加目标语言  -- 2013-4-25起废弃
    template = u'{{ user }} 增加了目标语言 {{ info }}'


class REMOVE_TAR_LANG(MsgType):
    #删除目标语言  -- 2013-4-25起废弃
    template = u'{{ user }} 删除了目标语言 {{ info }}'


class UPDATE_TAR_LANGS(MsgType):
    #更新目标语言
    template = u'{{ user }} {{ status }}了目标语言 {{ langs }}'


class RESET_API_KEY(MsgType):
    #重置api key
    template = u'{{ user }} 重置了 API Key'


# 语言选择器相关
class CREATE_LANG_SELECTOR(MsgType):
    template = u'{{ user }} 创建并发布了域名 {{ url }} 的语言选择器'


class DELETE_LANG_SELECTOR(MsgType):
    template = u'{{ user }} 删除了域名 {{ url }} 的语言选择器'


class UPDATE_LANG_SELECTOR(MsgType):
    template = u'{{ user }} 更新了域名 {{ url }} 的语言选择器'


class CANCEL_LANG_SELECTOR(MsgType):
    template = u'{{ user }} 取消发布域名 {{ url }} 的语言选择器'


# 货币选择器相关
class CREATE_CURRENCY_SELECTOR(MsgType):
    template = u'{{ user }} 创建并发布了域名 {{ url }} 的货币选择器'


class DELETE_CURRENCY_SELECTOR(MsgType):
    template = u'{{ user }} 删除了域名 {{ url }} 的货币选择器'


class UPDATE_CURRENCY_SELECTOR(MsgType):
    template = u'{{ user }} 更新了域名 {{ url }} 的货币选择器'


class CANCEL_CURRENCY_SELECTOR(MsgType):
    template = u'{{ user }} 取消发布域名 {{ url }} 的货币选择器'


# 众包JS相关
class CREATE_CROWD_JS(MsgType):
    template = u'{{ user }} 创建并发布了域名 {{ url }} 的众包站点工具'


class DELETE_CROWD_JS(MsgType):
    template = u'{{ user }} 删除了域名 {{ url }} 的众包站点工具'


class CROWD_ENTRY_RESULT_USE(MsgType):
    template = u'{{ user }} 对众包词条 {{ word }} 使用了结果 {{ result }}'


#前端事件相关
class CREATE_SERVICE(MsgType):
    #创建服务
    template = u'{{ user }} 创建了项目 {{ name }}'


class RE_SUBMIT_TO_TRANS(MsgType):
    #重新提交去翻译
    template = u'{{ user }} 重新提交了 {{ file_path }} 去翻译'


class RE_PULL_ALL(MsgType):
    #全部重新提交
    template = u'{{ user }} 全部重新提交'


class CLEAR_LOG(MsgType):
    #清除日志
    template = u'{{ user }} 清除了日志'


class UPLOAD_FONT_FILE(MsgType):
    #上传字体文件
    template = u'{{ user }} 上传了字体文件 {{ file_path }}'

# 异常相关
class NO_XPATH_INFO(MsgType):
    #没有XPath信息
    template = u'没有XPath信息'


class EMPTY_XPATH_CONTENT(MsgType):
    #XPath content is empty
    template = u'XPath内容为空'


class XML_SYNTAX_ERROR(MsgType):
    #XML语法错误
    template = u'XML语法错误'


class UNKNOWN_ERROR(MsgType):
    #未知错误
    template = u'未知错误'


class SWF_EXTRACT_EXCEPTION(MsgType):
    #SWF分解异常
    template = u'{{ file_path }} 文件分解异常'


class UPLOAD_ZIP_FILE(MsgType):
    #上传zip文件
    template = u'{{ user }} 上传了ZIP文件 {{ file_path }}'


class UPLOAD_FILE(MsgType):
    #上传单个文件
    template = u'{{ user }} 上传了文件 {{ file_path }}'


class ADD_SVN_REPOSITORY(MsgType):
    #添加SVN仓库
    template = u'{{ user }} 添加了SVN仓库 {{ svn_url }}'


class DEL_SVN_REPOSITORY(MsgType):
    #删除SVN仓库
    template = u'{{ user }} 删除了SVN仓库 {{ svn_url }}'


class MODIFY_SVN_REPOSITORY(MsgType):
    #修改SVN仓库
    template = u'{{ user }} 删除了SVN仓库 {{ svn_url }}'


# 人员相关
class ADD_MEMBERSHIP(MsgType):
    template = u'{{ user }} 添加了{% if role %}{{ role }}{% endif %} {{ account }}'


# 人员相关
class ADD_MEMBERSHIP_TO_GROUP(MsgType):
    template = u'{{ user }} 添加了 {{ account }} 到角色组 {{ group }} 中'


class REMOVE_MEMBERSHIP(MsgType):
    template = u'{{ user }} 删除了{% if role %}{{ role }}{% endif %} {{ account }}'


# 翻译订单
class DELETE_TRANS_RECORD(MsgType):
    template = u'{{ user }} 删除了翻译任务 {{ name }}'


# 提交人工订单
class HUMAN_TRANS_TASK(MsgType):
    template = u'{{ user }} 提交了 {{ entry_cnt }}词条(共{{ word_cnt }}词)的 人工翻译任务 ' \
               u'{{ name }}，接收者 {{task_receiver}}， 共￥{{ cost }}'


# 指派翻译人员
class DISTRIBUTE_TRANSLATOR(MsgType):
    template = u'{{ user }} 为翻译任务 {{ name }} 指派了翻译人员 {{ translator }}，' \
               u'源语言：{{ src_lang }}，目标语言：{{ tar_lang }}'


# 删除翻译指派人员
class REMOVE_TRANSLATE_DISTRIBUTE(MsgType):
    template = u'{{ user }} 从翻译任务 {{ name }} 删除了翻译人员 {{ translator }}，' \
               u'源语言：{{ src_lang }}，目标语言：{{ tar_lang }}'


# 指派校对人员
class DISTRIBUTE_PROOFREADER(MsgType):
    template = u'{{ user }} 为翻译任务 {{ name }} 指派了校对人员 {{ translator }}，' \
               u'源语言：{{ src_lang }}，目标语言：{{ tar_lang }}'


# 删除校对指派人员
class REMOVE_PROOFREAD_DISTRIBUTE(MsgType):
    template = u'{{ user }} 从翻译任务 {{ name }} 删除了校对人员 {{ translator }}，' \
               u'源语言：{{ src_lang }}，目标语言：{{ tar_lang }}'


# 完成翻译指派
class FINISH_TRANSLATION(MsgType):
    template = u'{{ user }} 在翻译任务 {{ name }} 完成了译员 {{ translator }} 的翻译指派，' \
               u'源语言：{{ src_lang }}，目标语言：{{ tar_lang }}'


# 完成校对指派
class FINISH_PROOFREAD(MsgType):
    template = u'{{ user }} 在翻译任务 {{ name }} 完成了译员 {{ translator }} 的校对指派，' \
               u'源语言：{{ src_lang }}，目标语言：{{ tar_lang }}'


# 重新翻译
class RE_TRANSLATE(MsgType):
    template = u'{{ user }} 在翻译任务 {{ name }} 让译员 {{ translator }} 重新翻译，' \
               u'源语言：{{ src_lang }}，目标语言：{{ tar_lang }}'


# 重新校对
class RE_PROOFREAD(MsgType):
    template = u'{{ user }} 在翻译任务 {{ name }} 让译员 {{ translator }} 重新校对，' \
               u'源语言：{{ src_lang }}，目标语言：{{ tar_lang }}'


# 下载翻译结果
class DOWNLOAD_TRANSLATE_RESULT(MsgType):
    template = u'{{ user }} 在翻译任务 {{ name }} 下载了译员 {{ translator }} 的翻译结果，' \
               u'源语言：{{ src_lang }}，目标语言：{{ tar_lang }}'


# 接受校对建议
class ACCEPT_PROOFREAD_SUGGESTION(MsgType):
    template = u'{{ user }} 在翻译任务 {{ name }} 接受了译员 {{ translator }} 的校对建议，' \
               u'源语言：{{ src_lang }}，目标语言：{{ tar_lang }}'


# 批量接受校对建议
class BATCH_ACCEPT_PROOFREAD_SUGGESTION(MsgType):
    template = u'{{ user }} 在翻译任务 {{ name }} 批量接受了校对建议'


# 完成翻译任务
class FINISH_TASK(MsgType):
    template = u'{{ user }} 确定完成了翻译任务 {{ name }}'


def register_classes():
    for c in MsgType.__subclasses__():
        msg_dict[c.__name__] = c


register_classes()


def test():
    for k, v in msg_dict.iteritems():
        print k, v.get_code()

    print FILE_CREATE.get_display(params={'file': 'file.xml'})


if __name__ == '__main__':
    test()
