class Stream:
  def start(self, code):
    self.code = code
    self.idx = 0
  
  def getChar(self):
    return self.code[self.idx]

  def next(self):
    self.idx += 1

class EnumObject:
  def __init__(self, enum, name):
    self.enum = enum
    self.name = name

  def __eq__(self, other):
    if type(self) != type(other): return False
    return self.enum == other.enum and self.name == other.name

  def __str__(self):
    return self.name

  def __repr__(self): return str(self)

def Enum(name, x):
  return type(name, (), {
    i : EnumObject(name, i) for i in x
  } | {'check' : staticmethod(lambda x: getattr(x, 'enum', None) == name)})

def Tuple(name, x):
  def init(self, *args):
    for i in range(len(args)):
      setattr(self, self.x[i], args[i])
      
  def strl(self):
    arg = ', '.join([f'{i}={getattr(self, i)}' for i in self.x])
    return f'{self.type}({arg})'

  def eq(self, other):
    return all([getattr(self, i) == getattr(other, i, None) for i in self.x])

  def hashl(self):
    return hash(tuple(map(lambda x: getattr(self, x), self.x)))
  
  return type(name, (), {
    'type': name, 'x': x,
    '__init__': init, '__str__': strl, '__repr__': strl,
    '__eq__': eq, '__hash__': hashl
  })
    
