"""Small deterministic comparison, NOT an AI efficacy benchmark.

Run from repository root: python3 experiments/workflow_comparison.py
The same finite tables are executed and checked; no model extraction is claimed.
"""
from collections import deque
from copy import deepcopy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import hegelese as h
import hgl_lineage as lineage


class Workflow:
    """Minimal table interpreter, not a production authorization boundary.

    Inputs are already classified events. Authentication, concurrency and effects
    are outside this experiment. Copying prevents later candidate table mutation.
    """
    def __init__(self, table):
        self.table = deepcopy(table)
        self.state = self.table['initial']

    def dispatch(self, event):
        self.state = self.table['transitions'][self.state][event]
        return self.observe()

    def observe(self):
        return {name: values[self.state]
                for name, values in self.table['observations'].items()}


def trace_check(source, target, obligations):
    """Independent finite trace-equivalence baseline, all reachable pairs.

    No candidate mapping or Hegelese checker is used. BFS returns a shortest
    counterexample trace. The caller protects obligations, including previously
    promised observations, outside candidate control. This is stronger than a
    sampled regression suite for these deterministic finite tables.
    """
    queue = deque([(source['initial'], target['initial'], [])])
    seen = set()
    while queue:
        left, right, trace = queue.popleft()
        if (left, right) in seen:
            continue
        seen.add((left, right))
        for name in sorted(obligations):
            expected = source['observations'][name][left]
            table = target['observations'].get(name)
            actual = None if table is None else table[right]
            if table is None or type(expected) is not type(actual) or expected != actual:
                return {'accepted': False, 'trace': trace, 'observation': name,
                        'expected': expected, 'actual': actual,
                        'reachable_pairs_checked': len(seen)}
        for event in source['inputs']:
            queue.append((source['transitions'][left][event],
                          target['transitions'][right][event], trace + [event]))
    return {'accepted': True, 'trace': None, 'reachable_pairs_checked': len(seen)}


def request():
    r = json.loads((ROOT / 'pilot/request.json').read_text())
    s = r['source']
    s['inputs'].append('cancel')
    s['states'].append('cancelled')
    for state, row in s['transitions'].items():
        row['cancel'] = 'cancelled' if state in ('draft', 'editor_review', 'owner_review') else state
    s['transitions']['cancelled'] = {event: 'cancelled' for event in s['inputs']}
    s['transitions']['cancelled']['reset'] = 'draft'
    s['observations']['publicStatus']['cancelled'] = 'cancelled'
    s['observations']['canPublish']['cancelled'] = False
    s['observations']['reviewRoute']['cancelled'] = 'cancelled'
    return r


def proposal(r, merge=False):
    source = r['source']
    mapping = {s: 'review' if merge and s in ('editor_review', 'owner_review') else s
               for s in source['states']}
    target = deepcopy(source)
    target['states'] = sorted(set(mapping.values()))
    target['transitions'] = {mapping[s]: {e: mapping[t] for e, t in row.items()}
                             for s, row in source['transitions'].items()}
    names = r['required_observations'] if merge else source['observations']
    target['observations'] = {name: {mapping[s]: value for s, value in source['observations'][name].items()}
                              for name in names}
    return {'schema': 'hegelese-proposal/0.1', 'operation': 'upheave',
            'request_sha256': h.digest(r),
            'occasion': {'kind': 'Rearticulation', 'explanation': 'Simplify an executable approval workflow.'},
            'target': target, 'mapping': mapping,
            'dispositions': {name: {'action': 'withdraw' if merge and name == 'observation:reviewRoute' else 'retain',
                                    'reason': 'Keep required behavior; optionally remove route identity.'}
                             for name in ['initial', 'step'] + ['observation:' + n for n in source['observations']]},
            'assumptions': []}


def run_case(name, r, p, prior=None, authorize=False):
    # Freeze caller-owned request/obligations independently of the candidate.
    obligations = set(r['required_observations'])
    history = lineage.empty_history(r)
    if prior is not None:
        first = lineage.check_lineage(r, lineage.successor(prior, history), history)
        history = first['next_history']
        obligations.update(n for n in r['source']['observations']
                           if prior['dispositions']['observation:' + n]['action'] == 'retain')
    obligations.update(n for n in r['source']['observations']
                       if p['dispositions']['observation:' + n]['action'] == 'retain')
    resolutions = {}
    if authorize:
        for finding in h.structural_losses(r['source'], p['mapping'])['groups']:
            history['authorized_losses'][finding['id']] = 'Host permits route identity loss; public behavior remains required.'
            resolutions[finding['id']] = {'action': 'accept_loss', 'reason': 'Use host-authorized abstraction.'}
    finite = h.check(r, p)
    checked = lineage.check_lineage(r, lineage.successor(p, history, resolutions), history)
    baseline = trace_check(r['source'], p['target'], obligations)
    # Replay every baseline counterexample through the actual table interpreter.
    if not baseline['accepted']:
        old, new = Workflow(r['source']), Workflow(p['target'])
        for event in baseline['trace']:
            old.dispatch(event)
            new.dispatch(event)
        obs = baseline['observation']
        assert obs not in new.observe() or type(old.observe()[obs]) is not type(new.observe()[obs]) or old.observe()[obs] != new.observe()[obs]
    return {'case': name, 'required_and_inherited_observations': sorted(obligations),
            'trace_baseline': baseline, 'ordinary_finite_check': finite['status'],
            'lineage': checked['status'], 'lineage_accepted': checked['accepted'],
            'accounting': [x['status'] for x in checked.get('loss_accounting', [])]}


def compare():
    r = request()
    identity, merge = proposal(r), proposal(r, True)
    bypass = deepcopy(identity)
    bypass['target']['transitions']['draft']['approve'] = 'approved'
    cancel_bug = deepcopy(identity)
    cancel_bug['target']['transitions']['cancelled']['approve'] = 'approved'
    rows = [run_case('unchanged workflow', r, identity),
            run_case('useful route merge, no loss authorization', r, merge),
            run_case('useful route merge, explicit authorization', r, merge, authorize=True),
            run_case('approval bypass from draft', r, bypass),
            run_case('approval after cancellation', r, cancel_bug),
            run_case('withdraw previously retained route', r, merge, prior=identity, authorize=True)]
    return {'scope': 'Six hand-authored deterministic cases; no LLM runs, statistical claims, or external deployment.',
            'cases': rows,
            'conclusion': 'Both methods catch these behavioral failures. Lineage adds explicit structural-loss accounting; no detection advantage is demonstrated.'}


if __name__ == '__main__':
    print(json.dumps(compare(), indent=2))
