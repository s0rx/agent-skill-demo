---
name: roll-dice
description: Roll dice using a random number generator. Use when asked to roll a die (d6, d20, etc.), roll dice, or generate a random dice roll.
---

To roll a die, use one of these commands to generate a random integer from
1 to the given number of sides.

Use the Bash command in a bash-compatible shell:

```bash
echo $((RANDOM % <sides> + 1))
```

Or use the PowerShell command in PowerShell:

```powershell
Get-Random -Minimum 1 -Maximum (<sides> + 1)
```

Replace `<sides>` with a positive integer number of sides, such as 6 for a
standard die or 20 for a d20.
