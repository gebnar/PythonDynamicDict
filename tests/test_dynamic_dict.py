# Copyright (c) 2024 Shane Plesner
#
# This software is released under the MIT License
# https://opensource.org/licenses/MIT

import pytest

from dynamic_dict import Dynamic

def test_init_with_dict():
    d = {'key1': 'value1', 'key2': {'subkey1': 'subvalue1'}}
    dd = Dynamic(d)
    assert dd.key1 == 'value1'
    assert dd['key1'] == 'value1'
    assert isinstance(dd.key2, Dynamic)
    assert dd.key2.subkey1 == 'subvalue1'

def test_init_with_invalid():
    s = 'string1'
    with pytest.raises(TypeError):
        dd = Dynamic(s)

def test_nested_dicts():
    d = {'level1': {'level2': {'level3': 'value3'}}}
    dd = Dynamic(d)
    assert isinstance(dd.level1, Dynamic)
    assert isinstance(dd.level1.level2, Dynamic)
    assert dd.level1.level2.level3 == 'value3'

def test_init_without_dict():
    dd = Dynamic()
    assert dd == {}
    assert len(dd) == 0

def test_setattr():
    dd = Dynamic()
    dd.key = 'value'
    assert dd.key == 'value'    
    dd.subdict = {'subkey': 'subvalue'}
    assert isinstance(dd.subdict, Dynamic)
    assert dd.subdict.subkey == 'subvalue'

def test_setattr_dict_type_error():
    dd = Dynamic()
    with pytest.raises(TypeError):
        dd._dict = 'not a dict'

def test_iadd_with_dict():
    dd = Dynamic({'key1': 'value1'})
    dd += {'key2': 'value2'}
    assert dd.key2 == 'value2'

def test_iadd_with_attrdict():
    dd1 = Dynamic({'key1': 'value1'})
    dd2 = Dynamic({'key2': 'value2'})
    dd1 += dd2
    assert dd1.key2 == 'value2'

def test_iadd_type_error():
    dd = Dynamic()
    with pytest.raises(TypeError):
        dd += 123

def test_add_with_dict():
    dd = Dynamic({'key1': 'value1'})
    dd = dd + {'key2': 'value2'}
    assert dd.key2 == 'value2'

def test_isub_with_dict_strict():
    dd = Dynamic({'key1': 'value1', 'key2': 'value2'})
    dd -= {'key2': 'value2'}
    dd -= {'key1': 'value1b'}
    assert dd.key1 == 'value1'
    assert 'key2' not in dd

def test_isub_with_dict_lax():
    dd = Dynamic({'key1': 'value1', 'key2': 'value2'}, _strict_subtraction = False)
    dd -= {'key2': 'value2b'}
    assert 'key2' not in dd

def test_change_strict_subtraction_mode():
    dd = Dynamic({'key1': 'value1', 'key2': 'value2'})
    dd._strict_subtraction = False
    dd -= {'key2': 'value2b'}
    assert 'key2' not in dd

def test_isub_with_attrdict():
    dd1 = Dynamic({'key1': 'value1', 'key2': 'value2'})
    dd2 = Dynamic({'key2': 'value2'})
    dd1 -= dd2
    assert 'key2' not in dd1

def test_sub_with_dict():
    dd = Dynamic({'key1': 'value1','key2':'value2'})
    dd = dd - {'key2': 'value2'}
    assert 'key2' not in dd

def test_getattr():
    dd = Dynamic({'key': 'value'})
    assert dd.key == 'value'
    with pytest.raises(AttributeError):
        _ = dd.non_existent_key

def test_delattr():
    dd = Dynamic({'key': 'value'})
    assert dd.key == 'value'
    del dd.key
    assert 'key' not in dd
    with pytest.raises(AttributeError):
        del dd.non_existent_key

def test_iter():
    d = {'key1': 'value1', 'key2': 'value2'}
    dd = Dynamic(d)
    for key, value in dd:
        assert d[key] == value

def test_repr():
    d = {'key1': 'value1', 'key2': 'value2'}
    dd = Dynamic(d)
    assert repr(dd) == repr(d)

def test_getitem():
    dd = Dynamic({'key': 'value'})
    assert dd['key'] == 'value'
    with pytest.raises(KeyError):
        _ = dd['non_existent_key']

def test_contains():
    dd = Dynamic({'key': 'value'})
    assert 'key' in dd
    assert 'non_existent_key' not in dd

def test_contains_for_nested_keys():
    dd = Dynamic({'key1': {'subkey1': 'subvalue1'}})
    assert 'key1' in dd
    assert 'subkey1' not in dd
    assert 'subkey1' in dd.key1

def test_eq():
    dd1 = Dynamic({'key': 'value'})
    dd2 = Dynamic({'key': 'value'})
    assert dd1 == dd2
    assert dd1 == {'key': 'value'}
    assert dd1 != {'key': 'different_value'}
    assert dd1 != 123

def test_bool():
    dd1 = Dynamic({'key': 'value'})
    dd2 = Dynamic()
    assert bool(dd1)
    assert not bool(dd2)

def test_len():
    dd = Dynamic({'key1': 'value1', 'key2': 'value2'})
    assert len(dd) == 2

def test_str():
    d = {'key1': 'value1', 'key2': 'value2'}
    dd = Dynamic(d)
    assert str(dd) == str(d)

def test_func_key():
    d = Dynamic({'key1':'value1'})
    def f():
        return 'FuncValue'
    d.f = f
    assert d.f() == 'FuncValue'

def test_mutation():
    s = 'string1'
    d = Dynamic()
    d.s = s
    assert d.s == 'string1'
    s = 'string2'
    assert d.s == 'string1'

def test_use_inspection_disabled():
    s = 'string1'
    dd = Dynamic()
    with pytest.raises(TypeError):
        dd += s

def test_internal_dict_methods():
    dd = Dynamic({'key1':'value1'})
    assert dd._dict.get('key1') == 'value1'

def test_initialize_with_dynamic():
    dd = Dynamic({'key1':'value1'})
    dd2 = Dynamic(dd)
    assert dd2.key1 == 'value1'

def test_namespace_preservation():
    dd = Dynamic()
    dd.keys = lambda: 'Some Keys'
    assert dd.keys() == 'Some Keys'

def test_unsafe_delete():
    dd = Dynamic()
    with pytest.raises(AttributeError):
        del dd._dict

def test_key_renaming():
    dd = Dynamic({'key 1':'value 1'})
    assert dd.key_1 == 'value 1'

def test_key_renaming_duplicates():
    dd = Dynamic({'key 1':'value 1','key%1':'value 2'})
    assert len(dd) == 1

def test_strict_typing():
    dd = Dynamic({
        'number_key': 123,
        'string_key': 'my string',
        'dict_key': {'subkey':'subvalue'},
        'exception_key': TypeError,
    },_strict_typing = True)
    with pytest.raises(TypeError):
        dd.number_key = 'not a number'
    dd.number_key = 321
    assert dd.number_key == 321
    with pytest.raises(TypeError):
        dd.string_key = 123
    dd.string_key = 'another string'
    assert dd.string_key == 'another string'
    with pytest.raises(TypeError):
        dd.dict_key = 'not a dict'
    dd.dict_key = {'a':'new dict'}
    assert dd.dict_key.a == 'new dict'
    with pytest.raises(TypeError):
        dd.exception_key = 'not an error'
    dd.exception_key = AttributeError
    assert dd.exception_key == AttributeError
    dd.exception_key = None
    assert dd.exception_key == None
    dd.exception_key = AssertionError
    assert dd.exception_key == AssertionError

def test_add_parameter_preservation():
    dd = Dynamic({'number_key':123},_strict_typing = True)
    dd2 = dd + {'string_key':'some string'}
    assert dd2._strict_typing == True
    dd3 = Dynamic({'string_key':'some string'}) + dd
    assert dd3._strict_typing == False

def test_sub_parameter_preservation():
    d = {'number_key':123}
    dd = Dynamic(d,_strict_typing = True)
    dd2 = dd - d
    assert dd2._strict_typing == True
    dd3 = Dynamic(d) - dd
    assert dd3._strict_typing == False