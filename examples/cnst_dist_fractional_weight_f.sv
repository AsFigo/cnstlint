// ----------------------------------------------------
// SPDX-FileCopyrightText: AsFigo Technologies, UK
// SPDX-FileCopyrightText: VerifWorks, India
// SPDX-License-Identifier: MIT
// ----------------------------------------------------

class foo_class;

    int foo_wt;
    rand bit [8:0] foo;
    rand bit [8:0] bar;
    rand bit [8:0] baz;
    rand bit [8:0] qux;

    // Integer division truncates to 0: 111 and 222 are never picked
    constraint foo_int_div_cnst {
        foo dist {111 := 1/2, 222 := 1/2, 333 := 1};
    }

    // Real weights are tool-dependent
    constraint bar_real_cnst {
        bar dist {111 := 0.5, 222 :/ 0.5, [300:400] :/ 1.0e1};
    }

    // Fraction on a range truncates to 0: only 12 and 31 are ever picked
    constraint baz_range_cnst {
        baz dist {[0:10] := 1/11, 12 := 1, [13:30] := 1/18, 31 := 1};
    }

    // Non-zero but truncated (10/3 == 3), and runtime division
    constraint qux_trunc_cnst {
        qux dist {111 := 10/3, 222 := foo_wt/4};
    }

endclass
