# custom superfence

## general custom prefix

```bash prefix="pi@raspberrypi"
echo "This is a test of the custom prefix superfence"
```

## dollar superfence

```bash dollar title="Dollar superfence"
echo "Another test"
```

## venv superfence

```py venv
python3 -m pip install mkdocs  # (1)
```

1. inside a venv

# hash superfence

```bash hash
echo "Last one"
```


## Normal superfence

```bash title="This is a simple code fence"
print("Test")  # (1)
```

1. This is a test
