import pandas as pd
import datetime
import rectpack


class Hangar(object):
    
    def __init__(self, height, width):
        
        b = (height, width)
        self.switch_list = []
        self.rects = dict()
        self.packers = dict()
        
        td = datetime.timedelta(days=1)
        start_date = datetime.date(2020, 5, 9)
        end_date = datetime.date(2021, 5, 9)

        while start_date <= end_date:
            self.rects.update({start_date: []})
            self.packers.update({start_date: newPacker().add_bin(*b)})
            start_date += td
        
        
    def is_available(self, t, t_delta, order_count, width, height):
        
        start_date = t
        end_date = t + datetime.timedelta(days=t_delta)
        td = datetime.timedelta(days=1)

        while start_date <= end_date:
            
            r = (height, width)
            packer = self.packer[start_date]
            packer.add_rect(*r)
            packer.pack()
            all_rects = packer.rect_list()

            if len(all_rects) == len(self.rects[start_date]):
                return False

            start_date += td
            
        return True



#псевдокод

A_SVO, A_DME, A_VNO = class_init
target = 0

for order in order_list:

    plane = order.plane

    A_airs = best_air_list(plane)
    
    counts_sorted = list(range(order.count))[::-1]

    for order_count in counts_sorted:

        for A_air in A_airs:

            time_list = A_air.t_list()

            for t in time_list:

                    if A_air.is_available(t, order.delta, order_count, order.width, order.height):

                        A_air.update(t, order.delta, order_count, order.width, order.height)

                        target += order.sum * order.delta * order_count
                        
                        t_new = t + order.delta
                        
                        if t_new not in time_list:
                            A_air.add_t(t_new)

                        go_to_next_order
