3D Bin Packing
====

3D Bin Packing implementation based on [this paper](http://www.cs.ukzn.ac.za/publications/erick_dube_507-034.pdf). The code is based on [gedex](https://github.com/gedex/bp3d) implementation in Go.

## Install

```
pip install py3dbp
```

## Usage

```
from main import Packer, Bin, Item

# Create the new packer
packer = Packer()

# Add the bins
packer.add_bin(Bin("Small Bin", 15, 15, 15, 10))

# Add the items
packer.add_item(Item("Item 1", 8, 15, 10, 20))
packer.add_item(Item("Item 2", 9, 10, 15, 20))

# Pack the items into de bins
packer.pack()

# Iterate the bins to show the items that contains
for b in packer.bins:
    print(b.string())
    for i in b.items:
        print("====> ", i.string())

```

## Credit

* http://www.cs.ukzn.ac.za/publications/erick_dube_507-034.pdf
* https://github.com/bom-d-van/binpacking
* https://github.com/gedex/bp3d

## License

[MIT](./LICENSE)