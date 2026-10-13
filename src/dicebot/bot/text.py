helptext = """
**Comrade Dicebot** executes the `!roll`, `!distribution` and `!list` directives.

**Rolls**
• `d20`, `8d8`
• Keep highest: `3d20k2`, `4d6k3`
• Individual: `3d6i`

**Operators**
• Math: `+ - * / %`
• Logical: `> < ==`

**Functions**
• `max(a,b,...)` — maximum of a set
• `min(a,b,...)` — minimum of a set
• `fac(a)` — factorial
• `comb(a,b)` — combination
• `any(a,b,c)` — 1 if any argument > 0

**Assignment**
• Macro: `a = 2d20`, `b = d8+3`
• Value: `a &= 2d20`

**Multirolls**
• `d20; d20+7`
• `reroll_1s_d6 = (d6; a &= (a == 1) * d6 + (a > 1) * a; a)`

**Comments**
• `"This is a roll:" d20; "And another one" d100+20`
"""

welcome_text = """
Comrade Dicebot answers to text commands. Deploy !roll and !distribution to roll dice.
The dice belong to the people. For assistance, consult SomaQM.
"""
