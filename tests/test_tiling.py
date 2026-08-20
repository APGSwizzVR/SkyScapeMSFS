from skyscape.tiling import lonlat_to_tile,quadkey
def test_tile_is_valid():
    t=lonlat_to_tile(0,0,2)
    assert 0 <= t.x < 4 and 0 <= t.y < 4
    assert len(quadkey(t))==2
