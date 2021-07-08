from utils import Stream
from structure import SKI, Apply, Lambda, Var

# Lambda Calculus
class LC:
  @staticmethod
  def free(x, e):
    """ True if x is free variable in e, else False """
    def fv(x):
      if isinstance(x, Var): return {x}
      if isinstance(x, Apply): return fv(x.target) | fv(x.expr)
      if isinstance(x, Lambda): return fv(x.expr) - {Var(x.arg)}
      return set()
    return Var(x) in fv(e)

  """ Translate Lambda into SKI """
  @staticmethod
  def T(x):
    if isinstance(x, Var) or SKI.check(x): return x
    if isinstance(x, Apply): return LC.T(x.target).apply(LC.T(x.expr))
    if isinstance(x, Lambda):
      v, expr = x.arg, x.expr
      if not LC.free(v, expr): return Apply(SKI.K, LC.T(expr))
      if expr == Var(v): return SKI.I
      if isinstance(expr, Lambda):
        if LC.free(v, expr.expr):
          return LC.T(Lambda(v, LC.T(expr)))
      if isinstance(expr, Apply):
        if not LC.free(v, expr.target) and expr.expr == Var(v):
          return LC.T(expr.target)
        if LC.free(v, expr.target) or LC.free(v, expr.expr):
          return Apply(SKI.S, LC.T(Lambda(v, LC.T(expr.target)))).apply(LC.T(Lambda(v, LC.T(expr.expr))))

# Binary Lambda Calculus
class BLC(Stream):
  Instance = None

  def eval(self, code):
    c = self.getChar()
    if c == '1':
      self.next()
      return Apply(self.eval(code), self.eval(code))
    if c == '0':
      self.next()
      s = self.getChar()
      self.next()
      if s == '1': return SKI.S
      if s == '0': return SKI.K

  """ Translate Binary to SKI """
  @staticmethod
  def evaluate(code):
    if BLC.Instance == None:
      BLC.Instance = BLC()
    inst = BLC.Instance
    inst.start(code)
    return inst.eval(code)

# SKI Combinatory
class SKIC:

  """ Translate SKI to Lambda """
  @staticmethod
  def evaluate(x):
    if x == SKI.I: return Lambda('x', Var('x'))
    if x == SKI.K: return Lambda('x', Lambda('y', Var('x')))
    if x == SKI.S:
      return Lambda('x', Lambda('y', Lambda('z', Apply(Apply(Var('x'), Var('z')), Apply(Var('y'), Var('z'))))))
    if isinstance(x, Apply):
      t, s = x.target, x.expr
      return SKIC.evaluate(t).apply(SKIC.evaluate(s))
