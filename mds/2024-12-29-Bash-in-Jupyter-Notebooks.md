# Bash in Jupyter Notebooks

## Variables


```bash
%%bash
name="Uma"
echo "Hi $name"
echo "Note: it's safer to quote variables like ${name}"
```


```bash
%%bash
echo "${name}"
```

`!` is like `%%bash` for one-line commands:


```python
!name="Daniel"; echo "Hi ${name}"
```


```python
!echo "Hi ${name}"
```

Variables don't persist across cells, for `%%bash` or `!`. Each cell's commands run in its own subshell.

## Constants


```bash
%%bash
readonly UMA="the sweetest"
echo "Uma is ${UMA}"
```

## Control Flow


```bash
%%bash
a=5
b=4
if [ "$a" -eq "$b" ]; then
    echo "Equal"
elif [ "$a" -gt "$b" ]; then
    echo "Greater"
else
    echo "Less"
fi
```


```bash
%%bash
for i in {1..5}; do
    echo $i
done
```


```bash
%%bash
count=2
while [ $count -lt 5 ]; do
    echo $count
    ((count++))
done
```

## Functions


```bash
%%bash
greet() {
    echo "Hello $1"  # $1 is first argument
    return 0
}
greet "Uma the cutie"
```

## Arrays


```bash
%%bash
fruits=("apple" "banana" "orange")
echo "First fruit: ${fruits[0]}"
echo "All fruits: ${fruits[@]}"
```
