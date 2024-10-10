A `cli` that helps you manage your commands.

## Design

Basically, `carefree-cli` aims to help you when:

- you need to run lots of (`cli` / `bash`) commands everyday.
- these commands can be divided into several groups, and commands in each group are highly repetitive.

So the implementation of `carefree-cli` is very simple:

- It will prompt you to create (`cli` / `bash`) command templates and manage them in hierarchical structures.
- It will prompt you to 'fill' the template with your own parameters when you want to run a command.
- It will printed out the final command for you to copy-paste / run.

## Installation

`carefree-cli` requires `python>=3.8`.

```bash
pip install carefree-cli
```

## Basic Workflow

1. Initialize `carefree-cli`:

```bash
cfi init
```

2. Create a command template:

```bash
cfi add -h
```

3. Fill a command template:

```bash
cfi load -h
```

## Common Usages

> Fun fact: you can add `cfi` templates with `carefree-cli` itself!
>
> ```bash
> cfi add 'cfi add \"{template}\" {hierarchy}' cfi_add
> ```

- Get help:

```bash
cfi -h
```

- Install cli completion:

```bash
cfi --install-completion
```

- List templates:

```bash
cfi ls -h
```

## Serializations

- Export templates:

```bash
cfi export
```

- Import templates:

```bash
cfi import -h
```

## Documentation

An auto-generated documentation is available [here](https://github.com/carefree0910/carefree-cli/blob/main/docs.md).

> ```bash
> typer cfi utils docs --name cfi --output docs.md --title '`carefree-cli`'
> ```
