from caasm_adapter_base.util.adapter_fabric import fabric_util


def choose_new_record(records):
    return fabric_util.choose_record_by_last_seen(records)
