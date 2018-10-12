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

from traits.trait_base import ETSConfig
from pyface.base_toolkit import Toolkit, find_toolkit
from traits.api import * #HasTraits, Int, Str, Property
from traitsui.api import *
import pandas as pd

# ============= local library imports ===========================
ETSConfig.toolkit = 'qt4'

# todo - is 'table editor with live search and cell" useful for us?
class file_selection(HasTraits):

    # File references the built-in file editor.
    file_name = File
    # List references the built-in list editor
    header_list = List

    # When the user selects a file, the decorator triggers the function that reads the headers.
    @on_trait_change('file_name')
    def update1(self):
        df = pd.read_csv(self.file_name, header=0)
        self.header_list = list(df.columns.values)

    # ==== Aesthetics ====

    # create a resizeable vertical list.
    view1 = View(VGroup(Item('file_name', style='simple'), Item('header_list', style='readonly')),
                 resizable=True, title="Select the xls or csv you want to read in", buttons=['Undo', 'Cancel', 'OK']
                 )

file_selection().configure_traits(view='view1')

# # Testing
# if __name__ == "__main__":
#
#     path = "/Users/Gabe/Desktop/juliet_stuff/juliet_jornada_plot_stats/Pixel_012_RZSWF_stats.csv"
#     df = pd.read_csv(path, header=0)
#     print(df.columns)
#     print(list(df.columns.values))