# # The item structure
# item = {
#     "name": "item 1",  # string
#     "width": 20.5,  # float
#     "height": 20.5,  # float
#     "depth": 20.5,  # float
#     "weight": 20.5,  # float
#     "rotationType": 1,  # integer
#     "position": []  # array floats
# }

# # The bin structure
# bin = {
#     "name": "item 2",  # string
#     "width": 50.5,  # float
#     "height": 30.5,  # float
#     "depth": 20.5,  # float
#     "max_weight": 40.5,  # float
#     "items": []  # array objects
# }


class RotationType:
    RT_WHD = 0
    RT_HWD = 1
    RT_HDW = 2
    RT_DHW = 3
    RT_DWH = 4
    RT_WDH = 5

    ALL = [RT_WHD, RT_HWD, RT_HDW, RT_DHW, RT_DWH, RT_WDH]


class Axis:
    WIDTH = 0
    HEIGHT = 1
    DEPTH = 2

    ALL = [WIDTH, HEIGHT, DEPTH]


START_POSITION = [0, 0, 0]


class Item:
    def __init__(
        self, name, width, height, depth, weight, rotation_type, position
    ):
        self.name = name
        self.width = width
        self.height = height
        self.depth = depth
        self.weight = weight
        self.rotation_type = rotation_type
        self.position = position

    def string(self):
        return "%s(%sx%sx%s, weight: %s) pos(%s) rt(%s)" % (
            self.name, self.width, self.height, self.depth, self.weight,
            self.position, self.rotation_type
        )

    def get_volume(self):
        return self.width * self.height * self.depth

    def get_dimension(self):
        if self.rotation_type == RotationType.RT_WHD:
            d = [self.width, self.height, self.depth]
        elif self.rotation_type == RotationType.RT_HWD:
            d = [self.height, self.width, self.depth]
        elif self.rotation_type == RotationType.RT_HDW:
            d = [self.height, self.depth, self.width]
        elif self.rotation_type == RotationType.RT_DHW:
            d = [self.depth, self.height, self.width]
        elif self.rotation_type == RotationType.RT_DWH:
            d = [self.depth, self.width, self.height]
        elif self.rotation_type == RotationType.RT_WDH:
            d = [self.width, self.depth, self.height]
        else:
            d = []

        return d


class Bin:
    def __init__(self, name, width, height, depth, max_weight, items=[]):
        self.name = name
        self.width = width
        self.height = height
        self.depth = depth
        self.max_weight = max_weight
        self.items = items

    def string(self):
        return "%s(%sx%sx%s, max_weight:%s)" % (
            self.name, self.width, self.height, self.depth, self.max_weight
        )

    def get_volume(self):
        return self.width * self.height * self.depth

    def put_item(self, item, pivot):
        fit = False
        item.position = pivot
        for i in range(0, len(RotationType.ALL)):
            item.rotation_type = i
            d = item.get_dimension()
            if (
                self.width < pivot[0]+d[0] or
                self.height < pivot[1]+d[1] or
                self.depth < pivot[2]+d[2]
            ):
                continue

            fit = True

            for ib in self.items:
                if intersect(ib, item):
                    fit = False
                    break

            if fit:
                self.items.append(item)

            return fit

        return fit


class Packer:
    def __init__(self, bins=[], items=[], unfit_items=[]):
        self.bins = bins
        self.items = items
        self.unfit_items = unfit_items

    def add_bin(self, bin):
        return self.bins.append(bin)

    def add_item(self, item):
        return self.items.append(item)

    def unfit_item(self):
        if len(self.items) == 0:
            return
        self.unfit_items.append(self.items[0])
        self.items = self.items[1:]

    def find_fitted_bin(self, item):
        for b in self.bins:
            if not b.put_item(item, START_POSITION):
                continue
            if len(b.items) == 1 and b.items[0] == item:
                b.items = []

            return b

        return None

    def get_bigger_bin_than(self, bin):
        v = bin.get_volume()
        for bin2 in self.bins:
            if bin2.get_volume() > v:
                return bin2

        return None

    def pack_to_bin(self, bin, items):
        unpacked = []
        fitted = bin.put_item(items[0], START_POSITION)
        if not fitted:
            bin2 = self.get_bigger_bin_than(bin)
            if bin2 is not None:
                return self.pack_to_bin(bin2, items)
            return self.items

        for i in items[1:]:
            for pt in range(0, 3):
                for ib in bin.items:
                    if pt == Axis.WIDTH:
                        pv = [
                            ib.position[0] + ib.width,
                            ib.position[1],
                            ib.position[2]
                        ]
                    elif pt == Axis.HEIGHT:
                        pv = [
                            ib.position[0],
                            ib.position[1] + ib.height,
                            ib.position[2]
                        ]
                    elif pt == Axis.DEPTH:
                        pv = [
                            ib.position[0],
                            ib.position[1],
                            ib.position[2] + ib.depth
                        ]
                    else:
                        pv = [0, 0, 0]

                    if bin.put_item(i, pv):
                        fitted = True
                        break

            if not fitted:
                bin2 = self.get_bigger_bin_than(bin)
                while bin2 is not None:
                    left = self.pack_to_bin(bin2, bin2.items.append(i))
                    if len(left) == 0:
                        bin = bin2
                        fitted = True
                        break
                    bin2 = self.get_bigger_bin_than(bin)

                if not fitted:
                    unpacked.append(i)

        return unpacked

    def pack(self):
        self.bins.sort(key=lambda x: x.get_volume(), reverse=True)
        self.items.sort(key=lambda x: x.get_volume(), reverse=True)

        while len(self.items) > 0:
            bin = self.find_fitted_bin(self.items[0])
            if bin is None:
                self.unfit_item()
                continue

            self.items = self.pack_to_bin(bin, self.items)

        return None


def rect_intersect(item1, item2, x, y):
    d1 = item1.get_dimension()
    d2 = item2.get_dimension()

    cx1 = item1.position[x] + d1[x]/2
    cy1 = item1.position[y] + d1[y]/2
    cx2 = item2.position[x] + d2[x]/2
    cy2 = item2.position[y] + d2[y]/2

    ix = max(cx1, cx2) - min(cx1, cx2)
    iy = max(cy1, cy2) - min(cy1, cy2)

    return ix < (d1[x]+d2[x])/2 and iy < (d1[y]+d2[y])/2


def intersect(item1, item2):
    return (
        rect_intersect(item1, item2, Axis.WIDTH, Axis.HEIGHT) and
        rect_intersect(item1, item2, Axis.HEIGHT, Axis.DEPTH) and
        rect_intersect(item1, item2, Axis.WIDTH, Axis.DEPTH)
    )
