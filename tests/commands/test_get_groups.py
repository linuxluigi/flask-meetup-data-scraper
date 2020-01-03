import pytest
from meetup_search.commands.get_groups import get_groups
from typing import List, Dict


def test_get_groups():
    # load all groups from JSON test file
    groups_dict: Dict[str, List[str]] = get_groups(
        meetup_files_path="/app/compose/local/flask/meetup_groups"
    )

    assert len(groups_dict["valid"]) == 1
    assert len(groups_dict["invalid"]) == 2
