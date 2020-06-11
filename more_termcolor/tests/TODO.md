Different reset codes
=====================

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


Same reset code
===============

## TRIVIAL
- [ ] bold, dark
- [ ] dark, bold
- [ ] standard bg, standard bg
- [ ] standard bg, saturated bg
- [ ] standard fg, standard fg
- [ ] standard fg, saturated fg

## 1 inner color
- [x] bold [ dark ]
- [x] dark [ bold ]
- [ ] bg [ bg ]
- [x] fg [ fg ]


## 2 inner colors
- [ ] bg [ bg, fg ]
- [ ] bg [ bg, formatting ]
- [x] fg [ fg, bg ]
- [ ] fg [ fg, formatting ]
- [x] formatting [ formatting, fg ]
- [ ] formatting [ formatting, bg ]

## 2 outer colors
- [ ] bg, bg [ fg ]
- [ ] bg, fg [ bg ]
- [ ] bg, bg [ formatting ]
- [ ] bg, formatting [ bg ]
- [ ] fg, fg [ bg ]
- [ ] fg, bg [ fg ]
- [ ] fg, fg [ formatting ]
- [ ] fg, formatting [ fg ]
- [ ] formatting, formatting [ fg ]
- [ ] formatting, fg [ formatting ]
- [ ] formatting, formatting [ bg ]
- [ ] formatting, bg [ formatting ]
- [ ] formatting, formatting [ formatting ]
- [ ] fg, fg [ fg ]
- [ ] bg, bg [ bg ]

# Mulitple recursion levels

Bad usage
=========

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