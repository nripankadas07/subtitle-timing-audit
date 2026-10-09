import unittest
import subtitle_timing_audit as m


def srt(*intervals):
    return '\n\n'.join('%d\n%s --> %s\n%s' % (i+1,*x) for i,x in enumerate(intervals))


class Tests(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(m.audit(srt(('00:00:01,000','00:00:03,000','Hello')))['findings'],[])
    def test_numeric_last_line_preserved(self):
        self.assertEqual(m.parse(srt(('00:00:01,000','00:00:03,000','Town\n1963')))[0]['lines'],['Town','1963'])
    def test_nonadjacent_overlap(self):
        r=m.audit(srt(('00:00:01,000','00:00:10,000','A'),('00:00:02,000','00:00:03,000','B'),('00:00:04,000','00:00:05,000','C')))
        self.assertEqual([(x['cue'],x['other_cue']) for x in r['findings'] if x['code']=='overlap'],[(2,1),(3,1)])
    def test_touching_is_not_overlap(self):
        self.assertFalse(m.audit(srt(('00:00:01,000','00:00:02,000','A'),('00:00:02,000','00:00:03,000','B')))['findings'])
    def test_reading_rate(self):
        self.assertIn('reading_rate',[x['code'] for x in m.audit(srt(('00:00:01,000','00:00:02,000','x'*21)))['findings']])
    def test_line_length(self):
        self.assertIn('line_length',[x['code'] for x in m.audit(srt(('00:00:01,000','00:00:06,000','x'*43)))['findings']])
    def test_nonpositive(self):
        self.assertEqual(m.audit(srt(('00:00:02,000','00:00:01,000','A')))['findings'][0]['code'],'nonpositive_duration')
    def test_bad_timestamp(self):
        with self.assertRaises(ValueError):m.parse(srt(('00:61:01,000','00:00:03,000','A')))
    def test_duplicate_and_order(self):
        r=m.audit('2\n00:00:02,000 --> 00:00:03,000\nA\n\n2\n00:00:01,000 --> 00:00:02,000\nB')
        self.assertTrue({'duplicate_index','chronology','nonsequential_index'} <= {x['code'] for x in r['findings']})
    def test_short_gap(self):
        r=m.audit(srt(('00:00:01,000','00:00:02,000','A'),('00:00:02,100','00:00:03,100','B')),{'min_gap_ms':200})
        self.assertEqual(r['findings'][0]['code'],'short_gap')
    def test_bom_crlf(self):
        self.assertEqual(m.audit('\ufeff'+srt(('00:00:01,000','00:00:03,000','Hello')).replace('\n','\r\n'))['findings'],[])
    def test_policy_fail_closed(self):
        for p in ({'max_cps':True},{'max_cps':float('nan')},{'unknown':1},{'min_duration_ms':8000}):
            with self.assertRaises(ValueError):m.policy(p)
    def test_limit(self):
        with self.assertRaises(ValueError):m.parse('x'*(2*1024*1024+1))
    def test_no_caption_in_report(self):
        self.assertNotIn('SECRET_TEXT',str(m.audit(srt(('00:00:01,000','00:00:02,000','SECRET_TEXT')))))


if __name__=='__main__':unittest.main()
