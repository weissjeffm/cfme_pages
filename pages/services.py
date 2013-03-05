# -*- coding: utf-8 -*-

import re
from pages.base import Base
from pages.regions.quadicons import Quadicons
from pages.regions.quadiconitem import QuadiconItem

class Services(Base):
    class VirtualMachines(Base):
        _page_title = 'CloudForms Management Engine: Virtual Machines'
        
        @property
        def quadicon_region(self):
            return Quadicons(self.testsetup,Services.VirtualMachines.VirtualMachineQuadIconItem)
        
        @property
        def paginator(self):
            from pages.regions.paginator import Paginator
            return Paginator(self.testsetup)

        @property
        def accordion(self):
            from pages.regions.accordion import Accordion
            return Accordion(self.testsetup)
        
        @property
        def taskbar(self):
            from pages.regions.taskbar.taskbar import Taskbar
            return Taskbar(self.testsetup)
        
        class VirtualMachineQuadIconItem(QuadiconItem):
            @property
            def os(self):
                image_src = self._root_element.find_element(*self._quad_tl_locator).find_element_by_tag_name("img").get_attribute("src")
                return re.search('.+/os-(.+)\.png', image_src).group(1)
                
            @property
            def current_state(self):
                image_src = self._root_element.find_element(*self._quad_tr_locator).find_element_by_tag_name("img").get_attribute("src")
                return re.search('.+/currentstate-(.+)\.png',image_src).group(1)

            @property
            def vendor(self):
                image_src = self._root_element.find_element(*self._quad_bl_locator).find_element_by_tag_name("img").get_attribute("src")
                return re.search('.+/vendor-(.+)\.png', image_src).group(1)

            @property
            def snapshots(self):
                return self._root_element.find_element(*self._quad_br_locator).text
            