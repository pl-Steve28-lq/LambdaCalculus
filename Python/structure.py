from utils import Enum, Tuple

SKI = Enum('SKI', 'SKI')
Apply = Tuple('Apply', ['target', 'expr'])
Lambda = Tuple('Lambda', ['arg', 'expr'])
Var = Tuple('Var', ['name'])

def apply(self, arg):
  def check(a):
    if isinstance(a, Var):
      if a.name == self.arg:
        return arg
      return a
    if isinstance(a, Apply):
      target, expr = a.target, a.expr
      flag = 0
      if target == Var(self.arg): flag += 1
      if expr == Var(self.arg): flag += 2
      return (arg if flag%2 else check(target)).apply(arg if flag//2 else check(expr))
    if isinstance(a, Lambda):
      return Lambda(a.arg, check(a.expr))

  return check(self.expr)

def apply2(self, arg):
  return Apply(self, arg)

setattr(Lambda, 'apply', apply)
setattr(Apply, 'apply', apply2)
setattr(Var, 'apply', apply2)
