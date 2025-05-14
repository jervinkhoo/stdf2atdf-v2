# src/core/atdf_generator/templates.py
"""
Contains ATDF record structure definitions (ATDF_TEMPLATES) and
utility functions for accessing and using these templates during generation.
"""
# Note: No external imports needed for this specific content,
# as ATDF_TEMPLATES is defined here and used by the functions.
# If logging were used in get_atdf_template, it would be added.

# Copied from src/core/atdf/templates.py
ATDF_TEMPLATES = {
    "FAR": {
        "data_file_type": {"stdf": "cpu_type", "value": None, "req": True},
        "stdf_version": {"stdf": "stdf_ver", "value": None, "req": True},
        "atdf_version": {"stdf": None, "value": None, "req": True},
        "scaling_flag": {"stdf": None, "value": None, "req": False}
    },
    "ATR": {
        "modification_timestamp": {"stdf": "mod_tim", "value": None, "req": False},
        "command_line": {"stdf": "cmd_line", "value": None, "req": False}
    },
    "MIR": {
        "lot_id": {"stdf": "lot_id", "value": None, "req": True},
        "part_type": {"stdf": "part_typ", "value": None, "req": True},
        "job_name": {"stdf": "job_nam", "value": None, "req": True},
        "node_id": {"stdf": "node_nam", "value": None, "req": True},
        "tester_type": {"stdf": "tstr_typ", "value": None, "req": True},
        "setup_time": {"stdf": "setup_t", "value": None, "req": True},
        "start_time": {"stdf": "start_t", "value": None, "req": True},
        "operator_name": {"stdf": "oper_nam", "value": None, "req": True},
        "test_mode": {"stdf": "mode_cod", "value": None, "req": True},
        "station_number": {"stdf": "stat_num", "value": None, "req": True},
        "sublot_id": {"stdf": "sblot_id", "value": None, "req": False},
        "test_code": {"stdf": "test_cod", "value": None, "req": False},
        "retest_code": {"stdf": "rtst_cod", "value": None, "req": False},
        "job_revision": {"stdf": "job_rev", "value": None, "req": False},
        "executive_type": {"stdf": "exec_typ", "value": None, "req": False},
        "executive_version": {"stdf": "exec_ver", "value": None, "req": False},
        "protect_code": {"stdf": "prot_cod", "value": None, "req": False},
        "command_mode": {"stdf": "cmod_cod", "value": None, "req": False},
        "burn_in_time": {"stdf": "burn_tim", "value": None, "req": False},
        "test_temp": {"stdf": "tst_temp", "value": None, "req": False},
        "user_text": {"stdf": "user_txt", "value": None, "req": False},
        "auxiliary_file": {"stdf": "aux_file", "value": None, "req": False},
        "package_type": {"stdf": "pkg_typ", "value": None, "req": False},
        "family_id": {"stdf": "famly_id", "value": None, "req": False},
        "date_code": {"stdf": "date_cod", "value": None, "req": False},
        "facility_id": {"stdf": "facil_id", "value": None, "req": False},
        "floor_id": {"stdf": "floor_id", "value": None, "req": False},
        "process_id": {"stdf": "proc_id", "value": None, "req": False},
        "operation_frequency": {"stdf": "oper_frq", "value": None, "req": False},
        "specification_name": {"stdf": "spec_nam", "value": None, "req": False},
        "specification_version": {"stdf": "spec_ver", "value": None, "req": False},
        "flow_id": {"stdf": "flow_id", "value": None, "req": False},
        "setup_id": {"stdf": "setup_id", "value": None, "req": False},
        "design_revision": {"stdf": "dsgn_rev", "value": None, "req": False},
        "engineering_lot_id": {"stdf": "eng_id", "value": None, "req": False},
        "rom_code_id": {"stdf": "rom_cod", "value": None, "req": False},
        "serial_number": {"stdf": "serl_num", "value": None, "req": False},
        "super_name": {"stdf": "supr_nam", "value": None, "req": False}
    },
    "MRR": {
        "finish_time": {"stdf": "finish_t", "value": None, "req": True},
        "disposition": {"stdf": "disp_cod", "value": None, "req": False},
        "user_description": {"stdf": "usr_desc", "value": None, "req": False},
        "executive_description": {"stdf": "exc_desc", "value": None, "req": False}
    },
    "PCR": {
        "head_number": {"stdf": "head_num", "value": None, "req": None},
        "site_number": {"stdf": "site_num", "value": None, "req": None},
        "part_count": {"stdf": "part_cnt", "value": None, "req": True},
        "retest_count": {"stdf": "rtst_cnt", "value": None, "req": False},
        "abort_count": {"stdf": "abrt_cnt", "value": None, "req": False},
        "good_count": {"stdf": "good_cnt", "value": None, "req": False},
        "funct_count": {"stdf": "func_cnt", "value": None, "req": False}
    },
    "HBR": {
        "head_number": {"stdf": "head_num", "value": None, "req": None},
        "site_number": {"stdf": "site_num", "value": None, "req": None},
        "bin_number": {"stdf": "hbin_num", "value": None, "req": True},
        "bin_count": {"stdf": "hbin_cnt", "value": None, "req": True},
        "pass_or_fail": {"stdf": "hbin_pf", "value": None, "req": False},
        "bin_name": {"stdf": "hbin_nam", "value": None, "req": False}
    },
    "SBR": {
        "head_number": {"stdf": "head_num", "value": None, "req": None},
        "site_number": {"stdf": "site_num", "value": None, "req": None},
        "bin_number": {"stdf": "sbin_num", "value": None, "req": True},
        "bin_count": {"stdf": "sbin_cnt", "value": None, "req": True},
        "pass_or_fail": {"stdf": "sbin_pf", "value": None, "req": False},
        "bin_name": {"stdf": "sbin_nam", "value": None, "req": False}
    },
    "PMR": {
        "pmr_index": {"stdf": "pmr_indx", "value": None, "req": True},
        "channel_type": {"stdf": "chan_typ", "value": None, "req": False},
        "channel_name": {"stdf": "chan_nam", "value": None, "req": False},
        "pin_name": {"stdf": "phy_nam", "value": None, "req": False},
        "logical_name": {"stdf": "log_nam", "value": None, "req": False},
        "head_number": {"stdf": "head_num", "value": None, "req": False},
        "site_number": {"stdf": "site_num", "value": None, "req": False}
    },
    "PGR": {
        "group_index": {"stdf": "grp_indx", "value": None, "req": True},
        "group_name": {"stdf": "grp_nam", "value": None, "req": False},
        "index_array": {"stdf": "pmr_indx", "value": None, "req": False}
    },
    "PLR": {
        "index_array": {"stdf": "grp_indx", "value": None, "req": True},
        "mode_array": {"stdf": "grp_mode", "value": None, "req": False},
        "radix_array": {"stdf": "grp_radx", "value": None, "req": False},
        "programmed_state": {"stdf": ("pgm_chal", "pgm_char"), "value": None, "req": False},
        "returned_state": {"stdf": ("rtn_chal", "rtn_char"), "value": None, "req": False}
    },
    "RDR": {
        "retest_bins": {"stdf": "rtst_bin", "value": None, "req": True}
    },
    "SDR": {
        "head_number": {"stdf": "head_num", "value": None, "req": True},
        "site_group": {"stdf": "site_grp", "value": None, "req": True},
        "site_array": {"stdf": "site_num", "value": None, "req": True},
        "handler_type": {"stdf": "hand_typ", "value": None, "req": False},
        "handler_id": {"stdf": "hand_id", "value": None, "req": False},
        "card_type": {"stdf": "card_typ", "value": None, "req": False},
        "card_id": {"stdf": "card_id", "value": None, "req": False},
        "load_type": {"stdf": "load_typ", "value": None, "req": False},
        "load_id": {"stdf": "load_id", "value": None, "req": False},
        "dib_type": {"stdf": "dib_typ", "value": None, "req": False},
        "dib_id": {"stdf": "dib_id", "value": None, "req": False},
        "cable_type": {"stdf": "cabl_typ", "value": None, "req": False},
        "cable_id": {"stdf": "cabl_id", "value": None, "req": False},
        "contractor_type": {"stdf": "cont_typ", "value": None, "req": False},
        "contractor_id": {"stdf": "cont_id", "value": None, "req": False},
        "laser_type": {"stdf": "lasr_typ", "value": None, "req": False},
        "laser_id": {"stdf": "lasr_id", "value": None, "req": False},
        "extra_type": {"stdf": "extr_typ", "value": None, "req": False},
        "extra_id": {"stdf": "extr_id", "value": None, "req": False}
    },
    "WIR": {
        "head_number": {"stdf": "head_num", "value": None, "req": True},
        "start_time": {"stdf": "start_t", "value": None, "req": True},
        "site_group": {"stdf": "site_grp", "value": None, "req": False},
        "wafer_id": {"stdf": "wafer_id", "value": None, "req": False}
    },
    "WRR": {
        "head_number": {"stdf": "head_num", "value": None, "req": True},
        "finish_time": {"stdf": "finish_t", "value": None, "req": True},
        "part_count": {"stdf": "part_cnt", "value": None, "req": True},
        "wafer_id": {"stdf": "wafer_id", "value": None, "req": False},
        "site_group": {"stdf": "site_grp", "value": None, "req": False},
        "retest_count": {"stdf": "rtst_cnt", "value": None, "req": False},
        "abort_count": {"stdf": "abrt_cnt", "value": None, "req": False},
        "good_count": {"stdf": "good_cnt", "value": None, "req": False},
        "functional_count": {"stdf": "func_cnt", "value": None, "req": False},
        "fab_wafer_id": {"stdf": "fabwf_id", "value": None, "req": False},
        "frame_id": {"stdf": "frame_id", "value": None, "req": False},
        "mask_id": {"stdf": "mask_id", "value": None, "req": False},
        "user_description": {"stdf": "usr_desc", "value": None, "req": False},
        "executive_description": {"stdf": "exc_desc", "value": None, "req": False}
    },
    "WCR": {
        "wafer_flat": {"stdf": "wf_flat", "value": None, "req": False},
        "positive_x": {"stdf": "pos_x", "value": None, "req": False},
        "positive_y": {"stdf": "pos_y", "value": None, "req": False},
        "wafer_size": {"stdf": "wafr_siz", "value": None, "req": False},
        "die_height": {"stdf": "die_ht", "value": None, "req": False},
        "die_width": {"stdf": "die_wid", "value": None, "req": False},
        "wafer_units": {"stdf": "wf_units", "value": None, "req": False},
        "center_x": {"stdf": "center_x", "value": None, "req": False},
        "center_y": {"stdf": "center_y", "value": None, "req": False}
    },
    "PIR": {
        "head_number": {"stdf": "head_num", "value": None, "req": True},
        "site_number": {"stdf": "site_num", "value": None, "req": True}
    },
    "PRR": {
        "head_number": {"stdf": "head_num", "value": None, "req": True},
        "site_number": {"stdf": "site_num", "value": None, "req": True},
        "part_id": {"stdf": "part_id", "value": None, "req": None},
        "number_of_tests": {"stdf": "num_test", "value": None, "req": True},
        "pass_fail_code": {"stdf": "part_flg", "value": None, "req": None},
        "hardware_bin": {"stdf": "hard_bin", "value": None, "req": True},
        "software_bin": {"stdf": "soft_bin", "value": None, "req": False},
        "x_coordinate": {"stdf": "x_coord", "value": None, "req": False},
        "y_coordinate": {"stdf": "y_coord", "value": None, "req": False},
        "retest_code": {"stdf": "part_flg", "value": None, "req": False},
        "abort_code": {"stdf": "part_flg", "value": None, "req": False},
        "test_time": {"stdf": "test_t", "value": None, "req": False},
        "part_text": {"stdf": "part_txt", "value": None, "req": False},
        "part_fix_data": {"stdf": "part_fix", "value": None, "req": False}
    },
    "TSR": {
        "head_number": {"stdf": "head_num", "value": None, "req": None},
        "site_number": {"stdf": "site_num", "value": None, "req": None},
        "test_number": {"stdf": "test_num", "value": None, "req": True},
        "test_name": {"stdf": "test_nam", "value": None, "req": False},
        "test_type": {"stdf": "test_typ", "value": None, "req": False},
        "execute_count": {"stdf": "exec_cnt", "value": None, "req": False},
        "fail_count": {"stdf": "fail_cnt", "value": None, "req": False},
        "alarm_count": {"stdf": "alrm_cnt", "value": None, "req": False},
        "sequencer_name": {"stdf": "seq_name", "value": None, "req": False},
        "test_label": {"stdf": "test_lbl", "value": None, "req": False},
        "test_time": {"stdf": "test_tim", "value": None, "req": False},
        "test_min": {"stdf": "test_min", "value": None, "req": False},
        "test_max": {"stdf": "test_max", "value": None, "req": False},
        "test_sums": {"stdf": "tst_sums", "value": None, "req": False},
        "test_squares": {"stdf": "tst_sqrs", "value": None, "req": False}
    },
    "PTR": {
        "test_number": {"stdf": "test_num", "value": None, "req": True},
        "head_number": {"stdf": "head_num", "value": None, "req": True},
        "site_number": {"stdf": "site_num", "value": None, "req": True},
        "test_result": {"stdf": "result", "value": None, "req": False},
        "pass_fail_flag": {"stdf": ("test_flg", "parm_flg"), "value": None, "req": True},
        "alarm_flags": {"stdf": ("test_flg", "parm_flg"), "value": None, "req": False},
        "test_text": {"stdf": "test_txt", "value": None, "req": False},
        "alarm_id": {"stdf": "alarm_id", "value": None, "req": False},
        "limit_compare": {"stdf": "parm_flg", "value": None, "req": False},
        "test_units": {"stdf": "units", "value": None, "req": False},
        "low_limit": {"stdf": "lo_limit", "value": None, "req": False},
        "high_limit": {"stdf": "hi_limit", "value": None, "req": False},
        "result_format": {"stdf": "c_resfmt", "value": None, "req": False},
        "low_limit_format": {"stdf": "c_llmfmt", "value": None, "req": False},
        "high_limit_format": {"stdf": "c_hlmfmt", "value": None, "req": False},
        "low_specification_limit": {"stdf": "lo_spec", "value": None, "req": False},
        "high_specification_limit": {"stdf": "hi_spec", "value": None, "req": False},
        "result_scale": {"stdf": "res_scal", "value": None, "req": False},
        "low_limit_scale": {"stdf": "llm_scal", "value": None, "req": False},
        "high_limit_scale": {"stdf": "hlm_scal", "value": None, "req": False}
    },
    "MPR": {
        "test_number": {"stdf": "test_num", "value": None, "req": True},
        "head_number": {"stdf": "head_num", "value": None, "req": True},
        "site_number": {"stdf": "site_num", "value": None, "req": True},
        "states_array": {"stdf": "rtn_stat", "value": None, "req": False},
        "results_array": {"stdf": "rtn_rslt", "value": None, "req": False},
        "pass_fail_flag": {"stdf": ("test_flg", "parm_flg"), "value": None, "req": True},
        "alarm_flags": {"stdf": ("test_flg", "parm_flg"), "value": None, "req": False},
        "test_text": {"stdf": "test_txt", "value": None, "req": False},
        "alarm_id": {"stdf": "alarm_id", "value": None, "req": False},
        "limit_compare": {"stdf": "parm_flg", "value": None, "req": False},
        "test_units": {"stdf": "units", "value": None, "req": False},
        "low_limit": {"stdf": "lo_limit", "value": None, "req": False},
        "high_limit": {"stdf": "hi_limit", "value": None, "req": False},
        "starting_value": {"stdf": "start_in", "value": None, "req": False},
        "increment": {"stdf": "incr_in", "value": None, "req": False},
        "input_units": {"stdf": "units_in", "value": None, "req": False},
        "index_array": {"stdf": "rtn_indx", "value": None, "req": False},
        "result_format": {"stdf": "c_resfmt", "value": None, "req": False},
        "low_limit_format": {"stdf": "c_llmfmt", "value": None, "req": False},
        "high_limit_format": {"stdf": "c_hlmfmt", "value": None, "req": False},
        "low_specification_limit": {"stdf": "lo_spec", "value": None, "req": False},
        "high_specification_limit": {"stdf": "hi_spec", "value": None, "req": False},
        "result_scale": {"stdf": "res_scal", "value": None, "req": False},
        "low_limit_scale": {"stdf": "llm_scal", "value": None, "req": False},
        "high_limit_scale": {"stdf": "hlm_scal", "value": None, "req": False}
    },
    "FTR": {
        "test_number": {"stdf": "test_num", "value": None, "req": True},
        "head_number": {"stdf": "head_num", "value": None, "req": True},
        "site_number": {"stdf": "site_num", "value": None, "req": True},
        "pass_fail_flag": {"stdf": "test_flg", "value": None, "req": True},
        "alarm_flags": {"stdf": "test_flg", "value": None, "req": False},
        "vector_name": {"stdf": "vect_nam", "value": None, "req": False},
        "timing_set": {"stdf": "time_set", "value": None, "req": False},
        "cycle_count": {"stdf": "cycl_cnt", "value": None, "req": False},
        "relative_address": {"stdf": "rel_vadr", "value": None, "req": False},
        "repeat_count": {"stdf": "rept_cnt", "value": None, "req": False},
        "failing_bits": {"stdf": "num_fail", "value": None, "req": False},
        "x_fail_address": {"stdf": "xfail_ad", "value": None, "req": False},
        "y_fail_address": {"stdf": "yfail_ad", "value": None, "req": False},
        "vector_offset": {"stdf": "vect_off", "value": None, "req": False},
        "returned_indexes": {"stdf": "rtn_indx", "value": None, "req": False},
        "returned_states": {"stdf": "rtn_stat", "value": None, "req": False},
        "programmed_state_indexes": {"stdf": "pgm_indx", "value": None, "req": False},
        "programmed_states": {"stdf": "pgm_stat", "value": None, "req": False},
        "failing_pins": {"stdf": "fail_pin", "value": None, "req": False},
        "vector_op_code": {"stdf": "op_code", "value": None, "req": False},
        "test_text": {"stdf": "test_txt", "value": None, "req": False},
        "alarm_id": {"stdf": "alarm_id", "value": None, "req": False},
        "programmed_text": {"stdf": "prog_txt", "value": None, "req": False},
        "result_text": {"stdf": "rslt_txt", "value": None, "req": False},
        "generator_number": {"stdf": "patg_num", "value": None, "req": False},
        "comparators": {"stdf": "spin_map", "value": None, "req": False}
    },
    "BPS": {
        "sequencer_name": {"stdf": "seq_name", "value": None, "req": False}
    },
    "EPS": {},
    "GDR": {
        "generic_data": {"stdf": "gen_data", "value": None, "req": False}
    },
    "DTR": {
        "text_data": {"stdf": "text_dat", "value": None, "req": False}
    },
}
# Functions moved from src/core/utils/templates.py
def create_atdf_template(record_type):
    # Uses ATDF_TEMPLATES defined above in this file
    if record_type not in ATDF_TEMPLATES:
        raise ValueError(f"No template found for ATDF record type {record_type}")
    
    return {
        "record_type": record_type,
        "header": f"{record_type}:",
        "fields": ATDF_TEMPLATES[record_type].copy()
    }

def get_atdf_template(record_type: str) -> dict:
    # Uses create_atdf_template defined above in this file
    try:
        return create_atdf_template(record_type)
    except ValueError as e:
        message = f"Template for '{record_type}' not found."
        #logging.error(message) # Original code had logging commented out
        raise ValueError(message)