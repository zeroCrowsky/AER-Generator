import cv2
import numpy as np
import time

import aergen.core.log as log

X, Y = 0, 1
WIDTH, HEIGHT = X, Y

WHITE = 255, 255, 255
BLACK = 0,   0,   0
BLUE  = 244, 133, 66

# TODO : Sequence viewer : Probleme avec l'update_with_time_acquisition(), update auto avec le temps

class SequenceViewer(object):
    def __init__(self, sequence, time_acquisition, dim=None, celldim=None, grid=False, padding=0, update_mode='step-by-step', fps=None, delay=0):
        self.sequence         = sequence 
        self.time_acquisition = time_acquisition
        self.grid             = grid
        self.padding          = self.init_padding(padding)
    
        self.dim, self.celldim = self.init_dimension(dim, celldim)   
        self.dim     = round(self.dim[0]), round(self.dim[1])
        self.celldim = round(self.celldim[0]), round(self.celldim[1])
        self.background = np.full((self.height, self.width, 3), 255, dtype=np.uint8)
        self.frame = self.background

        self.viewcomponent = self.init_viewcomponent()
        
        self.fps   = fps
        self.delay = delay
        self.init_update_mode(update_mode)

        return

    def init_padding(self, padding):
        if isinstance(padding, (int, float)):
            return padding, padding
        return padding[0], padding[1]

    def init_dimension(self, dim, celldim):
        if dim is None:
            dim = [celldim[0]*self.sequence.width, celldim[1]*self.sequence.height]
            return dim, celldim

        if celldim is None:
            celldim = [dim[0]/self.sequence.width, dim[1]/self.sequence.height]
            return dim, celldim
        
        celldim[0] = dim[0]/self.sequence.width  if celldim[0] is None else celldim[0]
        celldim[1] = dim[1]/self.sequence.height if celldim[1] is None else celldim[1]

        dim[0] = celldim[0]*self.sequence.width  if dim[0] is None else dim[0]
        dim[1] = celldim[1]*self.sequence.height if dim[1] is None else dim[1]
        
        return dim, celldim


    def init_viewcomponent(self):
        return InputViewCompenent(self)


    def init_update_mode(self, update_mode):
        self.update_mode = update_mode

        self.updated = True
        self.update_cpt = 1

        self.init_times()

        if update_mode == 'time':
            self.update_method = self.update_method_with_time
        elif update_mode == 'step-by-step':
            self.update_method = self.update_method_step_by_step 

        return

    def init_times(self):
        self.t0 = time.time()
        self.t1 = self.t0
        self.t2 = self.t1
        self.t  = 0
        self.dt = 0
        self.t_run = 0
        self.clk_run = 0

        if self.fps is not None:
            self.delay = round(1/self.fps, 5)
        
        return 

    def sleep(self, sec):
        time.sleep(sec)
        return


    def update_time(self):
        # Variable manage time (unit: second)
        self.t2      = round(time.time(), 5)
        self.t2      = round(self.t2 - self.t_run, 5)
        self.t       = round(self.t2 - self.t0, 5)
        self.dt      = round(self.t2 - self.t1, 5)
        self.clk_run = round(self.clk_run + self.dt, 5)
        
        log.info('t :', self.t, 'dt :', self.dt, 'clk_run :', self.clk_run)
        return

    def update_method_with_time(self):
        self.t1 = self.t2
        return

    def update_method_step_by_step(self):
        self.updated = False
        self.update_cpt += 1
        return

    

    @property
    def width(self):
        return self.dim[0]

    @property
    def height(self):
        return self.dim[1]

    def update(self):
        if not self.updated:
             return
        self.viewcomponent.update()

        return

    def update_show(self):
        self.update_time()
        
        self.update_method()
        # self.update_method_with_time()
        return


    def clear(self):
        self.frame = self.background

    def show(self):
        self.clear()
        self.viewcomponent.draw()
        cv2.imshow('Viewer', self.frame)
        
        self.update_show()

        return 
        
    def dispatch_event(self):
        # get keys
        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord('q'):
            log.info('Key Q press, quit application loop...')
            return False
        
        if key == ord('n'):
            log.info('Key N press, next update (' + str(self.update_cpt) + ') ...')
            self.updated = True

        return True

    def run(self):
        # loop over frames from the video stream
        log.info('Start application loop...')
        while True:
            run = self.dispatch_event()
            if not run:
                break
            self.update()
            self.show()
        self.exit()

    def exit(self):
        # do a bit of cleanup
        log.info("Stop video stream thread...")
        log.info("Exit app...")
        cv2.destroyAllWindows()

        return

class InputViewCompenent(object):
    def __init__(self, view, position=None):
        self.view = view
        self.sequence = view.sequence
        self.t_acquisition = view.time_acquisition
        self.dim     = view.dim
        self.celldim = view.celldim
        
        self.position = np.array([0, 0]) if position is None else position

        self.t0_idx = 0
        self.t0     = self.sequence.times[self.t0_idx]

        self.finished      = False
        self.just_finished = False

        self.clear()
        self.cellcolor_empty = WHITE
        self.cellcolor_full  = BLUE

        return


    def draw(self):
        o = self.position
        for x in range(self.sequence.width):
            for y in range(self.sequence.height):
                x0, y0 = o[X] + x * self.celldim[WIDTH], o[Y] + y * self.celldim[HEIGHT]
                x1, y1 = x0 + self.celldim[WIDTH], y0 + self.celldim[HEIGHT]

                color = self.cellcolor_empty if self.matrix[y][x] == 0 else self.cellcolor_full 

                self.view.frame = cv2.rectangle(self.view.frame, (x0,y0), (x1,y1), color, -1)
                self.view.frame = cv2.rectangle(self.view.frame, (x0,y0), (x1,y1), BLACK, 1)
        
        return 

    def update(self):
        if self.is_finished():
            self.update_finish()
            return 

        if self.t_acquisition == 0:
            self.update_without_time_aquisition()
        else:
            self.update_with_time_acquisition()

        return 

    def is_finished(self):
        status = self.t0_idx >= len(self.sequence.times) - 1
        result = status and self.finished
        if status and not self.finished:
            self.just_finished = True
        self.finished = status
        return result

    def update_finish(self):
        log.info('Fin de la sequence')
        if self.just_finished:
            self.clear()
            self.just_finished = False
        return

    def clear(self):
        self.matrix = np.zeros((self.sequence.width, self.sequence.height), dtype=np.uint8)
        return
    
    def update_with_time_acquisition(self):
        self.clear()
        log.info('update_with_time_acquisition')
        for i in range(self.t0_idx, len(self.sequence.times)):
            ti = self.sequence.times[i]
            ii = self.sequence.indices[i]

            t1_idx = i
            t1     = self.t0 + self.t_acquisition

            if ti >= t1:
                self.t0_idx = t1_idx
                self.t0     = self.sequence.times[self.t0_idx]
                break
            
            xi = ii % self.sequence.width
            yi = ii // self.sequence.width
            self.matrix[yi][xi] = 1

        return 
    
    def update_without_time_aquisition(self):
        self.clear()

        for i in range(self.t0_idx, len(self.sequence.times)):
            ti = self.sequence.times[i]
            ii = self.sequence.indices[i]

            if self.t0 != ti:
                self.t0 = ti
                self.t0_idx = i
                break

            xi = ii % self.sequence.width
            yi = ii // self.sequence.width
            self.matrix[yi][xi] = 1            
        return


