"""Executable milestones: unnamed loss, forgotten history, checked repair.

Run: python3 examples/lineage_demo.py
No files are written. The caller retains history outside the proposer.
"""
import copy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import hegelese as h
import hgl_lineage as lineage


def main():
    request = json.loads((ROOT / 'request-four.json').read_text())
    proposal = json.loads((ROOT / 'proposal-four.json').read_text())
    request['source']['observations'] = {}
    request['required_observations'] = []
    proposal['target']['observations'] = {}
    proposal['dispositions'] = {k: v for k, v in proposal['dispositions'].items() if k in ('initial', 'step')}
    proposal['request_sha256'] = h.digest(request)
    plain = h.check(request, proposal)
    assert plain['accepted']
    assert plain['structural_loss']['erased_pairs'] == 2
    print('ordinary preservation check:', plain['status'])
    print('computed losses, with NO named observations:',
          [f['states'] for f in plain['structural_loss']['groups']])

    history = lineage.empty_history(request)
    first = lineage.check_lineage(request, lineage.successor(proposal, history), history)
    assert first['status'] == 'Unknown'
    print('unaccounted losses:', first['status'])
    history = first['next_history']  # Host retains even unsuccessful attempts.

    repaired = copy.deepcopy(proposal)
    repaired['target'] = copy.deepcopy(request['source'])
    repaired['mapping'] = {s: s for s in request['source']['states']}
    forgotten = lineage.check_lineage(request, lineage.successor(repaired, history), history)
    assert forgotten['status'] == 'Unknown'
    print('repaired map, but forgotten accounting:', forgotten['status'])
    history = forgotten['next_history']

    resolutions = {f['id']: {'action': 'repair', 'reason': 'Keep the phase distinctions in the target.'}
                   for f in plain['structural_loss']['groups']}
    final = lineage.check_lineage(request, lineage.successor(repaired, history, resolutions), history)
    assert final['accepted']
    assert all(f['status'] == 'Repaired' for f in final['loss_accounting'])
    print('repaired successor:', final['status'])
    print('The repair preserves four states; it does not claim the original compression succeeded.')


if __name__ == '__main__':
    main()
