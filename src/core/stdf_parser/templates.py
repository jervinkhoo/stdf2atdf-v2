# src/core/stdf_parser/templates.py
"""
Contains STDF record structure definitions (STDF_TEMPLATES).
Moved from src/core/stdf/templates.py.
Utility functions for using these templates will be added later.
"""

STDF_TEMPLATES = {
    "FAR": {
        "rec_len": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "rec_typ": {"dtype": "U*1", "ref": None, "value": 0, "missing": None},  # Contains rec_typ value
        "rec_sub": {"dtype": "U*1", "ref": None, "value": 10, "missing": None}, # Contains rec_sub value
        "cpu_type": {"dtype": "U*1", "ref": None, "value": None, "missing": None},
        "stdf_ver": {"dtype": "U*1", "ref": None, "value": None, "missing": None}
    },
    "ATR": {
        "rec_len": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "rec_typ": {"dtype": "U*1", "ref": None, "value": 0, "missing": None},
        "rec_sub": {"dtype": "U*1", "ref": None, "value": 20, "missing": None},
        "mod_tim": {"dtype": "U*4", "ref": None, "value": None, "missing": None},
        "cmd_line": {"dtype": "C*n", "ref": None, "value": None, "missing": None}
    },
    "MIR": {
        "rec_len": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "rec_typ": {"dtype": "U*1", "ref": None, "value": 1, "missing": None},
        "rec_sub": {"dtype": "U*1", "ref": None, "value": 10, "missing": None},
        "setup_t": {"dtype": "U*4", "ref": None, "value": None, "missing": None},
        "start_t": {"dtype": "U*4", "ref": None, "value": None, "missing": None},
        "stat_num": {"dtype": "U*1", "ref": None, "value": None, "missing": None},
        "mode_cod": {"dtype": "C*1", "ref": None, "value": None, "missing": "space"},
        "rtst_cod": {"dtype": "C*1", "ref": None, "value": None, "missing": "space"},
        "prot_cod": {"dtype": "C*1", "ref": None, "value": None, "missing": "space"},
        "burn_tim": {"dtype": "U*2", "ref": None, "value": None, "missing": 65535},
        "cmod_cod": {"dtype": "C*1", "ref": None, "value": None, "missing": "space"},
        "lot_id": {"dtype": "C*n", "ref": None, "value": None, "missing": None},
        "part_typ": {"dtype": "C*n", "ref": None, "value": None, "missing": None},
        "node_nam": {"dtype": "C*n", "ref": None, "value": None, "missing": None},
        "tstr_typ": {"dtype": "C*n", "ref": None, "value": None, "missing": None},
        "job_nam": {"dtype": "C*n", "ref": None, "value": None, "missing": None},
        "job_rev": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "sblot_id": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "oper_nam": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "exec_typ": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "exec_ver": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "test_cod": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "tst_temp": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "user_txt": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "aux_file": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "pkg_typ": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "famly_id": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "date_cod": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "facil_id": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "floor_id": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "proc_id": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "oper_frq": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "spec_nam": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "spec_ver": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "flow_id": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "setup_id": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "dsgn_rev": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "eng_id": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "rom_cod": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "serl_num": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "supr_nam": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"}
    },
    "MRR": {
        "rec_len": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "rec_typ": {"dtype": "U*1", "ref": None, "value": 1, "missing": None},
        "rec_sub": {"dtype": "U*1", "ref": None, "value": 20, "missing": None},
        "finish_t": {"dtype": "U*4", "ref": None, "value": None, "missing": None},
        "disp_cod": {"dtype": "C*1", "ref": None, "value": None, "missing": "space"},
        "usr_desc": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "exc_desc": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"}
    },
    "PCR": {
        "rec_len": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "rec_typ": {"dtype": "U*1", "ref": None, "value": 1, "missing": None},
        "rec_sub": {"dtype": "U*1", "ref": None, "value": 30, "missing": None},
        "head_num": {"dtype": "U*1", "ref": None, "value": None, "missing": None},
        "site_num": {"dtype": "U*1", "ref": None, "value": None, "missing": None},
        "part_cnt": {"dtype": "U*4", "ref": None, "value": None, "missing": None},
        "rtst_cnt": {"dtype": "U*4", "ref": None, "value": None, "missing": 4294967295},
        "abrt_cnt": {"dtype": "U*4", "ref": None, "value": None, "missing": 4294967295},
        "good_cnt": {"dtype": "U*4", "ref": None, "value": None, "missing": 4294967295},
        "func_cnt": {"dtype": "U*4", "ref": None, "value": None, "missing": 4294967295}
    },
    "HBR": {
        "rec_len": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "rec_typ": {"dtype": "U*1", "ref": None, "value": 1, "missing": None},
        "rec_sub": {"dtype": "U*1", "ref": None, "value": 40, "missing": None},
        "head_num": {"dtype": "U*1", "ref": None, "value": None, "missing": None},
        "site_num": {"dtype": "U*1", "ref": None, "value": None, "missing": None},
        "hbin_num": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "hbin_cnt": {"dtype": "U*4", "ref": None, "value": None, "missing": None},
        "hbin_pf": {"dtype": "C*1", "ref": None, "value": None, "missing": "space"},
        "hbin_nam": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"}
    },
    "SBR": {
        "rec_len": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "rec_typ": {"dtype": "U*1", "ref": None, "value": 1, "missing": None},
        "rec_sub": {"dtype": "U*1", "ref": None, "value": 50, "missing": None},
        "head_num": {"dtype": "U*1", "ref": None, "value": None, "missing": None},
        "site_num": {"dtype": "U*1", "ref": None, "value": None, "missing": None},
        "sbin_num": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "sbin_cnt": {"dtype": "U*4", "ref": None, "value": None, "missing": None},
        "sbin_pf": {"dtype": "C*1", "ref": None, "value": None, "missing": "space"},
        "sbin_nam": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"}
    },
    "PMR": {
        "rec_len": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "rec_typ": {"dtype": "U*1", "ref": None, "value": 1, "missing": None},
        "rec_sub": {"dtype": "U*1", "ref": None, "value": 60, "missing": None},
        "pmr_indx": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "chan_typ": {"dtype": "U*2", "ref": None, "value": None, "missing": 0},
        "chan_nam": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "phy_nam": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "log_nam": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "head_num": {"dtype": "U*1", "ref": None, "value": None, "missing": None},
        "site_num": {"dtype": "U*1", "ref": None, "value": None, "missing": None}
    },
    "PGR": {
        "rec_len": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "rec_typ": {"dtype": "U*1", "ref": None, "value": 1, "missing": None},
        "rec_sub": {"dtype": "U*1", "ref": None, "value": 62, "missing": None},
        "grp_indx": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "grp_nam": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "indx_cnt": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "pmr_indx": {"dtype": "xU*2", "ref": "indx_cnt", "value": None, "missing": "indx_cnt = 0"}
    },
    "PLR": {
        "rec_len": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "rec_typ": {"dtype": "U*1", "ref": None, "value": 1, "missing": None},
        "rec_sub": {"dtype": "U*1", "ref": None, "value": 63, "missing": None},
        "grp_cnt": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "grp_indx": {"dtype": "xU*2", "ref": "grp_cnt", "value": None, "missing": None},
        "grp_mode": {"dtype": "xU*2", "ref": "grp_cnt", "value": None, "missing": 0},
        "grp_radx": {"dtype": "xU*1", "ref": "grp_cnt", "value": None, "missing": 0},
        "pgm_char": {"dtype": "xC*n", "ref": "grp_cnt", "value": None, "missing": "length byte = 0"},
        "rtn_char": {"dtype": "xC*n", "ref": "grp_cnt", "value": None, "missing": "length byte = 0"},
        "pgm_chal": {"dtype": "xC*n", "ref": "grp_cnt", "value": None, "missing": "length byte = 0"},
        "rtn_chal": {"dtype": "xC*n", "ref": "grp_cnt", "value": None, "missing": "length byte = 0"}
    },
    "RDR": {
        "rec_len": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "rec_typ": {"dtype": "U*1", "ref": None, "value": 1, "missing": None},
        "rec_sub": {"dtype": "U*1", "ref": None, "value": 70, "missing": None},
        "num_bins": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "rtst_bin": {"dtype": "xU*2", "ref": "num_bins", "value": None, "missing": "num_bins = 0"}
    },
    "SDR": {
        "rec_len": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "rec_typ": {"dtype": "U*1", "ref": None, "value": 1, "missing": None},
        "rec_sub": {"dtype": "U*1", "ref": None, "value": 80, "missing": None},
        "head_num": {"dtype": "U*1", "ref": None, "value": None, "missing": None},
        "site_grp": {"dtype": "U*1", "ref": None, "value": None, "missing": None},
        "site_cnt": {"dtype": "U*1", "ref": None, "value": None, "missing": None},
        "site_num": {"dtype": "xU*1", "ref": "site_cnt", "value": None, "missing": None},
        "hand_typ": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "hand_id": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "card_typ": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "card_id": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "load_typ": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "load_id": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "dib_typ": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "dib_id": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "cabl_typ": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "cabl_id": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "cont_typ": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "cont_id": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "lasr_typ": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "lasr_id": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "extr_typ": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "extr_id": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"}
    },
    "WIR": {
        "rec_len": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "rec_typ": {"dtype": "U*1", "ref": None, "value": 2, "missing": None},
        "rec_sub": {"dtype": "U*1", "ref": None, "value": 10, "missing": None},
        "head_num": {"dtype": "U*1", "ref": None, "value": None, "missing": None},
        "site_grp": {"dtype": "U*1", "ref": None, "value": None, "missing": 255},
        "start_t": {"dtype": "U*4", "ref": None, "value": None, "missing": None},
        "wafer_id": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"}
    },
    "WRR": {
        "rec_len": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "rec_typ": {"dtype": "U*1", "ref": None, "value": 2, "missing": None},
        "rec_sub": {"dtype": "U*1", "ref": None, "value": 20, "missing": None},
        "head_num": {"dtype": "U*1", "ref": None, "value": None, "missing": None},
        "site_grp": {"dtype": "U*1", "ref": None, "value": None, "missing": 255},
        "finish_t": {"dtype": "U*4", "ref": None, "value": None, "missing": None},
        "part_cnt": {"dtype": "U*4", "ref": None, "value": None, "missing": None},
        "rtst_cnt": {"dtype": "U*4", "ref": None, "value": None, "missing": 4294967295},
        "abrt_cnt": {"dtype": "U*4", "ref": None, "value": None, "missing": 4294967295},
        "good_cnt": {"dtype": "U*4", "ref": None, "value": None, "missing": 4294967295},
        "func_cnt": {"dtype": "U*4", "ref": None, "value": None, "missing": 4294967295},
        "wafer_id": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "fabwf_id": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "frame_id": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "mask_id": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "usr_desc": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "exc_desc": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"}
    },
    "WCR": {
        "rec_len": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "rec_typ": {"dtype": "U*1", "ref": None, "value": 2, "missing": None},
        "rec_sub": {"dtype": "U*1", "ref": None, "value": 30, "missing": None},
        "wafr_siz": {"dtype": "R*4", "ref": None, "value": None, "missing": 0},
        "die_ht": {"dtype": "R*4", "ref": None, "value": None, "missing": 0},
        "die_wid": {"dtype": "R*4", "ref": None, "value": None, "missing": 0},
        "wf_units": {"dtype": "U*1", "ref": None, "value": None, "missing": 0},
        "wf_flat": {"dtype": "C*1", "ref": None, "value": None, "missing": "space"},
        "center_x": {"dtype": "I*2", "ref": None, "value": None, "missing": -32768},
        "center_y": {"dtype": "I*2", "ref": None, "value": None, "missing": -32768},
        "pos_x": {"dtype": "C*1", "ref": None, "value": None, "missing": "space"},
        "pos_y": {"dtype": "C*1", "ref": None, "value": None, "missing": "space"}
    },
    "PIR": {
        "rec_len": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "rec_typ": {"dtype": "U*1", "ref": None, "value": 5, "missing": None},
        "rec_sub": {"dtype": "U*1", "ref": None, "value": 10, "missing": None},
        "head_num": {"dtype": "U*1", "ref": None, "value": None, "missing": None},
        "site_num": {"dtype": "U*1", "ref": None, "value": None, "missing": None}
    },
    "PRR": {
        "rec_len": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "rec_typ": {"dtype": "U*1", "ref": None, "value": 5, "missing": None},
        "rec_sub": {"dtype": "U*1", "ref": None, "value": 20, "missing": None},
        "head_num": {"dtype": "U*1", "ref": None, "value": None, "missing": None},
        "site_num": {"dtype": "U*1", "ref": None, "value": None, "missing": None},
        "part_flg": {"dtype": "B*1", "ref": None, "value": None, "missing": None},
        "num_test": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "hard_bin": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "soft_bin": {"dtype": "U*2", "ref": None, "value": None, "missing": 65535},
        "x_coord": {"dtype": "I*2", "ref": None, "value": None, "missing": -32768},
        "y_coord": {"dtype": "I*2", "ref": None, "value": None, "missing": -32768},
        "test_t": {"dtype": "U*4", "ref": None, "value": None, "missing": 0},
        "part_id": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "part_txt": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "part_fix": {"dtype": "B*n", "ref": None, "value": None, "missing": "length byte = 0"}
    },
    "TSR": {
        "rec_len": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "rec_typ": {"dtype": "U*1", "ref": None, "value": 10, "missing": None},
        "rec_sub": {"dtype": "U*1", "ref": None, "value": 30, "missing": None},
        "head_num": {"dtype": "U*1", "ref": None, "value": None, "missing": None},
        "site_num": {"dtype": "U*1", "ref": None, "value": None, "missing": None},
        "test_typ": {"dtype": "C*1", "ref": None, "value": None, "missing": "space"},
        "test_num": {"dtype": "U*4", "ref": None, "value": None, "missing": None},
        "exec_cnt": {"dtype": "U*4", "ref": None, "value": None, "missing": 4294967295},
        "fail_cnt": {"dtype": "U*4", "ref": None, "value": None, "missing": 4294967295},
        "alrm_cnt": {"dtype": "U*4", "ref": None, "value": None, "missing": 4294967295},
        "test_nam": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "seq_name": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "test_lbl": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "opt_flag": {"dtype": "B*1", "ref": None, "value": None, "missing": None},
        "test_tim": {"dtype": "R*4", "ref": None, "value": None, "missing": "opt_flag bit 2 = 1"},
        "test_min": {"dtype": "R*4", "ref": None, "value": None, "missing": "opt_flag bit 0 = 1"},
        "test_max": {"dtype": "R*4", "ref": None, "value": None, "missing": "opt_flag bit 1 = 1"},
        "tst_sums": {"dtype": "R*4", "ref": None, "value": None, "missing": "opt_flag bit 4 = 1"},
        "tst_sqrs": {"dtype": "R*4", "ref": None, "value": None, "missing": "opt_flag bit 5 = 1"}
    },
    "PTR": {
        "rec_len": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "rec_typ": {"dtype": "U*1", "ref": None, "value": 15, "missing": None},
        "rec_sub": {"dtype": "U*1", "ref": None, "value": 10, "missing": None},
        "test_num": {"dtype": "U*4", "ref": None, "value": None, "missing": None},
        "head_num": {"dtype": "U*1", "ref": None, "value": None, "missing": None},
        "site_num": {"dtype": "U*1", "ref": None, "value": None, "missing": None},
        "test_flg": {"dtype": "B*1", "ref": None, "value": None, "missing": None},
        "parm_flg": {"dtype": "B*1", "ref": None, "value": None, "missing": None},
        "result": {"dtype": "R*4", "ref": None, "value": None, "missing": "test_flg bit 1 = 1"},
        "test_txt": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "alarm_id": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "opt_flag": {"dtype": "B*1", "ref": None, "value": None, "missing": None},
        "res_scal": {"dtype": "I*1", "ref": None, "value": None, "missing": "opt_flag bit 0 = 1"},
        "llm_scal": {"dtype": "I*1", "ref": None, "value": None, "missing": "opt_flag bit 4 or 6 = 1"},
        "hlm_scal": {"dtype": "I*1", "ref": None, "value": None, "missing": "opt_flag bit 5 or 7 = 1"},
        "lo_limit": {"dtype": "R*4", "ref": None, "value": None, "missing": "opt_flag bit 4 or 6 = 1"},
        "hi_limit": {"dtype": "R*4", "ref": None, "value": None, "missing": "opt_flag bit 5 or 7 = 1"},
        "units": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "c_resfmt": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "c_llmfmt": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "c_hlmfmt": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "lo_spec": {"dtype": "R*4", "ref": None, "value": None, "missing": "opt_flag bit 2 = 1"},
        "hi_spec": {"dtype": "R*4", "ref": None, "value": None, "missing": "opt_flag bit 3 = 1"}
    },
    "MPR": {
        "rec_len": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "rec_typ": {"dtype": "U*1", "ref": None, "value": 15, "missing": None},
        "rec_sub": {"dtype": "U*1", "ref": None, "value": 15, "missing": None},
        "test_num": {"dtype": "U*4", "ref": None, "value": None, "missing": None},
        "head_num": {"dtype": "U*1", "ref": None, "value": None, "missing": None},
        "site_num": {"dtype": "U*1", "ref": None, "value": None, "missing": None},
        "test_flg": {"dtype": "B*1", "ref": None, "value": None, "missing": None},
        "parm_flg": {"dtype": "B*1", "ref": None, "value": None, "missing": None},
        "rtn_icnt": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "rslt_cnt": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "rtn_stat": {"dtype": "xN*1", "ref": "rtn_icnt", "value": None, "missing": "rtn_icnt = 0"},
        "rtn_rslt": {"dtype": "xR*4", "ref": "rslt_cnt", "value": None, "missing": "rslt_cnt = 0"},
        "test_txt": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "alarm_id": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "opt_flag": {"dtype": "B*1", "ref": None, "value": None, "missing": None},
        "res_scal": {"dtype": "I*1", "ref": None, "value": None, "missing": "opt_flag bit 0 = 1"},
        "llm_scal": {"dtype": "I*1", "ref": None, "value": None, "missing": "opt_flag bit 4 or 6 = 1"},
        "hlm_scal": {"dtype": "I*1", "ref": None, "value": None, "missing": "opt_flag bit 5 or 7 = 1"},
        "lo_limit": {"dtype": "R*4", "ref": None, "value": None, "missing": "opt_flag bit 4 or 6 = 1"},
        "hi_limit": {"dtype": "R*4", "ref": None, "value": None, "missing": "opt_flag bit 5 or 7 = 1"},
        "start_in": {"dtype": "R*4", "ref": None, "value": None, "missing": "opt_flag bit 1 = 1"},
        "incr_in": {"dtype": "R*4", "ref": None, "value": None, "missing": "opt_flag bit 1 = 1"},
        "rtn_indx": {"dtype": "xU*2", "ref": "rtn_icnt", "value": None, "missing": "rtn_icnt = 0"},
        "units": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "units_in": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "c_resfmt": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "c_llmfmt": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "c_hlmfmt": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "lo_spec": {"dtype": "R*4", "ref": None, "value": None, "missing": "opt_flag bit 2 = 1"},
        "hi_spec": {"dtype": "R*4", "ref": None, "value": None, "missing": "opt_flag bit 3 = 1"}
    },
    "FTR": {
        "rec_len": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "rec_typ": {"dtype": "U*1", "ref": None, "value": 15, "missing": None},
        "rec_sub": {"dtype": "U*1", "ref": None, "value": 20, "missing": None},
        "test_num": {"dtype": "U*4", "ref": None, "value": None, "missing": None},
        "head_num": {"dtype": "U*1", "ref": None, "value": None, "missing": None},
        "site_num": {"dtype": "U*1", "ref": None, "value": None, "missing": None},
        "test_flg": {"dtype": "B*1", "ref": None, "value": None, "missing": None},
        "opt_flag": {"dtype": "B*1", "ref": None, "value": None, "missing": None},
        "cycl_cnt": {"dtype": "U*4", "ref": None, "value": None, "missing": "opt_flag bit 0 = 1"},
        "rel_vadr": {"dtype": "U*4", "ref": None, "value": None, "missing": "opt_flag bit 1 = 1"},
        "rept_cnt": {"dtype": "U*4", "ref": None, "value": None, "missing": "opt_flag bit 2 = 1"},
        "num_fail": {"dtype": "U*4", "ref": None, "value": None, "missing": "opt_flag bit 3 = 1"},
        "xfail_ad": {"dtype": "I*4", "ref": None, "value": None, "missing": "opt_flag bit 4 = 1"},
        "yfail_ad": {"dtype": "I*4", "ref": None, "value": None, "missing": "opt_flag bit 4 = 1"},
        "vect_off": {"dtype": "I*2", "ref": None, "value": None, "missing": "opt_flag bit 5 = 1"},
        "rtn_icnt": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "pgm_icnt": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "rtn_indx": {"dtype": "xU*2", "ref": "rtn_icnt", "value": None, "missing": "rtn_icnt = 0"},
        "rtn_stat": {"dtype": "xN*1", "ref": "rtn_icnt", "value": None, "missing": "rtn_icnt = 0"},
        "pgm_indx": {"dtype": "xU*2", "ref": "pgm_icnt", "value": None, "missing": "pgm_icnt = 0"},
        "pgm_stat": {"dtype": "xN*1", "ref": "pgm_icnt", "value": None, "missing": "pgm_icnt = 0"},
        "fail_pin": {"dtype": "D*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "vect_nam": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "time_set": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "op_code": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "test_txt": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "alarm_id": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "prog_txt": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "rslt_txt": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"},
        "patg_num": {"dtype": "U*1", "ref": None, "value": None, "missing": 255},
        "spin_map": {"dtype": "D*n", "ref": None, "value": None, "missing": "length byte = 0"}
    },
    "BPS": {
        "rec_len": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "rec_typ": {"dtype": "U*1", "ref": None, "value": 20, "missing": None},
        "rec_sub": {"dtype": "U*1", "ref": None, "value": 10, "missing": None},
        "seq_name": {"dtype": "C*n", "ref": None, "value": None, "missing": "length byte = 0"}
    },
    "EPS": {
        "rec_len": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "rec_typ": {"dtype": "U*1", "ref": None, "value": 20, "missing": None},
        "rec_sub": {"dtype": "U*1", "ref": None, "value": 20, "missing": None}
    },
    "GDR": {
        "rec_len": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "rec_typ": {"dtype": "U*1", "ref": None, "value": 50, "missing": None},
        "rec_sub": {"dtype": "U*1", "ref": None, "value": 10, "missing": None},
        "fld_cnt": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "gen_data": {"dtype": "V*n", "ref": "fld_cnt", "value": None, "missing": None}
    },
    "DTR": {
        "rec_len": {"dtype": "U*2", "ref": None, "value": None, "missing": None},
        "rec_typ": {"dtype": "U*1", "ref": None, "value": 50, "missing": None},
        "rec_sub": {"dtype": "U*1", "ref": None, "value": 30, "missing": None},
        "text_dat": {"dtype": "C*n", "ref": None, "value": None, "missing": None}
    }
}
# Functions moved from src/core/utils/templates.py
def get_record_types():
    # Uses STDF_TEMPLATES defined above in this file
    return list(STDF_TEMPLATES.keys())

def create_stdf_mapping():
    """Create mapping of (rec_typ, rec_sub) to record types."""
    # Uses STDF_TEMPLATES defined above in this file
    mapping = {}
    for record, template in STDF_TEMPLATES.items():
        rec_typ = template["rec_typ"]["value"]
        rec_sub = template["rec_sub"]["value"]
        if rec_typ is not None and rec_sub is not None:
            mapping[(rec_typ, rec_sub)] = record
    return mapping

def create_stdf_template(record_type):
    # Uses STDF_TEMPLATES defined above in this file
    if record_type not in STDF_TEMPLATES:
        raise ValueError(f"No template found for STDF record type {record_type}")
    
    return {
        "record_type": record_type,
        "fields": STDF_TEMPLATES[record_type].copy()
    }

def get_stdf_template(stdf_mapping, rec_typ, rec_sub):
    # Uses create_stdf_template defined above in this file
    key = (rec_typ, rec_sub)
    record_type = stdf_mapping.get(key)
    
    if record_type:
        return create_stdf_template(record_type)
    else:
        message = f"No template found for rec_typ={rec_typ}, rec_sub={rec_sub}"
        raise ValueError(message)