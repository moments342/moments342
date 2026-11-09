import copy
import importlib.util
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
spec=importlib.util.spec_from_file_location('profile_build',Path(__file__).with_name('build.py'))
build=importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)

class ContributionRendererTest(unittest.TestCase):
    def setUp(self):
        self.calendar={'totalContributions':3,'weeks':[{'contributionDays':[{'contributionCount':0,'date':'2026-11-08','weekday':0},{'contributionCount':3,'date':'2026-11-09','weekday':1}]}]}
    def test_actual_counts_survive_in_both_maps(self):
        for m in [False,True]:
            root=ET.fromstring(build.activity(self.calendar,m));body=''.join(root.itertext())
            self.assertIn('3 contribuições',body);self.assertIn('2026-11-08: 0 contribuições',body);self.assertIn('2026-11-09: 3 contribuições',body)
    def test_mismatched_source_fails_instead_of_publishing_wrong_activity(self):
        self.calendar['totalContributions']=4
        with self.assertRaises(ValueError):build.render(self.calendar)
    def test_duplicate_days_fail(self):
        self.calendar['weeks'][0]['contributionDays'].append(copy.deepcopy(self.calendar['weeks'][0]['contributionDays'][1]));self.calendar['totalContributions']=6
        with self.assertRaises(ValueError):build.validate_calendar(self.calendar)
    def test_empty_activity_does_not_invent_work(self):
        for d in self.calendar['weeks'][0]['contributionDays']:d['contributionCount']=0
        self.calendar['totalContributions']=0
        for m in [False,True]:
            svg=build.activity(self.calendar,m);self.assertIn('0 contribuições',svg);self.assertNotIn('nan',svg.lower());ET.fromstring(svg)
    def test_render_is_deterministic_and_script_free(self):
        a=build.render(self.calendar);self.assertEqual(a,build.render(self.calendar));self.assertEqual(len(a),16)
        for svg in a.values():ET.fromstring(svg);self.assertNotIn('<script',svg);self.assertNotIn('foreignObject',svg)

if __name__=='__main__':unittest.main()
