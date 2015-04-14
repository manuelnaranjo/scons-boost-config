# -*- coding: utf-8 -*-

# A SCons tool to simplify pkg-config usage on SCons
#
# Copyright (c) 2015 Naranjo Manuel Francisco < naranjo dot manuel at gmail dot com >
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from functools import partial

MINVERSION = '1.54.0'

def exists(env):
    # we suppose the tool is always available
    return True

def BjamSupported(context):
    text = 'Checking for ${BJAM_BIN} ...'
    instruction = '${BJAM_BIN} -v'

    context.Message(context.env.subst(text))
    ret = context.TryAction(instruction)[0]
    context.Result(ret == 1)
    return ret == 1

VERSION_TEMPLATE='''
#include <boost/version.hpp>

#if BOOST_VERSION < %d
#error Installed boost version is too old!
#endif

int main() {
    return 0;
}
'''
def BoostVersionCheck(context, version = MINVERSION):
    context.Message('Checking for boost version %s... ' % version)
    v_arr = vesion.split('.')
    v_num = 0
    if len(v_arr) > 0:
        v_num += int(v_arr[0]) * 100000
    if len(v_arr) > 1:
        v_num += int(v_arr[1]) * 100
    if len(v_arr) > 2:
        v_num += int(v_arr[2])

    ret = context.TryCompile(VERSION_TEMPLATE % v_num, '.cpp')
    context.Result(ret)
    return ret

# libs supported so far by FindBoostLibrary
SUPPORTED = [
    ''
]

def FindBoostLibrary(env, conf, name, version=None):
    '''
    This method will try to find a name boost library

    '''
    if name not in SUPPORTED:
        raise Exception, 'boost-%s not supported by this tool yet' % name

    if 'ld' not in env['LINK']:
        raise Exception, 'Only gcc linker is supported by this tool'

    base = 'boost_%s' % name

    conf.env['BOOST_PREFIX'] = ''
    conf.env['BOOST_LIB'] = base
    conf.env['BOOST_SUFFIX'] = ''

    if version is not None:
        conf.env['BOOST_PREFIX'] = ':${SHLIBPREFIX}'
        conf.env['BOOST_SUFFIX'] = '${SHLIBSUFFIX}.%s' % version

    lib = '${BOOST_PREFIX}${BOOST_LIB}${BOOST_SUFFIX}'
    if conf.TryLink(lib):
        return conf.env.subst(lib)

def generate(env):
    from SCons import SConf
    SConfBase = SConf.SConfBase

    if not env.has_key('BJAM_BIN'):
        env['BJAM_BIN'] = 'bjam'

    class BoostSConfBase(SConfBase):
        def __init__(self, env, custom_tests = {}, *a, **kw):
            my_tests = {
                'BjamSupported': BjamSupported,
                'BoostVersionCheck': BoostVersionCheck,
            }
            my_tests.update(custom_tests)
            SConfBase.__init__(self, env, my_tests, *a, **kw)

    setattr(SConf, 'SConfBase', BoostSConfBase)
    env.AddMethod(FindBoostLibrary)
