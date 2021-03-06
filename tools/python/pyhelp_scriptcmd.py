'''
//===== rAthenaCN Python Script ============================== 
//= 脚本指令添加助手
//===== By: ================================================== 
//= Sola丶小克
//===== Current Version: ===================================== 
//= 1.0
//===== Description: ========================================= 
//= 此脚本用于快速建立一个新的脚本指令(Script Command)
//===== Additional Comments: ================================= 
//= 1.0 首个版本. [Sola丶小克]
//============================================================

// PYHELP - SCRIPTCMD - INSERT POINT - <Section 1>
rathena.hpp @ 宏定义

// PYHELP - SCRIPTCMD - INSERT POINT - <Section 2>
script.cpp @ BUILDIN_FUNC 脚本指令实际代码

// PYHELP - SCRIPTCMD - INSERT POINT - <Section 3>
script.cpp @ BUILDIN_DEF 脚本指令导出
'''

# -*- coding: utf-8 -*-

import os

from libs import InjectController, InputController
from libs import Common, Message

def insert_scriptcmd(inject, options):
    define = options['define']
    funcname = options['funcname']
    cmdname = options['cmdname']
    argsmode = options['argsmode']
    
    # rathena.hpp @ 宏定义
    inject.insert(1, [
        '',
        '\t// 是否启用 %s 脚本指令 [维护者昵称]' % cmdname,
        '\t// TODO: 请在此填写此脚本指令的说明',
        '\t#define %s' % define
    ])
    
    usage = ' * 用法: %s;' % cmdname
    if argsmode != '':
        usage = ' * 用法: %s <请补充完整参数说明>;' % cmdname
    
    # script.cpp @ BUILDIN_FUNC 脚本指令实际代码
    inject.insert(2, [
        '#ifdef %s' % define,
        '/* ===========================================================',
        ' * 指令: %s' % cmdname,
        ' * 描述: 请在此补充该脚本指令的说明',
        usage,
        ' * 返回: 请说明返回值',
        ' * 作者: 维护者昵称',
        ' * -----------------------------------------------------------*/',
        'BUILDIN_FUNC(%s) {' % funcname,
        '\t// TODO: 请在此填写脚本指令的实现代码',
        '\treturn SCRIPT_CMD_SUCCESS;',
        '}',
        '#endif // %s' % define,
        ''
    ])
    
    # script.cpp @ BUILDIN_DEF 脚本指令导出
    
    if funcname == cmdname:
        defcontent = '\tBUILDIN_DEF(%s,"%s"),\t\t\t\t\t\t// 在此写上脚本指令说明 [维护者昵称]' % (funcname, argsmode)
    else:
        defcontent = '\tBUILDIN_DEF2(%s,"%s","%s"),\t\t\t\t\t\t// 在此写上脚本指令说明 [维护者昵称]' % (funcname, cmdname, argsmode)
    
    inject.insert(3, [
        '#ifdef %s' % define,
        defcontent,
        '#endif // %s' % define
    ])

def welecome():
    print('=' * 70)
    print('')
    print('脚本指令添加助手'.center(62))
    print('')
    print('=' * 70)
    print('')

    Message.ShowInfo('在使用此脚本之前, 建议确保 src 目录的工作区是干净的.')
    Message.ShowInfo('这样添加结果如果不符合预期, 可以轻松的利用 git 进行重置操作.')

def guide(inject):

    define = InputController().requireText({
        'tips' : '请输入该脚本指令的宏定义开关名称 (rAthenaCN_ScriptCommand_的末尾部分)',
        'prefix' : 'rAthenaCN_ScriptCommand_'
    })
    
    # --------

    funcname = InputController().requireText({
        'tips' : '请输入该脚本指令的处理函数名称 (BUILDIN_FUNC 部分的函数名)',
        'prefix' : '',
        'lower': True
    })
    
    # --------
    
    samefunc = InputController().requireBool({
        'tips' : '脚本指令是否与处理函数名称一致 (%s)?' % funcname,
        'default' : True
    })
    
    # --------
    
    cmdname = funcname
    if not samefunc:
        cmdname = InputController().requireText({
            'tips' : '请输入该脚本指令的名称 (BUILDIN_DEF2 使用)',
            'prefix' : '',
            'lower' : True
        })
    
    # --------
    
    argsmode = InputController().requireText({
        'tips' : '请输入该脚本指令的参数模式 (如一个或多个的: i\s\? 为空则直接回车)',
        'prefix' : '',
        'lower' : True,
        'allow_empty' : True
    })
    
    # --------
    
    print('-' * 70)
    Message.ShowInfo('请确认建立的信息, 确认后将开始修改代码.')
    print('-' * 70)
    Message.ShowInfo('开关名称 : %s' % define)
    Message.ShowInfo('脚本处理函数名称 : %s' % funcname)
    Message.ShowInfo('脚本指令名称 : %s' % cmdname)
    Message.ShowInfo('脚本指令的参数模式 : %s' % argsmode)
    print('-' * 70)
    print('\n')

    nextstep = InputController().requireBool({
        'tips' : '请仔细阅读上述信息, 确认要开始写入操作么?',
        'default' : False
    })

    if not nextstep:
        Message.ShowStatus('终止写入操作, 程序终止')
        Common.exitWithPause(-1)

    # --------

    Message.ShowStatus('开始将地图标记信息写入到源代码...')
    
    options = {
        'define' : define,
        'funcname' : funcname,
        'cmdname' : cmdname,
        'argsmode' : argsmode
    }
    
    insert_scriptcmd(inject, options)
    
    Message.ShowStatus('已经成功写入到源代码, 请检查并完善必要的注释.')
    print('')
    print('=' * 70)
    print('')
    print('感谢您的使用, 脚本指令添加助手已经执行完毕'.center(48))
    print('')
    print('=' * 70)

def main():
    os.chdir(os.path.split(os.path.realpath(__file__))[0])

    welecome()

    options = {
        'source_dirs' : '../../src',
        'process_exts' : ['.hpp', '.cpp'],
        'mark_format' : r'// PYHELP - SCRIPTCMD - INSERT POINT - <Section (\d{1,2})>',
        'mark_counts' : 3
    }

    guide(InjectController(options))
    Common.exitWithPause()

if __name__ == '__main__':
    main()
