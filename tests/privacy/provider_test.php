<?php
// This file is part of Moodle - http://moodle.org/
//
// Moodle is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// Moodle is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with Moodle.  If not, see <http://www.gnu.org/licenses/>.

namespace local_newplugin\privacy;

/**
 * Tests for the privacy provider of local_newplugin.
 *
 * @package    local_newplugin
 * @category   test
 * @copyright  {{YEAR}} {{AUTHOR}} <{{EMAIL}}>
 * @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 * @covers     \local_newplugin\privacy\provider
 */
final class provider_test extends \advanced_testcase {
    /**
     * The provider declares that no personal data is stored, with an existing language string.
     */
    public function test_get_reason(): void {
        $reason = provider::get_reason();
        $this->assertSame('privacy:metadata', $reason);
        $this->assertTrue(get_string_manager()->string_exists($reason, 'local_newplugin'));
    }
}
