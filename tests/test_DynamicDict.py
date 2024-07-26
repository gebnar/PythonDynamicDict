import pytest

from DynamicDict import dynamic

def test_init_with_dict():
    d = {'key1': 'value1', 'key2': {'subkey1': 'subvalue1'}}
    dd = dynamic(d)
    assert dd.key1 == 'value1'
    assert dd['key1'] == 'value1'
    assert isinstance(dd.key2, dynamic)
    assert dd.key2.subkey1 == 'subvalue1'

def test_init_with_invalid():
    s = 'string1'
    with pytest.raises(TypeError):
        dd = dynamic(s)

def test_nested_dicts():
    d = {'level1': {'level2': {'level3': 'value3'}}}
    dd = dynamic(d)
    assert isinstance(dd.level1, dynamic)
    assert isinstance(dd.level1.level2, dynamic)
    assert dd.level1.level2.level3 == 'value3'

def test_init_without_dict():
    dd = dynamic()
    assert dd == {}
    assert len(dd) == 0

def test_setattr():
    dd = dynamic()
    dd.key = 'value'
    assert dd.key == 'value'    
    dd.subdict = {'subkey': 'subvalue'}
    assert isinstance(dd.subdict, dynamic)
    assert dd.subdict.subkey == 'subvalue'

def test_setattr_dict_type_error():
    dd = dynamic()
    with pytest.raises(TypeError):
        dd._dict = 'not a dict'

def test_iadd_with_dict():
    dd = dynamic({'key1': 'value1'})
    dd += {'key2': 'value2'}
    assert dd.key2 == 'value2'

def test_iadd_with_attrdict():
    dd1 = dynamic({'key1': 'value1'})
    dd2 = dynamic({'key2': 'value2'})
    dd1 += dd2
    assert dd1.key2 == 'value2'

def test_iadd_type_error():
    dd = dynamic()
    with pytest.raises(TypeError):
        dd += 123

def test_add_with_dict():
    dd = dynamic({'key1': 'value1'})
    dd = dd + {'key2': 'value2'}
    assert dd.key2 == 'value2'

def test_isub_with_dict_strict():
    dd = dynamic({'key1': 'value1', 'key2': 'value2'})
    dd -= {'key2': 'value2'}
    dd -= {'key1': 'value1b'}
    assert dd.key1 == 'value1'
    assert 'key2' not in dd

def test_isub_with_dict_lax():
    dd = dynamic({'key1': 'value1', 'key2': 'value2'}, _strict_subtraction = False)
    dd -= {'key2': 'value2b'}
    assert 'key2' not in dd

def test_change_strict_subtraction_mode():
    dd = dynamic({'key1': 'value1', 'key2': 'value2'})
    dd._strict_subtraction = False
    dd -= {'key2': 'value2b'}
    assert 'key2' not in dd

def test_isub_with_attrdict():
    dd1 = dynamic({'key1': 'value1', 'key2': 'value2'})
    dd2 = dynamic({'key2': 'value2'})
    dd1 -= dd2
    assert 'key2' not in dd1

def test_sub_with_dict():
    dd = dynamic({'key1': 'value1','key2':'value2'})
    dd = dd - {'key2': 'value2'}
    assert 'key2' not in dd

def test_getattr():
    dd = dynamic({'key': 'value'})
    assert dd.key == 'value'
    with pytest.raises(AttributeError):
        _ = dd.non_existent_key

def test_delattr():
    dd = dynamic({'key': 'value'})
    assert dd.key == 'value'
    del dd.key
    assert 'key' not in dd
    with pytest.raises(AttributeError):
        del dd.non_existent_key

def test_iter():
    d = {'key1': 'value1', 'key2': 'value2'}
    dd = dynamic(d)
    for key, value in dd:
        assert d[key] == value

def test_repr():
    d = {'key1': 'value1', 'key2': 'value2'}
    dd = dynamic(d)
    assert repr(dd) == repr(d)

def test_getitem():
    dd = dynamic({'key': 'value'})
    assert dd['key'] == 'value'
    with pytest.raises(KeyError):
        _ = dd['non_existent_key']

def test_contains():
    dd = dynamic({'key': 'value'})
    assert 'key' in dd
    assert 'non_existent_key' not in dd

def test_contains_for_nested_keys():
    dd = dynamic({'key1': {'subkey1': 'subvalue1'}})
    assert 'key1' in dd
    assert 'subkey1' not in dd
    assert 'subkey1' in dd.key1

def test_eq():
    dd1 = dynamic({'key': 'value'})
    dd2 = dynamic({'key': 'value'})
    assert dd1 == dd2
    assert dd1 == {'key': 'value'}
    assert dd1 != {'key': 'different_value'}
    assert dd1 != 123

def test_bool():
    dd1 = dynamic({'key': 'value'})
    dd2 = dynamic()
    assert bool(dd1)
    assert not bool(dd2)

def test_len():
    dd = dynamic({'key1': 'value1', 'key2': 'value2'})
    assert len(dd) == 2

def test_str():
    d = {'key1': 'value1', 'key2': 'value2'}
    dd = dynamic(d)
    assert str(dd) == str(d)

def test_func_key():
    d = dynamic({'key1':'value1'})
    def f():
        return 'FuncValue'
    d.f = f
    assert d.f() == 'FuncValue'

def test_mutation():
    s = 'string1'
    d = dynamic()
    d.s = s
    assert d.s == 'string1'
    s = 'string2'
    assert d.s == 'string1'

def test_use_inspection_disabled():
    s = 'string1'
    dd = dynamic()
    with pytest.raises(TypeError):
        dd += s

def test_internal_dict_methods():
    dd = dynamic({'key1':'value1'})
    assert dd._dict.get('key1') == 'value1'

def test_initialize_with_dynamic():
    dd = dynamic({'key1':'value1'})
    dd2 = dynamic(dd)
    assert dd2.key1 == 'value1'

def test_namespace_preservation():
    dd = dynamic()
    dd.keys = lambda: 'Some Keys'
    assert dd.keys() == 'Some Keys'

def test_unsafe_delete():
    dd = dynamic()
    with pytest.raises(AttributeError):
        del dd._dict

def test_key_renaming():
    dd = dynamic({'key 1':'value 1'})
    assert dd.key_1 == 'value 1'

def test_key_renaming_duplicates():
    dd = dynamic({'key 1':'value 1','key%1':'value 2'})
    assert len(dd) == 1