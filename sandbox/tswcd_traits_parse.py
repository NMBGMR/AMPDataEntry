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
from traits.api import HasTraits, File, Button, Instance, Str
from traitsui.api import View, UItem, ListStrEditor
from traits.trait_base import ETSConfig
# ============= local library imports ===========================
from sandbox.tswcd_csv_parse import make_empty_col_dict, data_frame_formatter, gen_parce, trace_parce

ETSConfig.toolkit = 'qt4'

class DataEntry(HasTraits):

    site_id = Str
    genchem = File
    # tracechem = File
    chemlab_id = None
    minor_rows = None
    genchem_dataframe = None

    # todo - add output data paths for the genparce and trace parce

    output_genchem = File("Where do you want the output of general chemistry?")
    # output_tracechem = File("Where do you want the output of trace chemistry?")

    parse_chem = Button('Parse Chemistry')

    # trying to get the button to run the parce function...
    #
    def parce_gchem(self):
        # todo - modify gen-parce and trace_parce to take in an output directory as input
       self.chemlab_id, self.minor_rows = gen_parce(self.genchem, self.site_id, self.output_genchem)


class ParseTrace(HasTraits):

    def __init__(self, site_id, chemlab_id, minor_rows):
        self.site_id = site_id
        self.chemlabid = chemlab_id
        self.minor_rows = minor_rows

    tracechem = File
    output_tracechem = File("Where do you want the output of trace chemistry?")

    parse_chem = Button('Parse Chemistry')

    def parce_trace_chem(self):
        trace_parce(self.tracechem, self.site_id, self.chemlabid, self.minor_rows, self.output_tracechem)


class Finished(HasTraits):

    all_done = Str("All Done formatting")


def main():
    """a linear gui-based formatting tool for TSWCD chemistry operational use"""

    # ==== Panel 1 ======
    # get the locations of the important files and parse the general chemistry
    panel_1 = DataEntry()
    # # for testing
    # panel_1.genchem = "/Users/Gabe/Desktop/AMP/TSWCD_copy_paste_optimization/" \
    #                    "templatesforgeochemistryfilecopypaste/06-0038_MLC-53_Kolshorn NoLocation_gen.csv"
    panel_1.configure_traits()
    panel_1.parce_gchem()
    # ==== Panel 2 ======
    # get the locations for trace chemistry and parce the trace chemistry
    panel_2 = ParseTrace(panel_1.site_id, panel_1.chemlab_id, panel_1.minor_rows)
    # # for testing
    # panel_2.tracechem = "/Users/Gabe/Desktop/AMP/TSWCD_copy_paste_optimization/" \
    #                     "templatesforgeochemistryfilecopypaste/06-0038_MLC-53_Kolshorn NoLocation_trace.csv"
    panel_2.configure_traits()
    panel_2.parce_trace_chem()
    fin = Finished()
    fin.configure_traits()

    # ==== Questions for Jake ====
    # 1) how do you get the buttons to actually do something?
    # 2) what makes the def _something() functions different from def something() functions?


if __name__ == '__main__':
    main()
