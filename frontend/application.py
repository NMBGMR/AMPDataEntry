# ===============================================================================
# Copyright 2018 ross
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
from traits.api import HasTraits, File, Button, Instance, Str
from traitsui.api import View, UItem, ListStrEditor

from backend.parser import Parser


class Application(HasTraits):

    source_file = File
    parse_button = Button('Parse')
    parser = Instance(Parser)

    selected_row = Str

    def _selected_row_changed(self, new):
        print('the selected row is ', new)

    def _source_file_changed(self):
        self.parser.parse(self.source_file)

    # def _parse_button_fired(self):
    #     self.parser.parse(self.source_file)

    def _parser_default(self):
        return Parser()

    def traits_view(self):
        v = View(UItem('source_file'),
                 UItem('object.parser.header_list', editor=ListStrEditor(selected='selected_row')),
                 title='AMP Data Entry',
                 resizable=True,
                 width=700, height=500
                 )
        return v

# ============= EOF =============================================
