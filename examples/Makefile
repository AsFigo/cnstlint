# ----------------------------------------------------
# SPDX-FileCopyrightText: AsFigo Technologies, UK
# SPDX-FileCopyrightText: VerifWorks, India
# SPDX-License-Identifier: MIT
# ----------------------------------------------------

CNSTLINT = python3 ../bin/cnstlint.py

all: run_f run_p run_dist_frac_f run_dist_frac_p

run_f:
	$(CNSTLINT) -t cnst_operator_precedence_f.sv

run_p:
	$(CNSTLINT) -t cnst_operator_precedence_p.sv

run_dist_frac_f:
	$(CNSTLINT) -t cnst_dist_fractional_weight_f.sv

run_dist_frac_p:
	$(CNSTLINT) -t cnst_dist_fractional_weight_p.sv
