# Python 考试备考手册

### 1. 第三方库 (Third-party Libraries)

* **是什么？** 

  想象一下你的Python自带了一些基础工具（标准库），但有时你需要更厉害的工具来完成特定任务（比如分析数据、做游戏）。第三方库就是其他厉害的程序员写好的、可以共享的工具包。

  

* **应用领域？** 

  它们可以用在很多地方：数据科学（处理和分析数字信息）、网站开发、游戏制作、人工智能等等。

  

* **常用库有哪些？**

  `pandas` (处理表格数据)、`numpy` (科学计算)、`requests` (访问网站)、`pygame` (做游戏)。

  

* **如何安装？** 

  通常在电脑的"命令行"或"终端"里输入 `pip install 库的名字`，比如 `pip install pandas`。`pip` 是Python的管理工具，专门用来安装这些库。

  

* **如何导入？**

  在你的Python代码开头写 `import 库的名字`，比如 `import math`。有时为了方便，可以给库起个别名，如 `import pandas as pd`。

  

### 2. 标准库 (Standard Libraries)

* **是什么？** 

  这是Python自带的工具箱，安装Python时就有了，不需要额外安装。

  

*   **`math` 库:** 包含很多数学计算的工具。
    * `math.sqrt(x)`: 计算x的平方根。例如 `math.sqrt(16)` 结果是 `4.0`。
    
    * `math.pi`: 圆周率 π (约等于 3.14159)。
    
    * `math.pow(x, y)`: 计算 x 的 y 次方。例如 `math.pow(2, 3)` 结果是 `8.0`。
    
    * 还有很多其他函数，比如 `sin`, `cos`, `log` 等，了解即可。
    
      
    
*   **`random` 库:** 用来生成随机的东西。
    
    * `random.random()`: 生成一个0到1之间的随机小数。
    
    * `random.randint(a, b)`: 生成一个a到b之间的随机整数（包括a和b）。例如 `random.randint(1, 6)` 可能生成 1, 2, 3, 4, 5, 6 中的任意一个。
    
    * `random.choice(列表)`: 从一个列表里随机选一个元素。例如 `random.choice(['苹果', '香蕉', '橘子'])`。
    
    * `random.shuffle(列表)`: 把列表里的元素顺序打乱。
    
      
    
*   **`tkinter` 库:** 用来创建图形用户界面（就是带窗口、按钮的那种程序），考试不会深入考。



### 3. 内置函数 (Built-in Functions)

* **是什么？** 

  这些是Python最基础的命令，直接就可以用，不需要 `import`。

  

* **`max / min(可迭代对象)`:** 找出一组数或一个列表里的最大值 / 最小值。例如 `max(1, 5, 3)` 结果是 `5`，`max([2, 8, 1])` 结果是 `8`。`min(1, 5, 3)` 结果是 `1`。

  

* **`sum(可迭代对象)`:** 计算一组数的和。例如 `sum([1, 2, 3, 4])` 结果是 `10`。

  

* **`sorted(可迭代对象)`:** 把列表或其它可迭代对象排序，返回一个新的排好序的列表。例如 `sorted([3, 1, 4, 2])` 结果是 `[1, 2, 3, 4]`。默认是从小到大，可以加参数 `reverse=True` 从大到小排。

  

* **`len(对象)`:** 计算对象的长度（比如字符串有多少个字符，列表有多少个元素）。例如 `len("hello")` 结果是 `5`，`len([1, 2, 3])` 结果是 `3`。

  

* **`type(对象)`:** 查看对象是什么类型。例如 `type(123)` 结果是 `<class 'int'>` (整数)，`type("abc")` 结果是 `<class 'str'>` (字符串)。

  

*   **`int(x)`, `float(x)`, `str(x)`:** 类型转换。`int()` 转成整数，`float()` 转成小数，`str()` 转成字符串。例如 `int("10")` 结果是 `10`，`str(10)` 结果是 `"10"`。

### 4. 其他概念

* **正则表达式 (Regular Expressions):** 

  一种描述文本模式的方法，用来在字符串里查找、替换符合特定规则的内容。比如可以用它来检查邮箱地址格式是否正确。是一种高级的查找技巧。

  

* **迭代器 (Iterators) & 生成器 (Generators):** 

  它们都用于处理一系列的数据，但特点是"懒加载"，即一次只处理一个数据，而不是一次性把所有数据都加载到内存里。这样可以节省内存，特别是在处理大量数据时。生成器是一种特殊的迭代器，用函数和 `yield` 关键字创建。

  

* **文件操作 (Files)**:

   Python可以读取电脑上的文件内容，也可以往文件里写入内容。常用步骤是：打开文件 (`open()`) -> 读取 (`read()`) 或写入 (`write()`) -> 关闭文件 (`close()`)。使用 `with open(...) as ...:` 结构更安全，可以自动关闭文件。

  

* **数据库编程 (Database Programming):** 

  把数据存到专门的数据库软件里，方便管理和查询。Python可以通过特定的库（如 `sqlite3`, `pymysql`）来连接和操作数据库。

### 5. 字符与数字转换

* **`ord(字符)`:** 获取一个字符对应的数字（ASCII码或Unicode码）。例如 `ord('A')` 结果是 `65`，`ord('a')` 结果是 `97`。

* **`chr(数字)`:** 获取一个数字对应的字符。例如 `chr(65)` 结果是 `'A'`，`chr(97)` 结果是 `'a'`。

  | 十进制 | 二进制  | 字符 |   描述    |
  | :----: | :-----: | :--: | :-------: |
  |   0    | 0000000 | NUL  |  空字符   |
  |        |         |      |           |
  |   48   | 0110000 |  0   |   数字0   |
  |   49   | 0110001 |  1   |   数字1   |
  |   50   | 0110010 |  2   |   数字2   |
  |        |         |      |           |
  |   65   | 1000001 |  A   | 大写字母A |
  |   66   | 1000010 |  B   | 大写字母B |
  |   67   | 1000011 |  C   | 大写字母C |
  |        |         |      |           |
  |   97   | 1100001 |  a   | 小写字母a |
  |   98   | 1100010 |  b   | 小写字母b |
  |   99   | 1100011 |  c   | 小写字母c |

### 6. 面向对象编程 (Object-Oriented Programming, OOP) 概念

* **是什么？**

  面向对象编程是一种编程思想，把世界万物看作是"对象"，每个对象有自己的"属性"（特征）和"方法"（能做什么）。

  

* **类 (Class):** 

  对象的"图纸"或"模板"。定义了一个类，就规定了这类对象应该有哪些属性和方法。比如定义一个 `Dog` 类。

  

* **对象 (Object) / 实例 (Instance):** 

  根据类的图纸创建出来的具体的东西。比如根据 `Dog` 类创建出一只叫"旺财"的具体的狗。

  

* **继承 (Inheritance):** 

  一个类可以"继承"另一个类的属性和方法，就像儿子继承父亲的特征一样。比如可以创建一个 `GoldenRetriever` 类继承自 `Dog` 类，它就自动拥有了 `Dog` 的所有属性和方法，还可以添加自己特有的。

  

* **公有属性 (Public Attribute):** 

  对象里谁都可以访问的属性。

  

* **私有属性 (Private Attribute):** 

  对象里受保护的属性，通常以双下划线开头 (如 `__name`)，不建议在类的外部直接访问。这是一种封装，保护内部数据不被随意修改。

  

* **Mixin:** 

  一种特殊的设计模式。一个类可以"混入"（Mixin）另一个类的功能，但它们之间不一定是严格的"父子"继承关系。通常用于给多个不相关的类添加相同的功能。

  

*   **魔术方法 (Magic Methods):**
    
     Python中以双下划line开头和结尾的方法，如 `__init__`, `__str__`, `__len__` 等。它们有特殊的含义，会在特定情况下自动被调用。
    
    *   `__init__(self, ...)`: 构造函数，创建对象时自动调用，用来初始化对象的属性。
    *   `__str__(self)`: 当你尝试用 `print()` 打印对象时，会调用这个方法，返回一个描述对象的字符串。
    *   `__len__(self)`: 当你对对象使用 `len()` 函数时，会调用这个方法。

### 7. 字符串、列表、字典、集合操作

*   **字符串 (String):** 就是文本。
    
    * 创建: `s = "hello"`
    
    * 拼接: `s1 + s2`
    
    * 访问单个字符: `s[0]` (第一个字符), `s[-1]` (最后一个字符)
    
    * 切片: `s[1:4]` (从第2个到第4个字符，不包括第4个)
    
    * 常用方法: `len()`, `s.find()`, `s.replace()`, `s.split()`, `s.lower()`, `s.upper()`, `s.strip()`
    
      
    
*   **列表 (List):** 有序的、可以修改的元素集合。
    * 创建: `my_list = [1, "a", True]`
    
    * 访问: `my_list[0]`
    
    * 修改: `my_list[1] = "b"`
    
    * 切片: `my_list[1:3]`
    
    * 常用方法: `len()`, `my_list.append()`, `my_list.insert()`, `my_list.pop()`, `my_list.remove()`, `my_list.sort()`, `my_list.reverse()`
    
      
    
*   **字典 (Dictionary):** 无序的、键值对 (key-value) 的集合，key必须是唯一的且不可变。
    * 创建: `my_dict = {"name": "小明", "age": 12}`
    
    * 访问 (通过key): `my_dict["name"]`
    
    * 添加/修改: `my_dict["score"] = 95`, `my_dict["age"] = 13`
    
    * 常用方法: `len()`, `my_dict.keys()`, `my_dict.values()`, `my_dict.items()`, `my_dict.get(key, default_value)`, `my_dict.pop(key)`
    
      
    
*   **集合 (Set):** 无序的、不重复的元素集合。主要用于去重和成员测试。
    
    * 创建: `my_set = {1, 2, 3, 2}` (结果是 `{1, 2, 3}`) 或 `my_set = set([1, 2, 3])`
    
    * 操作: `add()`, `remove()`, 并集 `|`, 交集 `&`, 差集 `-`
    
      
    
* **组合数据类型嵌套:** 就是把它们套起来用，比如

  列表里放字典 `[{'name': 'A'}, {'name': 'B'}]`

  字典的值是列表 `{'scores': [90, 85, 92]}`。

### 8. 面向对象编程 (OOP)

* **类和对象:** 

  理解如何用 `class` 定义一个类（图纸），如何用 `类名()` 创建一个对象（实例）。

  

* **构造函数 `__init__(self, ...)`:**

  每个类通常都有这个方法，在创建对象时自动运行，用来设置对象的初始属性 (比如 `self.name = name`)。`self` 代表对象本身。

  

* **运算符重载:** 

  让类自定义标准运算符（如 `+`, `-`, `*`, `/`, `<`, `>`, `==` 等）的行为。比如，可以定义两个 `Vector` 对象相加是什么意思。需要实现对应的魔术方法（如 `__add__` 对应 `+`， `__lt__` 对应 `<`）。

### 9. 函数定义和调用

```python
def add(a, b):
    result = a + b
    return result
sum_result = add(5, 3) # sum_result 会得到 8
print(sum_result)
```

### 10. 异常处理 (Exception Handling)

* **是什么？** 

  程序运行时可能会出错（比如用户输入了非数字，或者要打开的文件不存在），异常处理就是抓住这些错误，让程序不至于崩溃，而是能优雅地处理。

*   **`try...except` 结构:**
    
    ```python
    try:
        # 可能会出错的代码放这里
        num = int(input("请输入一个数字: "))
        result = 10 / num
        print(result)
        
    except ValueError:
        # 如果 try 块里发生了 ValueError (比如输入了字母)
        print("输入无效，请输入数字！")
        
    except ZeroDivisionError:
        # 如果 try 块里发生了 ZeroDivisionError (比如输入了 0)
        print("错误：不能除以零！")
        
    except Exception as e:
        # 捕捉其他所有类型的错误
        print(f"发生了未知错误: {e}")
        
    finally:
        # 无论是否发生错误，finally 块里的代码总会执行
        print("程序尝试执行完毕。")
    ```
    
    |      异常类型       |                        主要内容描述                        |                          区别                          |         触发样例          |
    | :-----------------: | :--------------------------------------------------------: | :----------------------------------------------------: | :-----------------------: |
    |     ValueError      | 当操作或函数接收到具有正确类型但不适当值的参数时引发的异常 |      表示参数值不合法，但类型正确，常见于转换函数      |       `int("abc")`        |
    |      TypeError      |       当操作或函数应用于不适当类型的对象时引发的异常       |      表示参数类型不正确，例如对字符串执行数学运算      |         `"5" + 3`         |
    |     IndexError      |   当序列（如列表、元组）中没有具有请求的索引时引发的异常   |      表示索引超出范围，常见于访问不存在的列表元素      |       `[1,2,3][5]`        |
    |      KeyError       |              当字典中没有指定的键时引发的异常              |  表示访问不存在的字典键值对，类似IndexError但针对字典  |      `{"a":1}["b"]`       |
    |  FileNotFoundError  |        当尝试打开或访问一个不存在的文件时引发的异常        | 表示文件不存在，属于OSError的子类，处理文件操作时常见  | `open("nonexistent.txt")` |
    | `ZeroDivisionError` |     当执行除法或取模运算时，除数或模数为零时引发的异常     |        表示除以零的数学错误，数学上无意义的操作        |          `5 / 0`          |
    |  `AssertionError`   |       当断言（`assert` 语句）的条件为假时引发的异常        | 用于调试和测试，表示代码中的逻辑错误或不符合预期的情况 |      `assert 1 == 2`      |

### 11. 选择和循环结构编程

```python
score = 75
if score >= 90:
    print("优秀")
elif score >= 60:
    print("及格")
else:
    print("不及格")

# ----------------------------------------------------------

# 遍历列表
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# 循环 5 次 (从 0 到 4)
for i in range(5):
    print(i)
    
# ----------------------------------------------------------
count = 0
while count < 3:
    print(f"Count is {count}")
    count = count + 1 # 或者 count += 1
```

### 12. 列表/字典生成式

* **列表生成式 (List Comprehension):** 一种简洁的创建列表的方式。

  ```python
  # 创建包含 0 到 9 平方的列表
  squares = [x*x for x in range(10)]
  # squares 会是 [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
  
  # 创建只包含偶数的平方的列表
  even_squares = [x*x for x in range(10) if x % 2 == 0]
  # even_squares 会是 [0, 4, 16, 36, 64]
  ```
* **字典生成式 (Dictionary Comprehension):** 用于快速创建字典。

  ```python
  # 创建数字及其平方的字典
  square_dict = {x: x*x for x in range(5)}
  # square_dict 会是 {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
  ```

---

## 代码示例锦囊 🚀

**1. 字符串操作示例**

```python
# 查找子字符串
my_string = "Hello, Python World!"
position = my_string.find("Python")
print(f"'Python' 在字符串中的位置是: {position}") # 输出: 7

# 替换子字符串
new_string = my_string.replace("World", "Learner")
print(f"替换后的字符串: {new_string}") # 输出: Hello, Python Learner!

# 分割字符串
words = my_string.split(" ") # 按空格分割
print(f"分割后的单词列表: {words}") # 输出: ['Hello,', 'Python', 'World!']

# 去除首尾空格
spaced_string = "   some spaces   "
clean_string = spaced_string.strip()
print(f"去除空格后: '{clean_string}'") # 输出: 'some spaces'
```

**2. 列表操作示例**

```python
# 添加元素
my_list = [1, 2, 3]
my_list.append(4)       # 在末尾添加
print(f"Append后: {my_list}") # 输出: [1, 2, 3, 4]
my_list.insert(1, 99)  # 在索引1的位置插入
print(f"Insert后: {my_list}") # 输出: [1, 99, 2, 3, 4]

# 删除元素
removed_item = my_list.pop(2) # 删除索引2的元素并返回它
print(f"Pop后: {my_list}, 删除的元素: {removed_item}") # 输出: [1, 99, 3, 4], 删除的元素: 2
my_list.remove(4)        # 删除第一个值为4的元素
print(f"Remove后: {my_list}") # 输出: [1, 99, 3]

# 列表排序
unsorted_list = [5, 1, 4, 2, 3]
unsorted_list.sort() # 原地排序（改变原列表）
print(f"Sort后: {unsorted_list}") # 输出: [1, 2, 3, 4, 5]

new_sorted_list = sorted([5, 1, 4, 2, 3], reverse=True) # 返回新列表，降序
print(f"Sorted降序: {new_sorted_list}") # 输出: [5, 4, 3, 2, 1]
```

**3. 字典操作示例**

```python
student = {"name": "小红", "age": 13, "subjects": ["语文", "数学"]}

# 获取所有键
keys = student.keys()
print(f"字典的键: {keys}") # 输出: dict_keys(['name', 'age', 'subjects'])

# 获取所有值
values = student.values()
print(f"字典的值: {values}") # 输出: dict_values(['小红', 13, ['语文', '数学']])

# 获取所有键值对
items = student.items()
print(f"字典的项: {items}") # 输出: dict_items([('name', '小红'), ('age', 13), ('subjects', ['语文', '数学'])])

# 安全地获取值 (如果键不存在，返回None或默认值)
score = student.get("score") # "score"键不存在
print(f"分数: {score}") # 输出: None
default_score = student.get("score", "暂无分数") # 提供默认值
print(f"分数 (带默认值): {default_score}") # 输出: 暂无分数
```

**4. 面向对象编程 (OOP) 示例**

```python
class Cat:
    # 构造函数 (初始化方法)
    def __init__(self, name, color):
        self.name = name      # 公有属性
        self.color = color
        self.__mood = "happy" # 私有属性 (通常不直接在外部访问)

    # 对象的方法 (能做什么)
    def meow(self):
        print(f"{self.name} ({self.color}) says: Meow!")

    def get_mood(self):
        return self.__mood

# 创建对象 (实例化)
cat1 = Cat("咪咪", "橘色")
cat2 = Cat("花花", "白色")

# 调用对象的方法
cat1.meow() # 输出: 咪咪 (橘色) says: Meow!
cat2.meow() # 输出: 花花 (白色) says: Meow!

# 访问公有属性
print(f"{cat1.name} 的颜色是 {cat1.color}") # 输出: 咪咪 的颜色是 橘色

# 访问私有属性 (通过方法间接访问)
print(f"{cat1.name} 现在的心情是: {cat1.get_mood()}") # 输出: 咪咪 现在的心情是: happy

# 尝试直接访问私有属性 (会报错或行为不符合预期)
# print(cat1.__mood) # 这通常会引发 AttributeError
```

**5. 函数与参数示例**

```python
def greet(name, greeting="你好"): # greeting有默认值
    print(f"{greeting}, {name}!")

greet("小明")             # 使用默认问候语: 你好, 小明!
greet("小华", "早上好")   # 指定问候语: 早上好, 小华!
greet(greeting="晚上好", name="小李") # 使用关键字参数: 晚上好, 小李!
```

**6. 异常处理示例**

```python
def safe_divide(a, b):
    try:
        result = a / b
        print(f"{a} / {b} = {result}")
    except ZeroDivisionError:
        print("错误：除数不能为零！")
    except TypeError:
        print("错误：操作数类型不兼容，请确保输入的是数字！")
    finally:
        print("除法尝试结束。")

safe_divide(10, 2)
safe_divide(5, 0)
safe_divide("十", 2)
```

---

## 实战演练场 🎯

**练习1：列表元素计数 (填空)**

```python
def count_even(numbers):
    count = 0
    for num in numbers:
        if num % 2 == ___: # 填空：判断是否为偶数
            count += 1
    return count

my_nums = [1, 2, 3, 4, 5, 6, 7, 8]
print(f"列表中的偶数个数: {count_even(my_nums)}") # 应该输出 4
```

**练习2：字典查找 (改错)**

下面代码想查找字典中'Bob'的年龄，但有错误，请改正。

```python
ages = {'Alice': 30, 'Bob': 25, 'Charlie': 35}

# 错误的代码
# bobs_age = ages[Bob] # 错误1: 变量名? 错误2: 键类型?
# print("Bob's age:", bobs_age)

# 请在这里写出正确的代码

```

**练习3：简单编程 - 计算平均分**

编写一个函数 `calculate_average(scores)`，它接受一个包含分数的列表 `scores` 作为参数，返回这些分数的平均值。如果列表为空，则返回0。

```python
# 在这里定义你的函数
def calculate_average(scores):
    # 你的代码...
    pass # pass是占位符，可以删掉

# 测试你的函数
print(calculate_average([80, 90, 100])) # 应该输出 90.0
print(calculate_average([75, 85]))     # 应该输出 80.0
print(calculate_average([]))           # 应该输出 0
```

**练习4：面向对象 - 创建一个`Book`类**

定义一个 `Book` 类，它有 `title` (书名) 和 `author` (作者) 两个属性。在创建对象时通过构造函数 `__init__` 初始化这两个属性。再添加一个 `display_info` 方法，用于打印书的信息，格式为："书名: [书名], 作者: [作者]"。

```python
# 在这里定义你的Book类
class Book:
    # 你的代码...
    pass

# 创建一个Book对象并测试
my_book = Book("Python入门", "张三")
my_book.display_info() # 应该输出: 书名: Python入门, 作者: 张三
```

**(练习答案提示在手册末尾)**

---

## 难点攻克营 🤔

有些概念可能一开始觉得有点绕，我们再来捋一捋。

*   **`self` 是什么？(OOP)**
    在类的方法定义中（比如 `__init__` 或 `meow`），`self` 总是第一个参数。它代表**对象本身**。

    当你创建一个对象（比如 `cat1 = Cat("咪咪", "橘色")`）并调用它的方法（比如 `cat1.meow()`）时，Python 会自动把这个对象 `cat1` 传递给方法的 `self` 参数。所以，在方法内部，`self.name = name` 就是把传入的 `name` 值赋给 `cat1` 这个对象的 `name` 属性。
    
    
    
*   **私有属性 `__mood` 真的不能访问吗？(OOP)**
    Python 的私有属性（以双下划线开头，且结尾没有双下划线）其实是一种"名称改写"（name mangling）。

    当你定义 `__mood` 时，Python 会偷偷把它改成类似 `_Cat__mood` 的名字。所以，虽然不推荐，但你其实可以通过 `cat1._Cat__mood` 来访问它。设置成私有主要是为了**提醒**使用者："这个属性是内部实现细节，最好不要直接碰它，请使用我提供的公共方法（如 `get_mood()`）来交互"。这有助于保持代码的整洁和稳定。
    
    
    
*   **列表生成式 `[x*x for x in range(10) if x % 2 == 0]` 怎么读？**
    把它拆开看，就像读一个普通的 `for` 循环：
    
    1. `for x in range(10)`: 先看循环部分，意思是对 0 到 9 的每个数字 `x` 进行处理。
    
    2. `if x % 2 == 0`: 接着看条件部分（如果有的话），只有当 `x` 是偶数时，才执行下一步。
    
    3. `x*x`: 最后看表达式部分，对于满足条件的 `x`，计算它的平方 `x*x`。
    
    4. `[...]`: 把所有计算出来的结果放到一个新的列表里。
       所以，这句话连起来就是："对于 0 到 9 中的每一个偶数 `x`，计算它的平方，然后把这些平方值收集到一个新列表里。"
    
       
    
*   **可变类型 vs 不可变类型**
    *   **不可变类型 (Immutable):** 值一旦创建就不能被修改。当你试图"修改"它时，实际上是创建了一个新的对象。常见的有：数字 (int, float), 字符串 (str), 元组 (tuple)。
        ```python
        a = 5
        print(id(a)) # 打印a的内存地址
        a = a + 1    # 看起来是修改了a，实际上是创建了新对象6，让a指向它
        print(id(a)) # 地址变了！
        
        s = "hello"
        print(id(s))
        s = s + " world" # 创建了新字符串 "hello world"
        print(id(s)) # 地址变了！
        ```
    *   **可变类型 (Mutable):** 值创建后可以被修改，修改发生在原地，不会创建新对象。常见的有：列表 (list), 字典 (dict), 集合 (set)。
        ```python
        my_list = [1, 2]
        print(id(my_list))
        my_list.append(3) # 在原列表末尾添加，修改了原对象
        print(id(my_list)) # 地址没变！
        ```

---

## 练习答案提示 🔑

**练习1:** `___` 应填 `0`
**练习2:** 正确代码：`bobs_age = ages["Bob"]` 或 `bobs_age = ages.get("Bob")`。注意键是字符串 `"Bob"`。
**练习3:** 函数内部需要判断列表是否为空，如果不为空，计算 `sum(scores) / len(scores)`。
**练习4:** 需要定义 `__init__(self, title, author)` 来接收并存储 `title` 和 `author` 到 `self.title` 和 `self.author`。`display_info(self)` 方法使用 `print()` 和 f-string 或字符串拼接来输出信息。