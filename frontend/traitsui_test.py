# ===============================================================================
# Copyright 2018 gabe-parrish
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================

# ============= standard library imports ========================
import os

from traitsui.toolkit import *

from traits.trait_base import ETSConfig
from pyface.base_toolkit import Toolkit, find_toolkit
from traits.api import * #HasTraits, Int, Str, Property
from traitsui.api import *
from subprocess import call

"""if you have trouble with the toolkit you need to check it in the terminal. this can be done in terminal in
the current env:
 python
 import os
 os.environ[ETS_TOOLKIT]

 if set to null or wx change it in the script globally by doing ETSConfig.toolkit = 'qt4'
"""

# ============= local library imports ===========================

ETSConfig.toolkit = 'qt4'
class Calculator(HasTraits):
    """
    Takes values 1 and 2. Sums the values and displays it in a GUI
    """
    value1 = Int()
    value2 = Int()

    sum = Property(Int, depends_on='value1, value2')

    def _get_sum(self):

        return self.value1 + self.value2

    # ==== Aesthetics ====

    view1 = View(
        Group(
            HGroup(Item('value1'), Item('value2')),
            HGroup(Item('sum', style='readonly')),
        ),
        resizable=True, title="Summer Tool", buttons=['Undo', 'Cancel', 'OK']
    )

class Double_Calculator(HasTraits):
    """
    Takes values 1 and 2. Sums the values and displays it in a GUI
    """
    value1 = Int(0)
    value2 = Int(0)

    # We can add instances of the previous Class...
    calc1 = Instance(Calculator(), ())
    calc2 = Instance(Calculator(), ())

    # Don't need this property anymore...
    # sum = Property(Int, depends_on='value1, value2')

    # main window (master)
    @on_trait_change('value1, value2')
    def update_1(self):
        self.calc1.value1 = self.value1;self.calc2.value1 = self.value1
        self.calc1.value2 = self.value2;self.calc2.value2 = self.value2

    # sub-window
    @on_trait_change('calc1.value2, calc1.value1')
    def update_2(self):
          self.value2 = self.calc1.value2; self.value1 = self.calc1.value1
    # sub-window
    @on_trait_change('calc2.value1, calc2.value2')
    def update_3(self):
          self.value2 = self.calc2.value2 ; self.value1 = self.calc2.value1



    # ==== Aesthetics ====

    view = View(
        VGroup(
            HGroup(Item('value1'), Item('value2')),
            Tabbed(Item('calc1', style='custom'), Item('calc2', style='custom')),
        ),
        resizable=True, title="Summer Tool", buttons=['Undo', 'Cancel', 'OK']
    )

def main():
    """Tests traits"""

    # print("toolkit i'm trying to use", ETSConfig.toolkit)
    # Calculator().configure_traits(view='view1')
    Double_Calculator().configure_traits()

if __name__ == "__main__":
    main()
# ============= EOF =============================================
