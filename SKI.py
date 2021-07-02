from collections import namedtuple

L = type('L', (namedtuple('_L', 'var expr'),), {
  '__repr__': lambda self: f'λ{self.var}.{self.expr}'
})
Apply = type('Apply', (namedtuple('_Apply', 'target expr'),), {
  's': lambda self, x: str(x) if isinstance(x, (Var, CL)) else f'({x})',
  '__repr__': lambda self: f'{self.s(self.target)}{self.s(self.expr)}'
})
Var = type('Var', (namedtuple('_Var', 'name'),), {
  '__hash__': lambda self: hash(self.name),
  '__repr__': lambda self: self.name
})
CL = namedtuple('CL', 'name')
setattr(CL, '__repr__', lambda self: self.name)
S = CL('S')
K = CL('K')
I = CL('I')

def free(x, e):
  def fv(x):
    if isinstance(x, Var): return {x}
    if isinstance(x, Apply): return fv(x.target) | fv(x.expr)
    if isinstance(x, L): return fv(x.expr) - {Var(x.var)}
    return set()
  return Var(x) in fv(e)

def T(x):
  if isinstance(x, (Var, CL)): return x
  if isinstance(x, Apply): return Apply(T(x.target), T(x.expr))
  if isinstance(x, L):
    v, expr = x.var, x.expr
    if not free(v, expr): return Apply(K, T(expr))
    if expr == Var(v): return I
    if isinstance(expr, L) and free(v, expr.expr):
      return T(L(v, T(expr)))
    if isinstance(expr, Apply) and (free(v, expr.target) or free(v, expr.expr)):
      print(L(v, T(expr.target)), L(v, T(expr.expr)))
      return Apply(
        Apply(S, T(L(v, T(expr.target)))),
        T(L(v, T(expr.expr)))
      )

W = lambda q: Apply(Var(q), Var(q))
F = L('x', Apply(Var('f'), W('x')))
a = L('f', Apply(L('t', W('t')), F))
print(a)
print(T(a))
