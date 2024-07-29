import cv2 as cv
import numpy as np
import os
from collections.abc import Iterable
from imutils.object_detection import non_max_suppression  #
import sys


def recursive_len(item):
    if isinstance(item, Iterable):
        return sum(recursive_len(subitem) for subitem in item)
    else:
        return 1


def has_match(inp):
    return recursive_len(inp) > 0


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


def detect_job(opener: str) -> str:
    """For a given opener (filename), will return the job it belongs to."""

    img = cv.imread(f"{opener}", cv.IMREAD_GRAYSCALE)
    assert img is not None, "file could not be read, check with os.path.exists()"
    img2 = img.copy()

    for class_icon in os.listdir("jobs"):
        template = cv.imread(f"jobs/{os.fsdecode(class_icon)}", cv.IMREAD_GRAYSCALE)
        assert (
            template is not None
        ), "file could not be read, check with os.path.exists()"
        w, h = template.shape[::-1]

        img = img2.copy()
        method = getattr(cv, "TM_CCOEFF_NORMED")

        # Apply template Matching
        res = cv.matchTemplate(img, template, method)
        threshold = 0.8
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            cv.rectangle(img, pt, (pt[0] + w, pt[1] + h), 255, 2)

        if has_match(loc):
            return os.fsdecode(class_icon).split(".")[0]


def detect_skills(opener: str, job: str, role: str) -> dict:
    """Given an opener, returns which skills are used in it"""
    job_path = f"skills/{role}/{job}"
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

        if has_match(pick):
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
    if len(sys.argv) < 2:
        print(
            """Insufficient arguments.
Usage:
    python3 ocrt <opener_filepath>"""
        )
        exit(0)
    opener = sys.argv[1]
    if os.path.isfile(f"{opener}"):
        print("[-] This may take a bit.")
        job = detect_job(opener)
        actions = detect_skills(opener, job, get_role(job))
    else:
        print("[!] Opener not found!\nUsage:\n    python3 ocrt <opener_filepath>")
        exit(0)
    print(actions)
