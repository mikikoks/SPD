# pr1

first program

### Usage

```
python3 pr1.py [-f FILENAME]
```

example:

```
python3 pr1.py -f data/data0.txt
```

to get help:
```
python3 pr1.py -h
```

## example how c_max works

    -------------
    cmax example: 
    -------------
    on data/data1.txt
    p = [1, 2, 3, 4, 5]

    p=1:
        time_unit[0] = 4
        time_unit[1] = 4    (if returns true)
        time_unit[1] = 9

    p=2 
        time_unit[0] = 8
        time_unit[1] = 10

    p=3 
        time_unit[0] = 18
        time_unit[1] = 18   (if returns true)
        time_unit[1] = 22

    p=4 
        time_unit[0] = 24
        time_unit[1] = 24   (if returns true)
        time_unit[1] = 34

    p=5 
        time_unit[0] = 26
        time_unit[1] = 37

    max(time_unit) = 37

### Authors

* jmacek
* mgromadz
