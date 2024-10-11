"""
pyodide-mkdocs-theme
Copyleft GNU GPLv3 🄯 2024 Frédéric Zinelli

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.
If not, see <https://www.gnu.org/licenses/>.
"""


from dataclasses import dataclass
import json
from textwrap import dedent
from typing import Callable, ClassVar, Dict, List, Tuple, TYPE_CHECKING


from .. import html_builder as Html
from ..tools_and_constants import HtmlClass, Kinds, PageUrl, PmtTests, Prefix, ScriptKind, ScriptSection
from ..plugin.maestro_tools_tests import IdeToTest
from .ide_ide import Ide


if TYPE_CHECKING:
    from ..plugin.pyodide_macros_plugin import PyodideMacrosPlugin




@dataclass
class IdeTester(Ide):

    MACRO_NAME: ClassVar[str] = "IDE_tester"

    ID_PREFIX: ClassVar[str] = Prefix.tester_

    NEEDED_KINDS: ClassVar[Tuple[ScriptKind]] = (
        Kinds.pyodide,
        Kinds.terms,
        Kinds.ides,
        Kinds.ides_test,
    )


    @property
    def has_check_btn(self):
        """ Tester always has... """
        return True


    def register_ide_for_tests(self):
        """ IdeTester are never registered for testing... """


    def list_of_buttons(self):
        return super().list_of_buttons()[:2]


    def counter_txt_spans(self):
        if self.env._dev_mode:                  # pylint: disable=protected-access
            return super().counter_txt_spans()
        return ''


    def build_corr_and_rems(self):
        """
        No corr/REMs visible here. Replace with an extra button to trigger all the tests.
        """
        btn = self.create_button('test_ides')
        return (
            '<br>\n\n'
            f'<div class="inline" id="test-ide-results">{ btn }<ul>'
                '<li>IDEs found : <span id="cnt-all"></span></li>'
                '<li>Skip :       <span id="cnt-skip" style="color:gray;"></span></li>'
                '<li>To do :      <span id="cnt-remaining"></span></li>'
                '<li>Success :    <span id="cnt-success" style="color:green;"></span></li>'
                '<li>Error :      <span id="cnt-failed" style="color:red;"></span></li>'
            '</ul>'
            '<button type="button" class="cases-btn" id="select-all">Select all</button>'
            '<br><button type="button" class="cases-btn" id="unselect-all">Unselect all</button>'
            '<br><button type="button" class="cases-btn" id="toggle-human">Toggle human</button>'
            '</div>'
            '\n\n'
        )



    #-----------------------------------------------------------------------------------



    @classmethod
    def get_markdown(cls, use_mermaid:bool):
        """
        Build the code generating the IdeTester object. Insert the MERMAID logistic only if
        the `mkdocs.yml` holds the custom fences code configuration.
        """
        return dedent(f"""
            # Testing all IDEs in the documentation

            <br>

            {'{{'} IDE_tester(MAX='+', MERMAID={ use_mermaid }) {'}}'}

        """)



    @classmethod
    def build_html_for_tester(
        cls,
        env:'PyodideMacrosPlugin',
        pages_with_ides: Dict[PageUrl, List[IdeToTest]],
    ) -> str :
        """
        Build all the html base elements holding the results/information for each IDE to test.
        """

        use_load_button = env.testing_include == PmtTests.serve
        if env.testing_load_buttons is not None:
            use_load_button = env.testing_load_buttons

        script_data = {}
        table_like  = ''.join(
            row for url,lst in pages_with_ides.items()
                for item in lst
                for row in cls._build_one_ide_items(env, url, item, use_load_button, script_data)
        )
        div_table = Html.div(
            table_like,
            kls = HtmlClass.py_mk_tests_results
        )
        cases_script = f"<script>const CASES_DATA={ json.dumps(script_data) }</script>"

        return Html.div( div_table + cases_script, kls=HtmlClass.py_mk_tests_table)


    @staticmethod
    def _diver(item:IdeToTest) -> Callable :

        def dive(*a, id=None, kls=None,**kw):
            return Html.div(
                *a,
                id  = id and f"{ id }-{ item.editor_id }",
                kls = f"{ HtmlClass.py_mk_test_element } { kls or '' }".strip(),
                **kw
            )
        return dive


    @staticmethod
    def description(dump:dict, is_top=False):
        """
        Build one test description html, with proper classes/ids/format.
        """
        if is_top and 'description' not in dump:
            return ""
        desc = Html.div(dump['description'], kls="pmt_note_tests" + ' top_test'*is_top)
        if is_top:
            desc = '<br>' + desc
        return desc



    @classmethod
    def _build_one_ide_items(
        cls,
        env:'PyodideMacrosPlugin',
        url:str,
        item:IdeToTest,
        use_load_button:bool,
        script_data: List[str],
    ):
        """
        Build the entire html data for the given IDE/item.
        Might generate several subtests if Case.subcases is used.
        """
        js_dump = item.as_dict(env, url)
        dive    = cls._diver(item)

        # Store for dump so script tag:
        script_data[ js_dump['editor_id'] ] = js_dump

        # Build main test/item row:
        main_row = cls._build_main_item_row(env, dive, js_dump, use_load_button, item)
        yield main_row

        # Now generate all the subtests, if they exist:
        for i,sub_case in enumerate(js_dump.get('subcases',()), 1):
            if 'subcases' in sub_case:
                raise ValueError("Case.subcases should go down one level at most.")

            div_svg   = dive('', id=HtmlClass.status+str(i), kls=HtmlClass.status)
            lone_btn  = cls.cls_create_button(env, 'test_1_ide', extra_btn_kls="testing")
            lone_test = dive(lone_btn, id=f"play{i}")

            yield dive(cls.description(sub_case)) + div_svg + lone_test + '<div></div>'




    @classmethod
    def _build_main_item_row(
        cls,
        env,
        dive:Callable,
        js_dump:dict,
        use_load_button:bool,
        item: IdeToTest,
    ):

        ide_name = js_dump['ide_name']

        # Link + main test description
        a_href = Html.a(ide_name, href=js_dump['ide_link'], target="_blank")
        link   = dive( a_href + cls.description(js_dump, True) )

        # Empty div that WILL hold the test's status svg indicator (filled in JS):
        svg_status = dive( '', id=HtmlClass.status, kls=HtmlClass.status + ' top_test')

        # Buttons
        load_btn  = cls.cls_create_button(env, 'load_ide') * use_load_button
        play_1    = cls.cls_create_button(env, 'test_1_ide')
        main_btns = dive( load_btn + play_1, id="test-btns")

        # sections indicators:
        def boxer(section):
            use_orange = (
                section=='code' and js_dump.get('code')
                or section=='corr' and not js_dump.get('code')
            )
            return Html.checkbox(
                item.has_section[section],
                id  = f"box_{ section }_{ item.editor_id }",
                kls = "section-box",
                kls_box = 'orange-box' * use_orange,
                tip_txt = section+"?",
                tip_shift=90,
            )

        row1 = []
        row2 = []
        for section in ScriptSection.sections():
            box = boxer(section)
            if section is ScriptSection.env_term:
                row2.append(box)
            elif section is ScriptSection.corr:
                row2.extend(map(boxer, (section,'REM','VIS_REM') ))
            elif section is ScriptSection.post_term:
                row2.append(box)
            else:
                row1.append(box)
        sections = dive( ''.join(row1+row2), kls='sections')

        return link + svg_status + main_btns + sections
