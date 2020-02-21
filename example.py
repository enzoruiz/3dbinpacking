from py3dbp import Packer, Bin, Item

packer = Packer()

packer.add_bin(Bin("Small Bin 1", 15, 15, 15, 100))
packer.add_bin(Bin("Small Bin 2", 15, 15, 15, 100))

packer.add_item(Item("Item 1", 8, 15, 10, 20))
packer.add_item(Item("Item 2", 9, 10, 15, 20))

packer.pack()

for b in packer.bins:
    print(b.string())
    for i in b.items:
        print("====> ", i.string())
if packer.unfit_items:
    print('Unfit items')
    for b in packer.unfit_items:
        print("====> ", b.string())
