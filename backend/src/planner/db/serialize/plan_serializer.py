"""Module providing serializer for plans"""

def plan_serializer(plan):
    """Function that serializes plan"""

    plan["date"] = plan["date"].strftime("%m/%d/%y")
    plan["owner"] = str(plan["owner"])
    plan["plan_id"] = str(plan["_id"])
    plan.pop("_id")
    members_str = []
    for member in plan["members"]:
        members_str.append(str(member))
    plan["members"] = members_str
    return plan
