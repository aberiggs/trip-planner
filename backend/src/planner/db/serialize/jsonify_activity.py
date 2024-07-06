"""Module providing function to jsonify activities"""


def jsonify_activity(activity):
    """Function that jsonify activity"""

    activity["start_time"] = activity["start_time"].strftime("%m/%d/%y %H:%M:%S")
    activity["end_time"] = activity["end_time"].strftime("%m/%d/%y %H:%M:%S")
    activity["name"] = activity["name"]
    activity["note"] = activity["note"]
    activity["activity_id"] = str(activity["_id"])
    activity["plan_id"] = str(activity["plan_id"])
    activity.pop("_id")

    return activity
