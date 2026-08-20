from skyscape.tiling import lonlat_to_tile,quadkey,parse_quadkey,tile_bounds
def test_tile_is_valid():
    t=lonlat_to_tile(0,0,2); assert 0<=t.x<4 and 0<=t.y<4; assert len(quadkey(t))==2
def test_quadkey_roundtrip():
    t=lonlat_to_tile(-6.3,53.3,18); assert parse_quadkey(quadkey(t))==t
def test_tile_bounds():
    west,south,east,north=tile_bounds(lonlat_to_tile(0,0,2)); assert west<east and south<north
