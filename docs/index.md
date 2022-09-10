# custom superfence

```prefix prefix="(test)$"
echo "This is a test of the prefix superfence"
```

```prefix prefix="$"
echo "Another test"
```

```prefix prefix="(venv)$"
echo "Last one"
```


# venv superfence

```venv
python3 -m pip install mkdocs  # inside a venv
```