# more_termcolor

- Pass any number of colors, color-codes, or attributes
- All standard, background, bright, or attribute codes are available (or any combination of them)
- If found, handles existing colors in the `text` arg as to allow the surrounding, adding or combining of colors dynamically and automatically
- Convenience methods that expose shortcuts to common values (`bold('foo')`, `yellow('bar')` etc)
- 100% compatible with the classic `termcolor` lib: anything that works with `termcolor` works the same with `more_termcolor` 

## Example
```python
from more_termcolor import cprint
cprint('some text', 'red', 'on bright black', 'bold', 'italic')

# This is also possible:
from more_termcolor.colors import bold, brightred
bold_text = bold('text')
fancy = brightred(f'this whole string, including this {bold_text} is bright red')
```

## Roadmap
- Parse complex `color` args, such as:
```python
cprint('foo', 'bold red on bright blue')
``` 
- `pygments`-like support for pseudo HTML tags, e.g.: 
```python
cprint("<black>some text<on white>that examplifies</on white>what's <bold>planned</bold></black>") 
```
- Custom tags:
```python
cprint("<r>some text</r>", r='red') 
``` 

