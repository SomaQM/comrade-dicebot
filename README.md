# Comrade Dicebot ☭

*You have nothing to roll but your dice!*

A dice-rolling bot for the proletariat. Built for an ongoing RPG campaign and shared freely with any comrade who wants it.

## Capabilities ✨

- **Flexible dice rolling:** Supports standard and custom dice notations, including complex expressions like `d8+3` or `max(d20, d20) + 8`.
- **Individual dice results:** Append `i` to any roll to see each die separately rather than the sum.
- **Probability distributions:** Visualize roll distributions to understand outcome probabilities before committing to a roll.
- **Text directives:** Every action is a text command. No ceremony, no GUI.
- **Macro management:** Create and manage roll macros for quick access to frequently used rolls.
- **Statistics tracking:** The collective remembers every die that has been rolled, and can report on them by user, server, or globally.

## Directives 📖

Once Comrade Kostyr has joined your server, the following directives are available:

| Directive | Purpose |
|---|---|
| `!roll [expression]` | Execute a roll |
| `!distribution [expression]` | Plot the probability distribution of an expression |
| `!list` | List your saved macros |
| `!unset [macro]` | Remove a saved macro |
| `!stats [scope] [die] [timespan]` | Report roll statistics (`scope` is `global`, `guild`, or `user`; `timespan` is `day`, `week`, or `month`) |
| `!help` | Display the full directive reference |

### Examples of Roll Expressions

- **Basic Rolls:**
  - `d20`: Roll a 20-sided die.
  - `8d8`: Roll eight 8-sided dice.

- **Individual Dice:**
  - `3d6i`: Roll three 6-sided dice and report each: `[4, 6, 1]`.
  - `d20i`: A single 20-sided die, reported as `[17]`.
  - `3d6i + 3`: Roll three dice, add 3 to each: `[7, 9, 4]`.
  - `3d6i * 2`: Roll three dice and double each result.
  - `2d6i + 3d6i`: Element-wise addition of two rolls of equal size.

  Note: `i` is a terminal suffix and cannot be combined with the keep (`k`, `kl`), reroll (`rr`), or explode (`!`) modifiers. Those take priority.

- **Keep Highest Rolls:**
  - `3d20k2`: Roll three 20-sided dice and keep the highest two.
  - `4d6k3`: Roll four 6-sided dice and keep the highest three.

- **Math Operations:**
  - `d20 + 5`: Roll a 20-sided die and add 5.
  - `2d10 - 3`: Roll two 10-sided dice and subtract 3.

- **Logical Operations:**
  - `d20 > 15`: Roll a 20-sided die and check if the result is greater than 15.
  - `2d6 == 7`: Roll two 6-sided dice and check if the sum equals 7.

- **Functions:**
  - `max(d20, d12)`: Roll a 20-sided die and a 12-sided die, and take the maximum.
  - `min(d10, d8)`: Roll a 10-sided die and an 8-sided die, and take the minimum.
  - `fac(5)`: Compute the factorial of 5.
  - `comb(5, 2)`: Compute the combination of 5 choose 2.
  - `any(d6-3, d6-3, d6-3)`: Roll three 6-sided dice and return 1 if any result is greater than 0.

- **Assignments:**
  - `a = 2d20`: Assign the result of rolling two 20-sided dice to variable `a`.
  - `b = d8 + 3`: Assign the result of rolling an 8-sided die plus 3 to variable `b`.
  - `a &= 2d20`: Compute the result of rolling two 20-sided dice and assign it to variable `a`.

  Macro assignments (`=`) reroll their contained dice each time they are referenced. Value assignments (`&=`) compute once and store the result.

- **Multi-Rolls:**
  - `d20; d20 + 7`: Roll a 20-sided die, then roll another 20-sided die and add 7.
  - `reroll_1s_d6 = (d6; a &= (a == 1) * d6 + (a > 1) * a; a)`: Roll a 6-sided die, and if the result is 1, reroll it.

- **Comments:**
  - `"This is a roll:" d20; "And another one" d100 + 20`: Add comments to your roll expressions.

## Joining the Collective 🤝

Contributions are welcome from all comrades. To get started:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/YourFeature`
3. Commit your changes: `git commit -m 'Add YourFeature'`
4. Push to the branch: `git push origin feature/YourFeature`
5. Open a pull request.

All contributions to the cause are valued equally.

## License 📄

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements 🙏

Special thanks to all contributors and the open-source community for their invaluable support.