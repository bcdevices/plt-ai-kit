# Skills

Model-invoked skills packaged with this plugin. Each skill is a subdirectory containing a `SKILL.md` with YAML frontmatter and instructions:

```
skills/
  my-skill/
    SKILL.md
    references/       # optional supporting files the skill loads on demand
    scripts/          # optional supporting scripts
```

`SKILL.md` frontmatter:

```markdown
---
name: my-skill
description: What the skill does AND when to use it. Coding agent reads this to decide whether to load the skill.
---

Instructions the model follows once loaded.
```
