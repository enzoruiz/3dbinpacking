from main import Packer, Bin, Item

packer = Packer()

packer.add_bin(Bin("Small Bin", 15, 15, 15, 10))

packer.add_item(Item("Item 1", 8, 15, 10, 20, 0, [0, 0, 0]))
packer.add_item(Item("Item 2", 9, 10, 15, 20, 0, [0, 0, 0]))

packer.pack()

for b in packer.bins:
    print(b.string())
    for i in b.items:
        print("====> ", i.string())
