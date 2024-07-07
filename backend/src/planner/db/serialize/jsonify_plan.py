"""Module providing function to jsonify plans"""

def jsonify_plan(plan):
    """Function that jsonify plan"""

    plan["date"] = plan["date"].strftime("%m/%d/%y")
    plan["owner"] = str(plan["owner"])
    plan["plan_id"] = str(plan["_id"])
    plan.pop("_id")

    members_str = []
    for member in plan["members"]:
        members_str.append(str(member))
    plan["members"] = members_str

    activities_str = []
    for activity in plan["activities"]:
        activities_str.append(str(activity))
    plan["activities"] = activities_str

    return plan

def jsonify_expanded_plan(plan):
    """Function that jsonify expanded plan"""

    plan["date"] = plan["date"].strftime("%m/%d/%y")
    plan["plan_id"] = str(plan["_id"])
    plan.pop("_id")

    activities = []
    for activity in plan["activities"]:
        activity["activity_id"] = str(activity["activity_id"])
        activity["start_time"] = activity["start_time"].strftime("%m/%d/%y %H:%M:%S")
        activity["end_time"] = activity["end_time"].strftime("%m/%d/%y %H:%M:%S")
        activities.append(activity)
    plan["activities"] = activities

    return plan
