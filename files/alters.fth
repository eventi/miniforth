( 64K should be enough for everybody, right? )
( at least to get to protected mode? )
( well, apparently I was too wasteful. )
( and reengineering everything is not my idea of a good time. )

: es 0 ;  : cs 1 ;  : ss 2 ;  : ds 3 ;
: r-rm,  swap rm-r, ;
: movw-sr,  $8C c, r-rm, ;
: movw-rs,  $8E c, rm-r, ;
: retf, $CB c, ;

:code ds>fs-cmove ( src dst count -- )
  bx cx movw-rr,
  si ax movw-rr,  di dx movw-rr,
  di pop, si pop,
  push-es, push-fs, pop-es,
  rep, movsb,
  pop-es,
  ax si movw-rr,  dx di movw-rr,
  bx pop,
  next,

variable saved-sp
variable saved-rp

: >alter ( n -- seg ) #12 lshift ;
: mk-alter ( n -- ) undirty >alter fs!
  sp@ saved-sp !
  rp@ saved-rp !
  0 0 FFFF ds>fs-cmove ;  ( the last byte doesn't matter anyway )

:code (switched)
  cs ax movw-sr,
  ax ds movw-rs,
  ax es movw-rs,
  ax ss movw-rs,
  [#] sp movw-mr, saved-sp ,
  [#] di movw-mr, saved-rp ,
  bx pop,
  ' mount ax movw-ir,
  ax jmp-r,

:code (switch) ( target-seg -- )
  bx push,
  ' (switched) ax movw-ir,  ax push,
  retf,

: switch ( target-alter -- )
  sp@ cell+ saved-sp !
  rp@ saved-rp !
  undirty >alter (switch) ;
