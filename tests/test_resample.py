# import os
#
# import rasterio
#
# from gfw_pixetl.data_type import data_type_factory
# from gfw_pixetl.grids import grid_factory, Grid
# from gfw_pixetl.layers import RasterSrcLayer
# from gfw_pixetl.tiles import RasterSrcTile
#
#
# minx: int = 30
# maxy: int = 30
# subset: str = "30N_030E"
#
# grid: Grid = grid_factory("30x30")
#
# src_uri: str = "gfw2-data/forest_change/hansen_2018/all.vrt"
#
# datatype = data_type_factory("uint", 5)
#
# uri: str = "gfw-test-data/gfw_pixetl/resample/{tile_id}.tif"
#
# layer: RasterSrcLayer = RasterSrcLayer(
#     "test_layer",
#     "test",
#     "test",
#     grid,
#     datatype,
#     src_uri,
#     single_tile=True,
#     subset=[subset],
# )
#
# tile = RasterSrcTile(minx, maxy, layer.grid, layer.src, layer.uri)
# tile.src_tile_exists()
#
#
# def test_src_tile_exists():
#     assert tile.src_tile_exists()
#
#
# def test_uri_exists():
#     assert not tile.uri_exists()
#
#
# def test_find_src_tiles():
#     assert tile.src_tile_intersects()
#
#
# def test_translate_src_tile():
#     tiles = layer.transform([tile])
#
#     for t in tiles:
#         with rasterio.open(t.uri) as trg:
#             trg_profile = trg.profile
#
#         assert trg_profile["blockxsize"] == grid.blockxsize
#         assert trg_profile["blockysize"] == grid.blockysize
#         assert trg_profile["compress"].lower() == datatype.compression.lower()
#         assert trg_profile["count"] == 1
#         assert trg_profile["crs"] == {"init": grid.srs.srs}
#         assert trg_profile["driver"] == "GTiff"
#         assert trg_profile["dtype"] == datatype.to_numpy_dt()
#         assert trg_profile["height"] == grid.cols
#         assert trg_profile["interleave"] == "band"
#         assert trg_profile["nodata"] == datatype.no_data
#         assert trg_profile["tiled"] is True
#         # assert trg_profile['transform']: Affine(30.0, 0.0, 381885.0, 0.0, -30.0, 2512815.0),
#         assert trg_profile["width"] == grid.rows
#
#         os.remove(t.uri)
