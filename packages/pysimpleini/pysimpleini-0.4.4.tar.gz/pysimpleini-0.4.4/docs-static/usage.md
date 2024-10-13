# Usage

## Installation

From pypi repository (prefered):
```console
/> python -m pip install pysimpleini
```   
 
From downloaded .whl file:
```console
/> python -m pip install pysimpleini-<VERSION>-py3-none-any.whl
```  

From master git repository:
```console
/> python -m pip install git+https://chacha.ddns.net/gitea/chacha/pysimpleini.git@master
```



## Import in your project

Add this line on the top of your python script:
```py
from pysimpleini import PySimpleINI
```
 
## Basic API

### Sample INI File:

```console
[testsection]
key1=test1
key2=test2
key3=test3
key3=test31

[testsection2]
key10=test10
```

### Load the INI File:

```py
myini:PySimpleINI = PySimpleINI("myinifile.ini")
```

### Access simple key values:

```py
print(myini.getkeyvalue("testsection", "key1"))
```
```console
test1
```

```py
print(myini.getkeyvalue("testsection", "key2"))
```
```console
test2
```

```py
print(myini.getkeyvalue("testsection", "key3"))
```
```console
['test3','test31']
```

```py
print(myini.getkeyvalue("testsection", "key3"))
```
```console
['test3','test31']
```

### Access key values with specified index:

```py
print(myini.getkeyvalue_ex("testsection", "key3",0))
```
```console
test3
```

```py
print(myini.getkeyvalue_ex("testsection", "key3",1))
```
```console
test31
```

### list keys name:

```py
print(myini.getallkeynames("testsection"))
```
```console
['key1', 'key2', 'key3', 'key3']
```

### list sections name:

```py
print(myini.getallsectionnames())
```
```console
['testsection', 'testsection2']
```

### add a new key:

```py
myini.setaddkeyvalue("testsection2","key11","test11")
print(myini.format())
```
```console
[testsection]
key1=test1
key2=test2
key3=test3
key3=test31
[testsection2]
key10=test10
key11=test11
```

### update a key value:

```py
myini.setaddkeyvalue("testsection2","key11","test13")
print(myini.format())
```
```console
[testsection]
key1=test1
key2=test2
key3=test3
key3=test31
[testsection2]
key10=test10
key11=test13
```

### create a new key with same name:

```py
myini.setaddkeyvalue("testsection2","key11","test14",True)
print(myini.format())
```
```console
[testsection]
key1=test1
key2=test2
key3=test3
key3=test31
[testsection2]
key10=test10
key11=test13
key11=test14
```

### create a new empty section

```py
myini.addsection("testsection3")
print(myini.format())
```
```console
[testsection]
key1=test1
key2=test2
key3=test3
key3=test31
[testsection2]
key10=test10
key11=test13
key11=test14
[testsection3]
```

### save your file
```py
myini.writefile()
```

### save to a new file
```py
myini.filepath = "somedir/somefile.ini"
myini.writefile()
```

__Read the API documentation and the unit test for more informations.__

## limitations

There is some known limitations.

1. File is only written when writefile() is called.

2. Support for more than one section with the same name is incomplete using setaddkeyvalue() / getkeyvalue_ex() / getkey_ex() / delkey_ex() because the index argument is only for keys. 
If more precise section selection is needed, please use getsection() to get the correct section object and then use the underlying methods.
