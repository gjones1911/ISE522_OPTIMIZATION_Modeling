var x11 >= 0;
var x21 >= 0;
var x31 >= 0;
var x12 >= 0;
var x22 >= 0;
var x32 >= 0;
maximize Revenue: .25(x11+x21+x31) + .2*(x12 + x22 + x32);
subject to Sugar: x11 + x12 <= 100;
subject to Nuts: x21 + x22 <= 20;
subject to Chocolate: x31 + x31 <= 30;
subject to NutsInEE: x21 <= .2*(x11+x21+x31);
subject to NutsInSlugger: x21 <= .2*(x11+x21+x31);
subject to NutsInSlugger: x21 <= .2*(x11+x21+x31);

