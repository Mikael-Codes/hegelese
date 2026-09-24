"""Meaningful checks for the comparison's independent oracle and runtime."""
from copy import deepcopy
import unittest
from experiments.workflow_comparison import Workflow, compare, request, trace_check


class WorkflowComparisonTests(unittest.TestCase):
    def test_baseline_checks_beyond_one_step_and_replays_counterexample(self):
        source = request()['source']
        target = deepcopy(source)
        target['transitions']['cancelled']['approve'] = 'approved'
        result = trace_check(source, target, {'canPublish'})
        self.assertFalse(result['accepted'])
        self.assertEqual(result['trace'], ['cancel', 'approve'])
        runtime = Workflow(target)
        for event in result['trace']:
            runtime.dispatch(event)
        self.assertTrue(runtime.observe()['canPublish'])

    def test_runtime_owns_copy(self):
        source = request()['source']
        runtime = Workflow(source)
        source['transitions']['draft']['approve'] = 'approved'
        self.assertFalse(runtime.dispatch('approve')['canPublish'])

    def test_baseline_preserves_types_and_detects_missing_observation(self):
        source = request()['source']
        target = deepcopy(source)
        target['observations']['canPublish']['draft'] = 0
        self.assertFalse(trace_check(source, target, {'canPublish'})['accepted'])
        del target['observations']['canPublish']
        self.assertFalse(trace_check(source, target, {'canPublish'})['accepted'])

    def test_honest_comparison_and_useful_abstraction(self):
        rows = compare()['cases']
        self.assertEqual([r['trace_baseline']['accepted'] for r in rows], [True, True, True, False, False, False])
        self.assertEqual([r['lineage_accepted'] for r in rows], [True, False, True, False, False, False])
        self.assertEqual(rows[1]['lineage'], 'Unknown')
        self.assertEqual(rows[-1]['ordinary_finite_check'], 'ExhaustivelyChecked')
        self.assertEqual(rows[-1]['lineage'], 'Refuted')


if __name__ == '__main__':
    unittest.main()
