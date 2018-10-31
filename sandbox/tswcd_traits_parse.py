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
# ============= local library imports ===========================
from sandbox.tswcd_csv_parse import make_empty_col_dict, data_frame_formatter, gen_parce, trace_parce

class GenchemParse(HasTraits):

    # todo - how do these get in here?
    site_id = Str
    csv_path = File
    # chemlab_id = Str
    chemlab_id = None
    minor_rows = None

    def _parse(self, site_id, csv_path):
        self.chemlab_id, self.minor_rows = gen_parce(csv_path, site_id)

class TracechemParse(HasTraits):

    chemlab_id = Str
    csv_path = Str
    site_id = Str
    chemlab_id =  Str
    minor_rows_gen = Str

    def _parse(self):
        trace_parce(self.csv_path, self.site_id, self.chemlab_id, self.minor_rows_gen)

class Application(HasTraits):

    # Fields the user will fill out.
    site_id = Str
    gen_chem_file = File
    trace_chem_file = File
    parce_gen_chem = Button("Parse General Chemistry")
    parce_trace_chem = Button("Parse Trace Chemistry")

    # Fields that will be filled out by using the parce_gen_chem button
    # a string
    chemlab_id = None
    # a dictionary todo - Does traits handle that in the UI?
    minor_rows = None

    # Instances of Objects: To do things with the inputs
    gen_parse = Instance(GenchemParse)
    trace_parse = Instance(TracechemParse)

    def _parce_gen_chem_fired(self):
        parse_obj = self.gen_parse(self.gen_chem_file, self.site_id)
        chemlab_id = parse_obj.chemlab_id
        minor_rows = parse_obj.minor_rows

    def _parce_trace_chem_fired(self):
        trace_parse = self.trace_parse(self.trace_chem_file, self.site_id, self.chemlab_id, self.minor_rows)


    def traits_view(self):
        v = View(UItem('site_id'),
                 UItem('gen_chem_file'),
                 UItem('trace_chem_file'),
                 title='TSWCD Data Entry',
                 resizable=True,
                 width=700, height=500
                 )
        return v


def main():
    """"""
    # I imagine we'll call the GenchemParse, we'll save the info from Genchem that we need in the application

    # Then when that's done we'll call the TracechemParse

    # # # todo - don't forget the A or B etc if it's the first/second sample from the site, got it?
    # site_id = "NM-28308A"
    # # chemlab_id, minor_rows = gen_parce(kolshorn_gen, site_id)
    # #
    # # trace_parce(kolshorn_trace, site_id, chemlab_id, minor_rows)

    app = Application()
    app.gen_chem_file = "/Users/Gabe/Desktop/AMP/TSWCD_copy_paste_optimization/" \
                   "templatesforgeochemistryfilecopypaste/06-0038_MLC-53_Kolshorn NoLocation_gen.csv"
    app.trace_chem_file = "/Users/Gabe/Desktop/AMP/TSWCD_copy_paste_optimization/" \
                     "templatesforgeochemistryfilecopypaste/06-0038_MLC-53_Kolshorn NoLocation_trace.csv"

    app.configure_traits()



if __name__ == '__main__':
    main()