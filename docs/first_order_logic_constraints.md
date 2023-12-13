# First order logic constraints

Builtin constraints may not be sufficient to cover the large number of use-cases user may encounter. Rather than extending more and more the builtin constraints, ProcessScheduler lets you build your own constraints using logical operators, implications and if-then-else statement between builtin constraints or class attributes.

## Logical operators

Logical operators and (:math:`\wedge`), or (:math:`\lor`), xor (:math:`\oplus`), not (:math:`\lnot`) are provided through the functions :func:`and_`, :func:`or_`, :func:`xor_` and :func:`not_`.

!!! note

	Take care of the trailing underscore character at the end of the function names. They are necessary because :const:`and`, :const:`or`, and :const:`not` are python keywords that cannot be overloaded. This naming convention may conflict with functions from the :mod:`operator` standard module.

Using builtin task constraints in combination with logical operators enables a rich expressivity. Imagine that you need a task :math:`t_1` to NOT start at time 3. At a first glance, you can expect a `TaskDontStartAt` to fit your needs, but it is not available from the builtin constraints library. The solution is to express this constraint in terms of first order logic, and state that you need the rule:

$$\lnot TaskStartAt(t_1, 3)$$

In python, this gives:

```
not_(TaskStartAt(t_1, 3)
```

You can combine/nest any of these operators to express a complex constraint. For example, if you don't want the task to start at 3, and also you don't want it to end at 9, then the rule to implement is:

$$\lnot TaskStartAt(t_1,3) \wedge \lnot TaskEndsAt(t_1, 9)$$

In python:

``` py
and_([not_(TaskStartAt(t_1, 3)),
      not_(TaskEndAt(t_1, 9))])
```

In a more general cas, those logical functions can take both task constraints or tasks attributes. For example, the following assertion is possible :

``` py
problem.add_constraint(t1.start == t_2.end + t_4.duration)
```

## Logical Implication - Conditional expressions

The logical implication ($\implies$) is wrapped by the `Implies` class. It takes two parameters: a condition, that always has to be :const:`True` or :const:`False`, and a list of assertions that are to be implied if the condition is :const:`True`. For example, the following logical implication:

$$t_2.start = 4 \implies TasksEndSynced(t_3, t_4)$$

is written in Python:

``` py
consequence = implies(t_2.start == 4,
                      [TasksEndSynced(t_3, t_4)]
problem.add_constraint(consequence)
```

Finally, an if/then/else statement is available through the function :func:`if_then_else` which takes 3 parameters: a condition and two lists of assertions that applies whether the condition is :const:`True` or :const:`False`.

``` py
ite = if_then_else(t_2.start == 4,  # condition
                   [TasksEndSynced(t_3, t_4)], # if the condition is True
                   [TasksStartSynced(t_3, t_4)]) # if the condition is False
problem.add_constraint(ite)
```

!!! note

    The classes `Implies` and `If_then_else` functions names do not conflict with any other function name from another package, thus dont have any underscore suffix.
