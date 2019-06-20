class EntityIdentityFactory(object):
    def __init__(self, *args, **kwargs):
        self.args = args; self.kwargs = kwargs

    def create(self):
        return EntityInput(*self.args, **self.kwargs)

# EAST  sw,          h//2-sh//2
# WEST  w-sw         h//2-sh//2
# NORTH w//2-sw//2   sh
# SOUTH w//2-sw//2   h-sh
