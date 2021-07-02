import kotlin.collections.Set

sealed class Structure { abstract override fun toString(): String }
class Apply(val target: Structure, val expr: Structure): Structure() {
    fun s(t: Structure) = if (t is Var || t is SKI) "$t" else "($t)"
    override fun toString() = "${s(target)}${s(expr)}"
}
class Var(val name: String): Structure() { override fun toString() = name }
class Lambda(val arg: String, val expr: Structure): Structure() {
    override fun toString() = "λ$arg.$expr"
}

sealed class SKI(val name: String): Structure() { override fun toString() = name }
object S: SKI("S")
object K: SKI("K")
object I: SKI("I")
object Debug: SKI("D")

fun free(x: String, t: Structure): Boolean {
    fun fv(e: Structure): Set<String> = when(e) {
        is Var -> setOf(e.name)
        is Lambda -> fv(e.expr) subtract setOf(e.arg)
        is Apply -> fv(e.target) union fv(e.expr)
        else -> setOf()
    }
    return fv(t).contains(x)
}

fun Structure.toSKI(): Structure = when (this) {
    is Var, is SKI -> this
    is Apply -> Apply(target.toSKI(), expr.toSKI())
    is Lambda -> {
        if (!free(arg, expr)) Apply(K, expr.toSKI())
        else if (expr is Var && expr.name == arg) I
        else if (expr is Lambda && free(arg, expr.expr)) Lambda(arg, expr.toSKI()).toSKI()
        else if (expr is Apply && (
            free(arg, expr.target) || free(arg, expr.expr)
        )) Apply(
            Apply(S, Lambda(arg, expr.target.toSKI()).toSKI()),
            Lambda(arg, expr.expr.toSKI()).toSKI()
        )
        else Debug
    }
}

fun main() {
    val applier: (String) -> Lambda = { q -> Lambda(q, Apply(Var(q), Var(q))) }
    val t = Lambda("x", Apply(Var("f"), applier("x")))
    val f = Lambda("f", Apply(t, t))
    println(f)
    println(f.toSKI())
}
