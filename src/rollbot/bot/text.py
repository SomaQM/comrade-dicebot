helptext = """
Comrade Dicebot executes the !roll, !distribution and !list directives.
The collective offers the following capabilities:
    roll examples: d20, 8d8
    keep highest: 3d20k2, 4d6k3
    math operators: +,-,\\*,/,%
    logical operators: >, <, ==
    functions:
        max(a,b,..): take the maximum of a set
        min(a,b,..): take the minimum of a set
        fac(a): compute the factorial
        comb(a,b): compute the combination
        any(a,b,c): return 1 if any argument is > 0
    assignment:
        macro assignment: creates a variable that will reroll contained dice every time it is referenced
            examples: a = 2d20, b=d8+3
        value assignment: compute the result of a diceroll and assign it to a variable.
            examples: a &= 2d20
        multirolls: You can combine multiple actions into one roll and even assign those to macros.
            examples: d20; d20+7
                      reroll_1s_d6 = (d6; a &= (a == 1) * d6 + (a > 1) * a; a)
        comments: You can apply text commentary on statements
            examples: "This is a roll:" d20; "And another one" d100+20
"""

welcome_text = "Comrade Dicebot answers to text commands. Deploy !roll and !distribution to roll dice. The dice belong to the people. For assistance, consult SomaQM."