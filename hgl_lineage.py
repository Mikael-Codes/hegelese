"""Caller-retained revision history for a fixed finite Hegelese source/request.

No evidence receipt is trusted. Historical inputs are validated again; their
structural findings and observation obligations are derived again. The host
must retain history and authorizations independently of the candidate author.
"""
import copy

import hegelese as h

SCHEMA = "hegelese-lineage/0.1"
CANDIDATE = "hegelese-successor/0.1"
MAX_ATTEMPTS = 32


def empty_history(request):
    return {"schema": SCHEMA, "request_sha256": h.digest(request),
            "attempts": [], "authorized_losses": {}}


def successor(proposal, history, resolutions=None):
    return {"schema": CANDIDATE, "history_sha256": h.digest(history),
            "proposal": copy.deepcopy(proposal), "resolutions": resolutions or {}}


def check_lineage(request, candidate, history, budget=100000):
    """A fresh check, including all inherited observations and structural losses.

    Deliberately supports revisions against one immutable request, not chains
    of different source programs. History is a caller-owned input, not a store
    controlled by this function. The next history is returned, never saved.
    """
    try:
        h.fields(history, "schema request_sha256 attempts authorized_losses", "/history")
        h.require(history["schema"] == SCHEMA, "/history/schema", "Unsupported history schema.")
        h.require(history["request_sha256"] == h.digest(request), "/history/request_sha256",
                  "History belongs to a different request; scope changes cannot silently reset it.")
        attempts = history["attempts"]
        h.require(type(attempts) is list and len(attempts) < MAX_ATTEMPTS, "/history/attempts",
                  "Expected fewer than 32 prior attempts; explicit archival/migration is not yet supported.")
        h.fields(candidate, "schema history_sha256 proposal resolutions", "/candidate")
        h.require(candidate["schema"] == CANDIDATE, "/candidate/schema", "Unsupported successor schema.")
        h.require(candidate["history_sha256"] == h.digest(history), "/candidate/history_sha256",
                  "Successor must bind the exact independently retained history.")
        proposal = candidate["proposal"]
        h.validate(request, proposal, budget)
        prior_proposals = []
        for i, attempt in enumerate(attempts):
            path = f"/history/attempts/{i}"
            h.fields(attempt, "proposal budget resolutions", path)
            h.require(type(attempt["resolutions"]) is dict, path + "/resolutions", "Expected historical resolution declarations.")
            for resolution in attempt["resolutions"].values():
                h.fields(resolution, "action reason", path + "/resolutions")
                h.require(resolution["action"] in ("repair", "carry", "accept_loss"), path + "/resolutions", "Invalid historical resolution action.")
                h.words(resolution["reason"], path + "/resolutions")
            h.validate(request, attempt["proposal"], attempt["budget"])
            prior_proposals.append(attempt["proposal"])
        source = request["source"]
        findings = {}
        observations = set()
        assumptions = set()
        for p in prior_proposals + [proposal]:
            for finding in h.structural_losses(source, p["mapping"])["groups"]:
                findings.setdefault(finding["id"], finding)
            observations.update(name for name in source["observations"]
                                if p["dispositions"]["observation:" + name]["action"] == "retain")
            assumptions.update(p["assumptions"])
        authorized = history["authorized_losses"]
        h.require(type(authorized) is dict, "/history/authorized_losses", "Expected finding IDs and authorization reasons.")
        for fid, reason in authorized.items():
            h.require(fid in findings, "/history/authorized_losses", "Authorization names an unknown finding.")
            h.words(reason, "/history/authorized_losses/" + fid)
        resolutions = candidate["resolutions"]
        h.require(type(resolutions) is dict and set(resolutions) <= set(findings),
                  "/candidate/resolutions", "Resolutions must name derived finding IDs.")
        for fid, resolution in resolutions.items():
            h.fields(resolution, "action reason", "/candidate/resolutions/" + fid)
            h.require(resolution["action"] in ("repair", "carry", "accept_loss"),
                      "/candidate/resolutions/" + fid, "Expected repair, carry, or accept_loss.")
            h.words(resolution["reason"], "/candidate/resolutions/" + fid + "/reason")
    except h.Invalid as error:
        return {"checker": h.CHECKER, "status": "Invalid", "accepted": False,
                "diagnostics": [{"path": error.path, "message": error.message}]}

    # Each old group represents ALL its erased pairs. An injective restriction
    # repairs every pair, not merely the displayed witness. Current groups are
    # included too, so splitting one old merger cannot hide a different merger.
    accounting, failed, pending = [], False, False
    for fid, finding in sorted(findings.items()):
        seen, collision = {}, None
        for state in finding["states"]:
            target = proposal["mapping"][state]
            if target in seen:
                collision = [seen[target], state]
                break
            seen[target] = state
        action = resolutions.get(fid, {}).get("action")
        if action == "repair":
            status = "Repaired" if collision is None else "Refuted"
        elif action == "accept_loss":
            status = "AuthorizedLoss" if fid in authorized else "Unauthorized"
        elif action == "carry":
            status = "Unresolved"
        else:
            status = "Unaccounted"
        failed |= status in ("Refuted", "Unauthorized")
        pending |= status in ("Unresolved", "Unaccounted")
        accounting.append({"id": fid, "states": finding["states"], "status": status,
                           "collision": collision, "resolution": resolutions.get(fid),
                           "authorization": authorized.get(fid)})

    # Recheck ALL inherited observation equations, including ones a successor
    # marks withdrawn. Rechecking the full domain subsumes old counterexamples
    # and unfinished checks; no previous successful verdict buys an exemption.
    base = h.check(request, proposal, budget)
    remaining = budget - base["evidence"]["checks_completed"]
    extra = sorted(name for name in observations
                   if proposal["dispositions"]["observation:" + name]["action"] != "retain")
    total = len(extra) * len(source["states"])
    completed, failures, witnesses = 0, 0, []
    for name in extra:
        table = proposal["target"]["observations"].get(name)
        for state in source["states"]:
            if completed >= remaining:
                break
            completed += 1
            actual = None if table is None else table[proposal["mapping"][state]]
            expected = source["observations"][name][state]
            if table is None or h.canonical(expected) != h.canonical(actual):
                failures += 1
                if len(witnesses) < 10:
                    witnesses.append({"law": "inherited_observation", "observation": name,
                                      "state": state, "expected": expected, "actual": actual,
                                      "target_observation_missing": table is None})
    failed |= base["status"] == "Refuted" or failures > 0
    pending |= base["status"] == "Unknown" or completed < total or bool(assumptions)
    status = "Refuted" if failed else "Unknown" if pending else "ExhaustivelyChecked"
    updated = copy.deepcopy(history)
    updated["attempts"].append({"proposal": copy.deepcopy(proposal), "budget": budget,
                                "resolutions": copy.deepcopy(resolutions)})
    return {"checker": h.CHECKER, "protocol": CANDIDATE, "status": status,
            "accepted": status == "ExhaustivelyChecked", "history_sha256": h.digest(history),
            "candidate_sha256": h.digest(candidate), "base_check": base,
            "loss_accounting": accounting,
            "inherited_observations": sorted(observations),
            "inherited_checks": {"checks_total": total, "checks_completed": completed,
                                 "failures": failures, "counterexamples": witnesses,
                                 "counterexamples_omitted": max(0, failures - len(witnesses))},
            "unresolved_assumptions": sorted(assumptions),
            "next_history": updated, "next_history_sha256": h.digest(updated),
            "limits": ["Host must retain history and authorize losses independently; hashes are not authority.",
                       "Fixed source/request revision lineage only; no cross-source proof transport.",
                       "Structural losses concern this map, not all encodings or application relevance.",
                       "Inherited assumptions cannot be discharged by prose in this protocol.",
                       "Historical inputs are revalidated and obligations rederived; old verdicts are not trusted.",
                       "Structural passes are bounded separately from the shared equation budget."]}
