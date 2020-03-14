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
        return "%s(%sx%sx%s, weight: %s) pos(%s) rt(%s) vol(%s)" % (
            self.name, self.width, self.height, self.depth, self.weight,
            self.position, self.rotation_type, self.get_volume()
        )

    def get_volume(self):
        return round(self.width * self.height * self.depth, 2)

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
        self.unfitted_items = []

    def string(self):
        return "%s(%sx%sx%s, max_weight:%s) vol(%s)" % (
            self.name, self.width, self.height, self.depth, self.max_weight,
            self.get_volume()
        )

    def get_volume(self):
        return round(self.width * self.height * self.depth, 2)

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

    def pack_to_bin(self, bin, item):
        fitted = False

        if not bin.items:
            response = bin.put_item(item, START_POSITION)

            if not response:
                bin.unfitted_items.append(item)

            return None

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

                if bin.put_item(item, pv):
                    fitted = True
                    break

        if not fitted:
            bin.unfitted_items.append(item)

    def pack(self, bigger_first=False, distribute_items=False):
        self.bins.sort(key=lambda x: x.get_volume(), reverse=bigger_first)
        self.items.sort(key=lambda x: x.get_volume(), reverse=bigger_first)

        for bin in self.bins:
            for item in self.items:
                self.pack_to_bin(bin, item)

            if distribute_items:
                for item in bin.items:
                    self.items.remove(item)


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
