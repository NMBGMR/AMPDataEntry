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
from frontend.application import Application


def main():
    app = Application()
    app.source_file = '/Users/Gabe/Desktop/juliet_stuff/juliet_jornada_plot_stats/Pixel_012_RZSWF_stats.csv'
    app.configure_traits()


if __name__ == '__main__':
    main()
# ============= EOF =============================================