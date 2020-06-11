# Same reset code

## TRIVIAL
- [ ] bold, dark
- [ ] dark, bold
- [ ] standard bg, other standard bg
- [ ] standard bg, saturated bg
- [ ] standard fg, other standard fg
- [ ] standard fg, saturated fg

## 1 inner color
- [x] bold [ dark ]
- [x] dark [ bold ]
- [ ] standard bg [ other standard bg ]
- [ ] standard bg [ saturated bg ]
- [x] standard fg [ other standard fg ]
- [ ] standard fg [ saturated fg ]
- [x] saturated fg [ standard fg ]
- [ ] saturated fg [ other saturated fg ]


## 2 inner colors
- [ ] standard bg [ other standard bg, <random> ]
- [ ] standard bg [ saturated bg, <random> ]
- [x] standard fg [ other standard fg, <random> ]
- [ ] standard fg [ saturated fg, <random> ]
- [x] formatting [ other formatting, <random> ]

## 2 outer colors
- [ ] standard bg, other standard bg [ <random> ]
- [ ] standard bg, saturated bg [ <random> ]
- [ ] standard fg, other standard fg [ <random> ]
- [ ] standard fg, saturated fg [ <random> ]
- [ ] formatting , other formatting [ <random> ]

# Different reset codes

## 1 inner color
- [x] standard fg [ standard bg ]
- [ ] standard fg [ saturated bg ]
- [ ] saturated fg [ standard bg ]
- [ ] saturated fg [ saturated bg ]
- [ ] standard bg [ standard fg ]
- [ ] standard bg [ saturated fg ]
- [ ] saturated bg [ standard fg ]
- [ ] saturated bg [ saturated fg ]
- [ ] standard fg [ formatting ]
- [x] saturated fg [ formatting ]
- [ ] standard bg [ formatting ]
- [ ] saturated bg [ formatting ]
- [ ] formatting [ standard fg ]
- [ ] formatting [ saturated fg ]
- [ ] formatting [ standard bg ]
- [ ] formatting [ saturated bg ]

## 2 inner colors
- [ ] standard fg [ standard bg, formatting ]
- [ ] standard fg [ saturated bg, formatting ]
- [ ] saturated fg [ standard bg, formatting ]
- [ ] saturated fg [ saturated bg, formatting ]
- [ ] standard bg [ standard fg, formatting ]
- [ ] standard bg [ saturated fg, formatting ]
- [ ] saturated bg [ standard fg, formatting ]
- [ ] saturated bg [ saturated fg, formatting ]
- [ ] formatting [ standard bg, standard fg ]
- [ ] formatting [ saturated bg, standard fg ]
- [ ] formatting [ standard bg, saturated fg ]
- [ ] formatting [ saturated bg, saturated fg ]

## 2 outer colors
- [ ] standard fg, standard bg [ formatting ]
- [ ] standard fg, saturated bg [ formatting ]
- [ ] saturated fg, standard bg [ formatting ]
- [ ] saturated fg, saturated bg [ formatting ]
- [ ] standard bg, standard fg [ formatting ]
- [ ] standard bg, saturated fg [ formatting ]
- [ ] saturated bg, standard fg [ formatting ]
- [ ] saturated bg, saturated fg [ formatting ]
- [ ] formatting, standard bg [ standard fg ]
- [ ] formatting, saturated bg [ standard fg ]
- [ ] formatting, standard bg [ saturated fg ]
- [ ] formatting, saturated bg [ saturated fg ]

# Mulitple recursion levels

# Bad usage

## TRIVIAL
- [ ] <color>, dark, <same color>
- [ ] colored('foo') (no colors)
- [ ] more than 3 colors

## 1 inner color
- [ ] standard bg [ <same color> ]
- [ ] standard fg [ <same color> ]
- [ ] saturated fg [ <same color> ]
- [ ] saturated bg [ <same color> ]
- [ ] formatting [ <same color> ]

## 2 inner colors
- [ ] standard bg [ <random>, <same color> ]
- [ ] standard fg [ <random>, <same color> ]
- [ ] saturated fg [ <random>, <same color> ]
- [ ] saturated bg [ <random>, <same color> ]
- [ ] formatting [ <random>, <same color> ]

## 2 outer colors
- [ ] standard bg, <random> [ <same color> ]
- [ ] standard fg, <random> [ <same color> ]
- [ ] saturated fg, <random> [ <same color> ]
- [ ] saturated bg, <random> [ <same color> ]
- [ ] formatting, <random> [ <same color> ]
- [ ] standard bg, <same color> [ <random> ]
- [ ] standard fg, <same color> [ <random> ]
- [ ] saturated fg, <same color> [ <random> ]
- [ ] saturated bg, <same color> [ <random> ]
- [ ] formatting, <same color> [ <random> ]