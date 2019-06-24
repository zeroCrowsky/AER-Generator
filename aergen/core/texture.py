import random as rdm
import numpy  as np
import copy   as cp


class Shape(object):
    '''
        Collection de méthodes statiques permettant de créer des formes
    '''
    @staticmethod
    def empty(width, height):
        return [[False]*width for x in range(height)]

    @staticmethod
    def point(x, y, width=1, height=1):
        pt = Shape.empty(width, height)
        pt[y][x] = True
        return pt

    @staticmethod
    def rectangle(width, height, fill=True):
        shape = [[fill]*width for x in range(height)]
        if not fill:
            for x in range(width):
                shape[0][x] = True
                shape[height-1][x] = True

            for y in range(height):
                shape[y][0] = True
                shape[y][width] = True
        return shape

    @staticmethod
    def circle(radius, fill=True, angle=360.0):
        shape = [[False]*(radius*2) for x in range(radius*2)]

        n = 4 * radius
        step = angle / n
        for i in range(n):
            theta = i * step
            x = radius + cos(theta) * radius
            y = radius + sin(theta) * radius
            shape[x][y] = True

            if not fill:
                continue

            if x > radius:
                begin = radius
                end = x
            else:
                begin = x + 1
                end = radius

            for xx in range(begin, end):
                shape[xx][y] = True
        return shape

    @staticmethod
    def hline(size):
        return [True] * size

    @staticmethod
    def vline(size):
        return [[True] for x in range(size)]

    @staticmethod
    def diagbt_line(size):
        shape = [[False]*size for x in range(size)]
        n = size-1
        for xy in range(size):
            shape[n-xy][xy] = True
        return shape

    @staticmethod
    def diagtb_line(size):
        shape = [[False]*size for x in range(size)]
        for xy in range(size):
            shape[xy][xy] = True
        return shape

    @staticmethod
    def random(p, width, height=None):
        height = width if height is None else height
        shape = [[False]*width for x in range(height)]

        for x in range(width):
            for y in range(height):
                if np.random.uniform(0, 1) < p:
                    shape[y][x] = True

        return shape

    @staticmethod
    def fromfile(filename, ishape=0):
        shape = []
        with open(filename, 'r') as f:
            i = 0
            for line in f:
                if i > ishape:
                    break

                if i == ishape:
                    line = line[:-1] if line[-1] == '\n' else line  
                    row = list(map(lambda x: x == '1', line))
                    shape.append(row)

                if line.startswith('#'):
                    i += 1
                    continue
            
        return shape


    def fromfolder(foldername):
        # TODO
        return

    @staticmethod
    def savefile(shape, filename, append=True):
        shape_str = Shape.tostr(shape, with_dim=False)
        mode = 'a' if append else 'w'
        with open(filename, mode) as f:
            f.write(shape_str)
            f.write('#\n')
        return

    @staticmethod
    def tostr(shape, with_dim=True):
        W, H = Shape.dimension(shape)
        header = str(W) + ' ' + str(H) + '\n' if with_dim else ''
        body = ''
        for y in range(H):
            body += ''.join(list(map(lambda x: '1' if x else '0', shape[y]))) + '\n'

        return header + body

    @staticmethod
    def totuple(shape):
        return tuple([tuple(row) for row in shape])

    @staticmethod
    def tolist(shape):
        return [list(row) for row in item]

    @staticmethod
    def dimension(shape):
        return len(shape[0]), len(shape)

    @staticmethod
    def count_pixel_on(shape):
        result = 0
        w, h = Shape.dimension(shape)
        for y in range(h):
            for x in range(w):
                result += shape[y][x]
        return result

    @staticmethod
    def sort_shape_by_npixel_on(shapes, npixel_on_max=None):
        shps_npxl_on = list(map)

        if npixel_on_max is None:
            pass



    @staticmethod
    def merge(shp1, shp2):
        width = min(len(shp1[0]), len(shp2[0]))
        height = min(len(shp1), len(shp2))
        shape = [[False] * width for _ in range(height)]

        for x in range(width):
            for y in range(height):
                shape[y][x] = shp1[y][x] or shp2[y][x]

        return shape

    @staticmethod
    def all_shapes_cvx(width, height, size=None):
        size = width * height - 1 if size is None else size

        x, y = width // 2, height // 2
        lst_shps = [(Shape.point(x, y, width, height), (x,y))]
        all_shps = []
        n = min(width, height)

        for i in range(2, n+1):
            aux = []
            for j in range(len(lst_shps)):
                shp, (x, y) = lst_shps[j]
                positions = [ ((x+1) % width, y), ((x+1) % width, (y+1) % height), # EAST, SOUTH-EAST
                              (x, (y+1) % height), ((x-1) % width, (y+1) % height) # SOUTH, SOUTH-WEST
                            ]

                for x, y in positions:
                    shp_mut = [list(r) for r in shp]
                    shp_mut[y][x] = True
                    item = shp_mut, (x, y)
                    aux.append(item)
                    all_shps.append(shp_mut)
            lst_shps = aux

        return all_shps

    @staticmethod
    def merge_strategy(shapes, retset=False):
        shps_merged_set = set(map(Shape.totuple, shapes))
        shps_merged = []
        nshape = len(shapes)
        for i in range(nshape-1):
            shp_i0 = shapes[i]
            shp_i1 = shapes[i+1]

            shp = Shape.merge(shp_i0, shp_i1)
            shp = Shape.totuple(shp)

            n = len(shps_merged_set)
            shps_merged_set.add(shp)
            if n < len(shps_merged_set): # new shape
                shps_merged.append(shp)

        if retset:
            return shps_merged, shps_merged_set
        return shps_merged



    @staticmethod
    def all_shapes(width, height, size=None):
        size = width * height - 1 if size is None else size

        all_shps = set()
        lst_shps = [Shape.empty(width, height)]

        for i in range(size):
            aux = []
            for j in range(len(lst_shps)):
                for k in range(width * height):
                    item = lst_shps[j]
                    x, y = k % width, k // width
                    if item[y][x]:
                        continue
                    # Create item
                    item = [list(r) for r in item]
                    item[y][x] = True
                    # Transform tuple
                    item = tuple([tuple(r) for r in item])

                    if item not in all_shps:
                        all_shps.add(item)
                        aux.append(item)
            lst_shps = aux

        return all_shps



    @staticmethod
    def print_shapes(shapes, ncol=4, sepcol='   ', seprow='\n'):
        nshape = len(shapes)
        rshape = len(shapes[0])
        cshape = len(shapes[0][0])
        ncol = min(ncol, nshape)

        for i in range(0, nshape, ncol):
            for r in range(rshape):
                line = ''
                for s in range(i, min(i+ncol, nshape)):
                    for c in range(cshape):
                        line += str(int(shapes[s][r][c]))
                    line += sepcol
                print(line)
            print(seprow, end='')


class Texture(object):
    def __init__(self, x, y, env=None):
        self.position = np.array([x, y])
        self.env = env
        return

    def __deepcopy__(self, memo):
        cls = self.__class__
        res = cls.__new__(cls)
        res.position = np.copy(self.position)
        res.env = self.env
        return res

    def __str__(self):
        return str(self.position[0]) + ' ' + str(self.position[1])

    def parse(self, s):
        x, y = list(map(int, s.split(' ')))
        self.position = np.array([x, y])


class EntityTexture(object):
    def __init__(self, x, y, shape=[[[]]], shape_id=0, env=None):
        self.position = np.array([x, y])
        self.env = env

        # Attribut private
        if isinstance(shape[0][0], bool):
            self.__shape = [shape]
        else:
            self.__shape = shape

        self.shape_id = shape_id

        return

    @property
    def shape(self):
        return self.__shape[self.shape_id]


    def __str__(self):
        header = Texture.__str__(self) + ' ' + str(self.shape_id) + ' ' + str(len(self.__shape)) + '\n'
        body = ''
        for shape in self.__shape:
            body += Shape.tostr(shape)

        return header + body

    def __deepcopy__(self, memo):
        res = Texture.__deepcopy__(self, memo)
        res.shape = cp.deepcopy(self.shape)
        return res

    def move(self, dir, mvt, time, no_move=True):
        if no_move and mvt == 0:
            return False
        pos = self.position + dir.direction * mvt
        return self.env.put(self, pos, time)

    def parse(self, s):
        lines = s.split('\n')
        i = 0
        x, y, s_id, s_n = list(map(int, lines[i].split(' '))); i += 1
        shapes = []

        for j in range(s_n):
            shape = []
            W, H = list(map(int, lines[i].split(' '))); i += 1

            for l in range(i, i+H):
                row = list(map(lambda x: x == '1', lines[l]))
                shape.append(row)
            i += H
            shapes.append(shape)

        self.shape_id = s_id
        self.__shape = shapes
        self.position = np.array([x, y])

    @staticmethod
    def fromstr(s):
        e = EntityTexture(0, 0)
        e.parse(s)
        return e



        
