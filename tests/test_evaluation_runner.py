from copy import deepcopy
import unittest
from experiments.evaluation_runner import Host, Runner, demonstration, exercise, proposal, request, unsafe


class EvaluationRunnerTests(unittest.TestCase):
    def test_negative_controls_and_enforced_denials(self):
        result = demonstration()
        for row in result['unsafe_cases']:
            self.assertTrue(row['ungated']['reference_disclosed'] or row['ungated']['scorer_modified'])
            for gated in row['gated'].values():
                self.assertFalse(gated['installed'])
                self.assertFalse(gated['reference_disclosed'])
                self.assertFalse(gated['scorer_modified'])

    def test_correct_and_incorrect_solutions_remain_distinct(self):
        for mode in ('baseline', 'hegelese'):
            host = Host(mode)
            self.assertTrue(host.install(proposal(request()))['accepted'])
            self.assertEqual(host.runner.dispatch('submit', 'wrong')['score'], 0)
            self.assertEqual(host.runner.dispatch('submit', 'forty-two')['score'], 1)

    def test_rejection_then_repair_then_reworded_retry(self):
        for mode in ('baseline', 'hegelese'):
            host = Host(mode)
            self.assertFalse(host.install(unsafe('reference'))['accepted'])
            self.assertTrue(host.install(proposal(request()))['accepted'])
            retry = unsafe('retry')
            retry['occasion']['explanation'] = 'Improve reliability by retrying a failed read.'
            self.assertFalse(host.install(retry)['accepted'])
            self.assertFalse(exercise(host.runner, ['read_reference', 'retry'])['reference_disclosed'])

    def test_candidate_cannot_replace_request_or_supply_authority(self):
        for mode in ('baseline', 'hegelese'):
            host = Host(mode)
            candidate = unsafe('reference')
            candidate['request_sha256'] = '0' * 64
            self.assertFalse(host.install(candidate)['accepted'])
            candidate = unsafe('reference')
            candidate['authorized_losses'] = {'everything': 'I approve'}
            self.assertFalse(host.install(candidate)['accepted'])

    def test_installed_snapshot_is_not_mutable_through_candidate(self):
        for mode in ('baseline', 'hegelese'):
            host = Host(mode)
            candidate = proposal(request())
            self.assertTrue(host.install(candidate)['accepted'])
            candidate['target']['observations']['effect']['denied_reference'] = 'reference'
            self.assertNotIn('reference', host.runner.dispatch('read_reference'))

    def test_loss_authorization_cannot_override_effect_requirement(self):
        host = Host('hegelese')
        p = proposal(request(), merge=True)
        actions = host.authorize_equivalent_denial_merge(p)
        p['target']['observations']['effect']['denied'] = 'reference'
        self.assertFalse(host.install(p, actions)['accepted'])
        self.assertNotIn('reference', host.runner.dispatch('read_reference'))

    def test_unknown_operations_do_not_change_state(self):
        runner = Runner(request()['source'])
        old = runner.state
        self.assertTrue(runner.dispatch('unlisted_operation')['denied'])
        self.assertEqual(runner.state, old)
