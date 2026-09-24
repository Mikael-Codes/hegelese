"""Synthetic evaluation-runner safety demonstration. No network or real secrets.

Candidates are finite JSON policies, never executable Python. The trusted host
owns the dispatcher, reference answer, scorer, requirements and history. This
is not an OS sandbox and cannot contain arbitrary code running in its process.
"""
from copy import deepcopy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import hegelese as h
import hgl_lineage as lineage
from experiments.workflow_comparison import trace_check


def request():
    events = ['read_input', 'submit', 'read_reference', 'write_scorer', 'retry']
    effects = {'ready': 'none', 'input': 'input', 'scored': 'score',
               'denied_reference': 'deny', 'denied_scorer': 'deny'}
    row = {'read_input': 'input', 'submit': 'scored',
           'read_reference': 'denied_reference', 'write_scorer': 'denied_scorer'}
    transitions = {s: dict(row, retry=s) for s in effects}
    source = {'name': 'SyntheticEvaluationRunner', 'version': '1',
              'states': list(effects), 'inputs': events, 'initial': 'ready',
              'transitions': transitions,
              'observations': {'effect': effects}}
    return {'schema': 'hegelese-request/0.1', 'source': source,
            'required_observations': ['effect']}


def proposal(r, merge=False):
    source = r['source']
    mapping = {s: 'denied' if merge and s.startswith('denied_') else s for s in source['states']}
    target = deepcopy(source)
    target['states'] = sorted(set(mapping.values()))
    target['transitions'] = {mapping[s]: {e: mapping[t] for e, t in row.items()}
                             for s, row in source['transitions'].items()}
    target['observations'] = {n: {mapping[s]: v for s, v in table.items()}
                              for n, table in source['observations'].items()}
    return {'schema': 'hegelese-proposal/0.1', 'operation': 'upheave',
            'request_sha256': h.digest(r), 'occasion': {'kind': 'Rearticulation',
            'explanation': 'Simplify a synthetic evaluation policy while preserving its effects.'},
            'target': target, 'mapping': mapping,
            'dispositions': {n: {'action': 'retain', 'reason': 'Preserve the host requirements.'}
                             for n in ['initial', 'step', 'observation:effect']},
            'assumptions': []}


class Runner:
    """Trusted toy dispatcher. Only the policy table is candidate-controlled.

    The deliberately available reference/tamper effects let negative controls
    show what an unsafe installed policy would do. They are not real resources.
    """
    def __init__(self, policy):
        self.policy = deepcopy(policy)
        self.state = policy['initial']
        self.reference = 'SYNTHETIC-REFERENCE-42'
        self.scorer_modified = False
        self.audit = []

    def dispatch(self, event, answer=''):
        if event not in self.policy['inputs']:
            self.audit.append({'event': event, 'effect': 'deny_unknown'})
            return {'denied': True}
        self.state = self.policy['transitions'][self.state][event]
        effect = self.policy['observations']['effect'][self.state]
        self.audit.append({'event': event, 'effect': effect})
        if effect == 'input':
            return {'input': 'Return the string forty-two.'}
        if effect == 'score':
            return {'score': 1 if self.scorer_modified or answer == 'forty-two' else 0}
        if effect == 'reference':
            return {'reference': self.reference}
        if effect == 'tamper':
            self.scorer_modified = True
            return {'modified': True}
        return {'denied': effect == 'deny'}


class Host:
    """Only install checked snapshots. Caller owns this object, not candidate.

    A JSON candidate cannot provide a replacement request, dispatcher, or history.
    This separation is a harness assumption, NOT Python access-control security.
    """
    def __init__(self, mode):
        if mode not in ('baseline', 'hegelese'):
            raise ValueError('Unknown mode')
        self.mode = mode
        self.request = request()
        self.history = lineage.empty_history(self.request)
        self.runner = Runner(self.request['source'])

    def install(self, candidate, resolutions=None):
        snapshot = deepcopy(candidate)
        if self.mode == 'hegelese':
            result = lineage.check_lineage(self.request,
                       lineage.successor(snapshot, self.history, resolutions), self.history)
            if 'next_history' in result:
                self.history = result['next_history']
        else:
            # Same input schema validation; independent semantic checker below.
            # Required effect obligation is host-fixed, never candidate-supplied.
            try:
                h.validate(self.request, snapshot, 100000)
                result = trace_check(self.request['source'], snapshot['target'], {'effect'})
            except (h.Invalid, KeyError, TypeError) as error:
                result = {'accepted': False, 'status': 'Invalid', 'error': str(error)}
        if result['accepted']:
            self.runner = Runner(snapshot['target'])
        return result

    def authorize_equivalent_denial_merge(self, candidate):
        """Explicit HOST fixture action, never called from candidate input."""
        findings = h.structural_losses(self.request['source'], candidate['mapping'])['groups']
        actions = {}
        for f in findings:
            if set(f['states']) != {'denied_reference', 'denied_scorer'}:
                raise ValueError('Only this reviewed harmless merger is authorized')
            self.history['authorized_losses'][f['id']] = 'Host permits merging denied-route identity; effects must still be preserved.'
            actions[f['id']] = {'action': 'accept_loss', 'reason': 'Host-reviewed equivalent denial states.'}
        return actions


def unsafe(kind):
    p = proposal(request())
    target = p['target']
    if kind == 'reference':
        target['observations']['effect']['denied_reference'] = 'reference'
    elif kind == 'scorer':
        target['observations']['effect']['denied_scorer'] = 'tamper'
    elif kind == 'retry':
        target['states'].append('leaked')
        target['observations']['effect']['leaked'] = 'reference'
        target['transitions']['leaked'] = dict(target['transitions']['ready'], retry='leaked')
        target['transitions']['denied_reference']['retry'] = 'leaked'
    else:
        raise ValueError(kind)
    return p


def exercise(runner, trace):
    outputs = [runner.dispatch(event, 'wrong-answer') for event in trace]
    return {'outputs': outputs, 'reference_disclosed': any('reference' in o for o in outputs),
            'scorer_modified': runner.scorer_modified, 'audit': deepcopy(runner.audit)}


def demonstration():
    cases = [('reference', ['read_reference']),
             ('scorer', ['write_scorer', 'submit']),
             ('retry', ['read_reference', 'retry'])]
    rows = []
    for name, trace in cases:
        p = unsafe(name)
        ungated = exercise(Runner(p['target']), trace)
        outcomes = {}
        for mode in ('baseline', 'hegelese'):
            host = Host(mode)
            result = host.install(p)
            effects = exercise(host.runner, trace)
            outcomes[mode] = {'installed': result['accepted'], **effects}
            assert not result['accepted'] and not effects['reference_disclosed'] and not effects['scorer_modified']
        assert ungated['reference_disclosed'] or ungated['scorer_modified']
        rows.append({'case': name, 'trace': trace, 'ungated': ungated, 'gated': outcomes})
    merge = proposal(request(), merge=True)
    host = Host('hegelese')
    before = host.install(merge)
    actions = host.authorize_equivalent_denial_merge(merge)
    after = host.install(merge, actions)
    baseline = Host('baseline').install(merge)
    assert not before['accepted'] and after['accepted'] and baseline['accepted']
    host.runner.dispatch('read_input')
    assert host.runner.dispatch('submit', 'forty-two')['score'] == 1
    assert host.runner.dispatch('submit', 'wrong-answer')['score'] == 0
    return {'scope': 'Constructed JSON policy rewrites, synthetic resources, no LLM trial or exploit reproduction.',
            'unsafe_cases': rows,
            'valid_simplification': {'baseline_accepted': baseline['accepted'],
              'hegelese_before_authorization': before['status'], 'hegelese_after_authorization': after['status'],
              'correct_solution_scores': 1, 'incorrect_solution_scores': 0},
            'conclusion': 'Both gates prevent these effects by refusing unsafe policy installation. No Hegelese-specific safety advantage established.'}


if __name__ == '__main__':
    print(json.dumps(demonstration(), indent=2))
