import os
import sys
import json
import cv2 as cv
import numpy as np
from collections.abc import Iterable
from imutils.object_detection import non_max_suppression


def recursive_len(item):
    if isinstance(item, Iterable):
        return sum(recursive_len(subitem) for subitem in item)
    else:
        return 1


def get_role(job: str):
    roles = {
        "melee": ["rpr", "drg", "vpr", "nin", "mnk"],
        "caster": ["blm", "rdm", "blu", "pct", "smn"],
        "tank": ["drk", "gnb", "pld", "war"],
        "healer": ["ast", "sch", "sge", "whm"],
        "ranged": ["dnc", "brd", "mch"],
    }

    for role in roles:
        if job in roles[role]:
            return role
    print("[!] Invalid job! Please use the job shorthand name. Ex: sge, blm, rpr")
    exit(1)


def detect_actions(opener: str, job: str, role: str) -> list:
    """Given an opener, returns which actions are used in it"""
    job_path = f"actions/{role}/{job}"
    opener = cv.imread(f"{opener}", cv.IMREAD_GRAYSCALE)
    assert opener is not None, "file could not be read, check with os.path.exists()"
    op = opener.copy()
    skill_list = os.listdir(job_path)
    actions = {}
    for skill in skill_list:
        template = cv.imread(f"{job_path}/{skill}", cv.IMREAD_GRAYSCALE)
        assert (
            template is not None
        ), "file could not be read, check with os.path.exists()"
        img = op.copy()
        method = getattr(cv, "TM_CCOEFF_NORMED")
        # Apply template Matching
        res = cv.matchTemplate(img, template, method)

        threshold = 0.8
        (yCoords, xCoords) = np.where(res >= threshold)
        # Perform non-maximum suppression.
        template_h, template_w = template.shape[:2]
        rects = []
        for x, y in zip(xCoords, yCoords):
            rects.append((x, y, x + template_w, y + template_h))
        pick = non_max_suppression(np.array(rects))

        if recursive_len(pick) > 0:
            skillname = skill.split(".")[0]
            actions[skillname] = pick
    a = []
    for skill_name in actions.keys():
        a += [
            (skill_name, (int((a[0] + a[2]) / 2), int((a[1] + a[3]) / 2)))
            for a in actions[skill_name]
        ]
    actions = sorted(
        a, key=lambda tup: tup[1][0]
    )  # Sort by x coord -> Left to Right in the opener timeline
    return [a[0] for a in actions]


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            """Incorrect number of arguments.
Usage:
    python3 ocrt <job> <opener_filepath>"""
        )
        exit(0)
    opener = sys.argv[2]
    job = sys.argv[1].lower()
    if os.path.isfile(f"{opener}"):
        print("[-] This may take a bit.")
        actions = detect_actions(opener, job, get_role(job))
        out = {}
        out[job] = actions
        with open(f"output/{job.lower()}_opener.json", "w+") as f:
            f.write(json.dumps(out))
        print(f"[-] Done! {job.upper()} Opener saved to output/{job}_actions.json. ")
        # print(actions)
    else:
        print("[!] Opener not found!\nUsage:\n    python3 ocrt <opener_filepath>")
        exit(0)