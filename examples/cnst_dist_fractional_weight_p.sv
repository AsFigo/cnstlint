// ----------------------------------------------------
// SPDX-FileCopyrightText: AsFigo Technologies, UK
// SPDX-FileCopyrightText: VerifWorks, India
// SPDX-License-Identifier: MIT
// ----------------------------------------------------

class foo_class #(int MAX = 256);

    int foo_wt;
    rand bit [8:0] foo;
    rand bit [8:0] bar;
    rand bit [8:0] baz;

    // Integer weights expressed as percentages
    constraint foo_int_cnst {
        foo dist {111 := 25, 222 := 25, 333 := 50};
    }

    // Whole-range weight with :/ instead of a fraction per value
    constraint bar_range_cnst {
        bar dist {[0:10] :/ 1, 12 := 1, [13:30] :/ 1, 31 := 1};
    }

    // Division in the value range (not the weight) and a variable weight
    constraint baz_value_div_cnst {
        baz dist {[0:MAX/2] :/ foo_wt, [MAX/2+1:MAX-1] :/ 3};
    }

endclass
