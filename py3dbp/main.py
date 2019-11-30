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
        self, name, width, height, depth, weight, rotation_type=0,
        position=START_POSITION
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
    def __init__(self, name, width, height, depth, max_weight):
        self.name = name
        self.width = width
        self.height = height
        self.depth = depth
        self.max_weight = max_weight
        self.items = []

    def string(self):
        return "%s(%sx%sx%s, max_weight:%s)" % (
            self.name, self.width, self.height, self.depth, self.max_weight
        )

    def get_volume(self):
        return self.width * self.height * self.depth

    def get_total_weight(self):
        total_weight = 0
        for item in self.items:
            total_weight += item.weight

        return total_weight

    def put_item(self, item, pivot):
        fit = False
        valid_item_position = item.position
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
                if self.get_total_weight() + item.weight > self.max_weight:
                    fit = False
                    return fit
                self.items.append(item)

            if not fit:
                item.position = valid_item_position
            return fit

        if not fit:
            item.position = valid_item_position

        return fit


class Packer:
    def __init__(self):
        self.bins = []
        self.items = []
        self.unfit_items = []
        self.total_items = 0

    def add_bin(self, bin):
        return self.bins.append(bin)

    def add_item(self, item):
        self.total_items = len(self.items) + 1
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
            for pt in range(0, len(Axis.ALL)):
                for ib in bin.items:
                    pv = [0, 0, 0]
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

    def pack(self, bigger_first=False):
        self.bins.sort(key=lambda x: x.get_volume(), reverse=bigger_first)
        self.items.sort(key=lambda x: x.get_volume(), reverse=bigger_first)

        while len(self.items) > 0:
            bin = self.find_fitted_bin(self.items[0])
            if bin is None:
                self.unfit_item()
                continue

            self.items = self.pack_to_bin(bin, self.items)

        return None

    def fitted_all(self):
        result = []
        for b in self.bins:
            result.append(True if len(b.items) == self.total_items else False)

        return result


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
