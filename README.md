3D Bin Packing
====

3D Bin Packing implementation based on [this paper](erick_dube_507-034.pdf). The code is based on [gedex](https://github.com/gedex/bp3d) implementation in Go.

## Features
1. Sorting Bins and Items:
    ```[bigger_first=False/True]``` By default all the bins and items are sorted from the smallest to the biggest, also it can be vice versa, to make the packing in such ordering.
2. Item Distribution:
    - ```[distribute_items=True]``` From a list of bins and items, put the items in the bins that at least one item be in one bin that can be fitted. That is, distribute all the items in all the bins so that they can be contained.
    - ```[distribute_items=False]``` From a list of bins and items, try to put all the items in each bin and in the end it show per bin all the items that was fitted and the items that was not.
3. Number of decimals:
    ```[number_of_decimals=X]``` Define the limits of decimals of the inputs and the outputs. By default is 3.

## Install

```
pip install py3dbp
```

## Basic Explanation

Bin and Items have the same creation params:
```
my_bin = Bin(name, width, height, depth, max_weight)
my_item = Item(name, width, height, depth, weight)
```
Packer have three main functions:
```
packer = Packer()           # PACKER DEFINITION

packer.add_bin(my_bin)      # ADDING BINS TO PACKER
packer.add_item(my_item)    # ADDING ITEMS TO PACKER

packer.pack()               # PACKING - by default (bigger_first=False, distribute_items=False, number_of_decimals=3)
```

After packing:
```
packer.bins                 # GET ALL BINS OF PACKER
my_bin.items                # GET ALL FITTED ITEMS IN EACH BIN
my_bin.unfitted_items       # GET ALL UNFITTED ITEMS IN EACH BIN
```


## Usage

```
from py3dbp import Packer, Bin, Item

packer = Packer()

packer.add_bin(Bin('small-envelope', 11.5, 6.125, 0.25, 10))
packer.add_bin(Bin('large-envelope', 15.0, 12.0, 0.75, 15))
packer.add_bin(Bin('small-box', 8.625, 5.375, 1.625, 70.0))
packer.add_bin(Bin('medium-box', 11.0, 8.5, 5.5, 70.0))
packer.add_bin(Bin('medium-2-box', 13.625, 11.875, 3.375, 70.0))
packer.add_bin(Bin('large-box', 12.0, 12.0, 5.5, 70.0))
packer.add_bin(Bin('large-2-box', 23.6875, 11.75, 3.0, 70.0))

packer.add_item(Item('50g [powder 1]', 3.9370, 1.9685, 1.9685, 1))
packer.add_item(Item('50g [powder 2]', 3.9370, 1.9685, 1.9685, 2))
packer.add_item(Item('50g [powder 3]', 3.9370, 1.9685, 1.9685, 3))
packer.add_item(Item('250g [powder 4]', 7.8740, 3.9370, 1.9685, 4))
packer.add_item(Item('250g [powder 5]', 7.8740, 3.9370, 1.9685, 5))
packer.add_item(Item('250g [powder 6]', 7.8740, 3.9370, 1.9685, 6))
packer.add_item(Item('250g [powder 7]', 7.8740, 3.9370, 1.9685, 7))
packer.add_item(Item('250g [powder 8]', 7.8740, 3.9370, 1.9685, 8))
packer.add_item(Item('250g [powder 9]', 7.8740, 3.9370, 1.9685, 9))

packer.pack()

for b in packer.bins:
    print(":::::::::::", b.string())

    print("FITTED ITEMS:")
    for item in b.items:
        print("====> ", item.string())

    print("UNFITTED ITEMS:")
    for item in b.unfitted_items:
        print("====> ", item.string())

    print("***************************************************")
    print("***************************************************")

```

## Latest Stable Version
    py3dbp==1.1.2

## Versioning
- **1.x**
    - Two ways to distribute items (all items in all bins - all items in each bin).
    - Get per bin the fitted and unfitted items.
    - Set the limit of decimals of inputs and outputs.
- **0.x**
    - Try to put all items in the first bin that can fit at least one.

## Credit

* https://github.com/bom-d-van/binpacking
* https://github.com/gedex/bp3d
* [Optimizing three-dimensional bin packing through simulation](erick_dube_507-034.pdf)

## License

[MIT](./LICENSE)