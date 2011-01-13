#  Copyright 2008-2011 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from runonfailure import RunOnFailure


class Flex(RunOnFailure):

    def select_flex_application(self, locator, alias=None):
        self.page_should_contain_element(locator)
        self._wait_for_flex_ready(locator)
        return self._flex_apps.register(locator, alias)

    def _wait_for_flex_ready(self, locator, timeout=5000):
        # It seems that selenium timeout is always used so this timeout has no effect.
        self._selenium.do_command("waitForFlexReady", [locator, timeout])

    def flex_component_should_exist(self, locator):
        self._flex_command('flexAssertDisplayObject', 'id=%s' % locator)

    def click_flex_element(self, locator):
        try:
            self._flex_command('flexClick', 'id='+locator)
        except Exception:
            self._flex_command('flexClick', 'name='+locator)

    def input_text_into_flex(self, locator, value):
        self._flex_command('flexType', 'id=%s,text=%s' % (locator, value))

    def text_in_flex_should_be(self, locator, expected):
        self._flex_command('flexAssertText',
                           'id=%s,validator=%s' % (locator, expected))

    def _flex_command(self, command, options):
        # TODO: Howto handle commas in option values??
        app = self._flex_apps.current
        if not app:
            raise RuntimeError('No Flex application selected.')
        self._selenium.do_command(command, [app, options])

