# Different reset codes

## Trivial
- [ ] standard fg, standard bg
- [ ] standard fg, saturated bg
- [ ] standard fg, formatting
- [ ] saturated fg, standard bg
- [ ] saturated fg, saturated bg
- [ ] saturated fg, formatting

## 1 inner color
- [x] fg [ bg ]
- [x] fg [ formatting ]
- [x] bg [ fg ]
- [x] bg [ formatting ]
- [x] formatting [ fg ]
- [x] formatting [ bg ]


## 2 inner colors
- [x] fg [ bg, formatting ]
- [x] bg [ fg, formatting ]
- [x] formatting [ bg, fg ]

## 2 outer colors
- [x] fg, bg [ formatting ]
- [x] formatting, bg [ fg ]
- [x] formatting, fg [ bg ]


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