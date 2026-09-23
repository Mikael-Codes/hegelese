"""Adversarial tests for derived loss and history-constrained revision."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import hegelese as h
import hgl_lineage as l

ROOT = Path(__file__).resolve().parents[1]


class LineageTests(unittest.TestCase):
    def setUp(self):
        self.request = json.loads((ROOT / 'request-four.json').read_text())
        self.proposal = json.loads((ROOT / 'proposal-four.json').read_text())
        # The proposer never supplies exactPhase or any other observation.
        self.request['source']['observations'] = {}
        self.request['required_observations'] = []
        self.proposal['target']['observations'] = {}
        self.proposal['dispositions'] = {k: v for k, v in self.proposal['dispositions'].items()
                                         if k in ('initial', 'step')}
        self.proposal['request_sha256'] = h.digest(self.request)
        self.history = l.empty_history(self.request)

    def run_candidate(self, proposal=None, history=None, actions=None, budget=100000):
        return l.check_lineage(self.request,
                               l.successor(proposal or self.proposal, history or self.history, actions),
                               history or self.history, budget)

    def identity(self):
        p = copy.deepcopy(self.proposal)
        p['target'] = copy.deepcopy(self.request['source'])
        p['mapping'] = {s: s for s in self.request['source']['states']}
        return p

    def actions(self, action):
        return {f['id']: {'action': action, 'reason': 'Explicit test resolution.'}
                for f in h.check(self.request, self.proposal)['structural_loss']['groups']}

    def test_loss_without_any_named_observation(self):
        result = h.check(self.request, self.proposal)
        self.assertTrue(result['accepted'])
        self.assertEqual(result['structural_loss']['erased_pairs'], 2)
        self.assertEqual([f['states'] for f in result['structural_loss']['groups']], [['0', '2'], ['1', '3']])
        self.assertTrue(all(not f['nonrecoverable_observations'] for f in result['structural_loss']['groups']))

    def test_observation_recoverability_uses_type_tags(self):
        s = self.request['source']
        s['observations'] = {'tag': {'0': True, '1': False, '2': 1, '3': False}}
        losses = h.structural_losses(s, self.proposal['mapping'])['groups']
        self.assertEqual(losses[0]['nonrecoverable_observations']['tag']['states'], ['0', '2'])
        self.assertNotIn('tag', losses[1]['nonrecoverable_observations'])

    def test_unaccounted_loss_prevents_acceptance(self):
        result = self.run_candidate()
        self.assertEqual(result['status'], 'Unknown')
        self.assertTrue(result['base_check']['accepted'])
        self.assertEqual({f['status'] for f in result['loss_accounting']}, {'Unaccounted'})

    def test_forgetting_finding_after_repair_is_not_enough(self):
        history = self.run_candidate()['next_history']
        result = self.run_candidate(self.identity(), history)
        self.assertEqual(result['status'], 'Unknown')
        self.assertEqual(len(result['loss_accounting']), 2)

    def test_repair_must_hold_structurally(self):
        result = self.run_candidate(actions=self.actions('repair'))
        self.assertEqual(result['status'], 'Refuted')
        self.assertTrue(all(f['collision'] for f in result['loss_accounting']))

    def test_repaired_successor_passes_all_equations(self):
        history = self.run_candidate()['next_history']
        result = self.run_candidate(self.identity(), history, self.actions('repair'))
        self.assertTrue(result['accepted'])
        self.assertEqual({f['status'] for f in result['loss_accounting']}, {'Repaired'})
        self.assertEqual(result['base_check']['evidence']['checks_completed'], 5)

    def test_carry_remains_unknown(self):
        self.assertEqual(self.run_candidate(actions=self.actions('carry'))['status'], 'Unknown')

    def test_proposer_cannot_authorize_own_loss(self):
        result = self.run_candidate(actions=self.actions('accept_loss'))
        self.assertEqual(result['status'], 'Refuted')
        self.assertEqual({f['status'] for f in result['loss_accounting']}, {'Unauthorized'})

    def test_host_can_authorize_specific_loss(self):
        history = self.run_candidate()['next_history']
        history['authorized_losses'] = {k: 'Application only needs alternation.' for k in self.actions('accept_loss')}
        self.assertTrue(self.run_candidate(history=history, actions=self.actions('accept_loss'))['accepted'])

    def test_authorization_does_not_fix_false_equations(self):
        history = self.run_candidate()['next_history']
        history['authorized_losses'] = {k: 'Approved.' for k in self.actions('accept_loss')}
        proposal = copy.deepcopy(self.proposal)
        proposal['target']['transitions']['0']['tick'] = '0'
        self.assertEqual(self.run_candidate(proposal, history, self.actions('accept_loss'))['status'], 'Refuted')

    def test_truncated_history_cannot_match_retained_parent(self):
        history = self.run_candidate()['next_history']
        candidate = l.successor(self.identity(), self.history, self.actions('repair'))
        self.assertEqual(l.check_lineage(self.request, candidate, history)['status'], 'Invalid')

    def test_history_scope_change_rejected(self):
        history = self.run_candidate()['next_history']
        request = copy.deepcopy(self.request)
        request['source']['version'] = 'different'
        self.assertEqual(l.check_lineage(request, l.successor(self.identity(), history), history)['status'], 'Invalid')

    def test_candidate_evidence_is_rejected(self):
        candidate = l.successor(self.proposal, self.history)
        candidate['accepted'] = True
        self.assertEqual(l.check_lineage(self.request, candidate, self.history)['status'], 'Invalid')

    def test_prior_assumption_cannot_disappear(self):
        proposal = self.identity()
        proposal['assumptions'] = ['External clock is reliable.']
        history = self.run_candidate(proposal)['next_history']
        result = self.run_candidate(self.identity(), history)
        self.assertEqual(result['status'], 'Unknown')
        self.assertEqual(result['unresolved_assumptions'], ['External clock is reliable.'])

    def test_budget_exhaustion_cannot_become_cached_success(self):
        history = self.run_candidate(self.identity(), budget=1)['next_history']
        self.assertEqual(self.run_candidate(self.identity(), history, budget=1)['status'], 'Unknown')
        result = self.run_candidate(self.identity(), history)
        self.assertTrue(result['accepted'])
        self.assertEqual(result['base_check']['evidence']['checks_completed'], 5)

    def test_historical_optional_observation_cannot_be_withdrawn(self):
        request = json.loads((ROOT / 'request-four.json').read_text())
        proposal = json.loads((ROOT / 'proposal-four.json').read_text())
        first = copy.deepcopy(proposal)
        first['target'] = copy.deepcopy(request['source'])
        first['mapping'] = {s: s for s in request['source']['states']}
        first['dispositions']['observation:exactPhase']['action'] = 'retain'
        history = l.empty_history(request)
        history = l.check_lineage(request, l.successor(first, history), history)['next_history']
        findings = h.structural_losses(request['source'], proposal['mapping'])['groups']
        history['authorized_losses'] = {f['id']: 'Permit state mergers.' for f in findings}
        actions = {f['id']: {'action': 'accept_loss', 'reason': 'Authorized.'} for f in findings}
        result = l.check_lineage(request, l.successor(proposal, history, actions), history)
        self.assertEqual(result['status'], 'Refuted')
        self.assertEqual(result['inherited_checks']['failures'], 4)
        limited = l.check_lineage(request, l.successor(proposal, history, actions), history, 9)
        self.assertEqual(limited['status'], 'Unknown')
        self.assertEqual(limited['inherited_checks']['checks_completed'], 0)

    def test_repair_requires_all_pairs_not_only_first_witness(self):
        proposal = copy.deepcopy(self.proposal)
        proposal['mapping'] = dict.fromkeys(self.request['source']['states'], '0')
        history = self.run_candidate(proposal)['next_history']
        fid = h.structural_losses(self.request['source'], proposal['mapping'])['groups'][0]['id']
        # The current map separates 0 and 1, the old displayed witness, but
        # still merges 0/2 and 1/3. It has not repaired the whole old group.
        result = self.run_candidate(history=history, actions={fid: {'action': 'repair', 'reason': 'Patched witness.'}})
        self.assertEqual(result['status'], 'Refuted')
        self.assertEqual(next(f for f in result['loss_accounting'] if f['id'] == fid)['collision'], ['0', '2'])

    def test_new_mergers_are_not_hidden_by_repairing_old_groups(self):
        history = self.run_candidate()['next_history']
        proposal = copy.deepcopy(self.proposal)
        proposal['mapping'] = {'0': '0', '1': '0', '2': '1', '3': '1'}
        result = self.run_candidate(proposal, history, self.actions('repair'))
        self.assertEqual(len(result['loss_accounting']), 4)
        self.assertEqual(sum(f['status'] == 'Unaccounted' for f in result['loss_accounting']), 2)

    def test_renaming_target_does_not_erase_finding_identity(self):
        old = h.structural_losses(self.request['source'], self.proposal['mapping'])['groups']
        mapping = {s: 'renamed-' + t for s, t in self.proposal['mapping'].items()}
        new = h.structural_losses(self.request['source'], mapping)['groups']
        self.assertEqual({f['id'] for f in old}, {f['id'] for f in new})

    def test_identity_has_no_losses(self):
        self.assertEqual(h.check(self.request, self.identity())['structural_loss']['erased_pairs'], 0)

    def test_unreachable_states_are_included(self):
        self.request['source']['transitions'] = {s: {'tick': s} for s in self.request['source']['states']}
        self.assertEqual(h.structural_losses(self.request['source'], self.proposal['mapping'])['erased_pairs'], 2)

    def test_malformed_history_rejected(self):
        for attempts in [None, [None], [{'proposal': self.proposal, 'budget': -1}],
                         [{'proposal': self.proposal, 'budget': 1}] * 32]:
            history = copy.deepcopy(self.history)
            history['attempts'] = attempts
            self.assertEqual(self.run_candidate(history=history)['status'], 'Invalid')

    def test_unknown_authorization_or_resolution_rejected(self):
        history = copy.deepcopy(self.history)
        history['authorized_losses'] = {'invented': 'Trust me.'}
        self.assertEqual(self.run_candidate(history=history)['status'], 'Invalid')
        self.assertEqual(self.run_candidate(actions={'invented': {'action': 'repair', 'reason': 'Trust me.'}})['status'], 'Invalid')

    def test_json_cli_and_exit_codes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, data in [('request', self.request), ('history', self.history)]:
                (root / (name + '.json')).write_text(json.dumps(data))
            for proposal, resolutions, status, code in [
                (self.proposal, {}, 'Unknown', 3),
                (self.proposal, self.actions('repair'), 'Refuted', 1),
                (self.identity(), {}, 'ExhaustivelyChecked', 0),
            ]:
                (root / 'candidate.json').write_text(json.dumps(l.successor(proposal, self.history, resolutions)))
                result = subprocess.run([sys.executable, str(ROOT / 'hegelese.py'), 'lineage',
                                         str(root / 'request.json'), str(root / 'candidate.json'),
                                         str(root / 'history.json')], text=True, capture_output=True)
                self.assertEqual(result.returncode, code, result.stderr)
                self.assertEqual(json.loads(result.stdout)['status'], status)

    def test_cli_example(self):
        result = subprocess.run([sys.executable, 'examples/lineage_demo.py'], cwd=ROOT,
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('repaired successor: ExhaustivelyChecked', result.stdout)


if __name__ == '__main__':
    unittest.main()
