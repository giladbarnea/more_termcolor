Different reset codes
=====================

## Trivial
- [ ] standard fg, standard bg
- [ ] standard fg, bright bg
- [ ] standard fg, formatting
- [ ] bright fg, standard bg
- [ ] bright fg, bright bg
- [ ] bright fg, formatting

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
- [ ] standard bg, bright bg
- [ ] standard fg, standard fg
- [ ] standard fg, bright fg

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
- [x] <color>, dark, <same color>
- [x] colored('foo') (no colors)
- [x] more than 3 colors

## 1 inner color
- [ ] standard bg [ <same color> ]
- [ ] standard fg [ <same color> ]
- [ ] bright fg [ <same color> ]
- [ ] bright bg [ <same color> ]
- [ ] formatting [ <same color> ]

## 2 inner colors
- [ ] standard bg [ <random>, <same color> ]
- [ ] standard fg [ <random>, <same color> ]
- [ ] bright fg [ <random>, <same color> ]
- [ ] bright bg [ <random>, <same color> ]
- [ ] formatting [ <random>, <same color> ]

## 2 outer colors
- [ ] standard bg, <random> [ <same color> ]
- [ ] standard fg, <random> [ <same color> ]
- [ ] bright fg, <random> [ <same color> ]
- [ ] bright bg, <random> [ <same color> ]
- [ ] formatting, <random> [ <same color> ]
- [ ] standard bg, <same color> [ <random> ]
- [ ] standard fg, <same color> [ <random> ]
- [ ] bright fg, <same color> [ <random> ]
- [ ] bright bg, <same color> [ <random> ]
- [ ] formatting, <same color> [ <random> ]