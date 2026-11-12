P = {
"sharp-axe": "h0-tired-b f01-hire-a f02-pile-a f03-amazed-a f04-harder-b f05-stump-a f06-hands-a f07-blade-b f08-shrug-a f09-sharpen-a k1-rest-b k2-strong-a",
"lost-watch": "h0-silent-b g01-lost-b g02-reward-a g03-chaos-a g04-giveup-a g05-ask-a g06-listen-b g07-watch-a g08-found-a k1-give-b k2-calm=h0-silent-a",
}
P["twenty-dollar"] = "h0-hold-a t01-stage-a t02-hands=t02-hands-c t03-crumple-a t04-step-a t05-dirty-a t06-value-a t07-crushed-a k1-rise-a k2-light-b"
P["salt-lake"] = "h0-sad-b s01-visit-b s02-salt-b s03-drink-a s04-walk-a s05-throw-b s06-sip-a s07-master-b k1-lake-a k2-peace=k1-lake-b"
P["golden-buddha"] = "h0-crack=h0-crack-c j01-gold-a j02-cover=j02-cover-c j03-army-a j04-years-a j05-notice-a j06-glint-a j07-chip-a j08-shine-b k1-face-a k2-walk=k2-walk-c"
P["potato-grudge"] = "h0-sack-b q01-bags-a q02-write-a q03-lift-b q04-street-a q05-bed-b q06-rot-a q07-teacher-b k1-down-a k2-free-a"
P["golden-buddha"] = P["golden-buddha"].replace("j08-shine-b", "j08-shine-a")
P["twenty-dollar"] = P["twenty-dollar"]
P["jar-rocks"] = "h0-wrong-b r01-rocks-a r02-yes-a r03-pebbles-a r04-sand-b r05-full-a r06-point-a k1-first-a k2-done-a"
P["monkey-jar"] = "h0-stuck-a m01-set=m01-set-c m02-banana=m02-banana-c m03-reach=m03-reach-c m04-hunters-a m05-scream-a m06-free=m06-free-c k0-hold-a k1-open-b"
P["frog-boil"] = "h0-desk-a p01-jump-b p02-cool=p02-cool-c p03-comfy-a p04-hotter-a p05-weak-b p06-habit-a p07-couple-b k1-leave-a k2-free=k2-free-c"
P["farmer-treasure"] = "h0-dig=h0-dig-c v01-bed-a v02-dig2=v02-dig2-c v03-holes-a v04-nothing=v04-nothing-c v05-sow-a v06-wheat-a v07-market-b k1-wheat-b k2-field-b"
P["golden-buddha"] = P["golden-buddha"].replace("j05-notice-a", "j05-notice=j05-notice-c").replace("j07-chip-a", "j07-chip=j07-chip-c")
P["monkey-jar"] = P["monkey-jar"].replace("m03-reach-c", "m03-reach-d")
P["frog-boil"] = P["frog-boil"].replace("p02-cool-c", "p02-cool-d")
P["farmer-treasure"] = P["farmer-treasure"].replace("h0-dig-c", "h0-dig-d").replace("v02-dig2-c", "v02-dig2-d").replace("v04-nothing-c", "v04-nothing-d")
