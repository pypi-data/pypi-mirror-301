import pytest
import SuomiGeoData
import os
import tempfile
import geopandas
import shapely
import rasterio


@pytest.fixture(scope='class')
def paituli():

    yield SuomiGeoData.Paituli()


@pytest.fixture(scope='class')
def syke():

    yield SuomiGeoData.Syke()


@pytest.fixture(scope='class')
def core():

    yield SuomiGeoData.core.Core()


@pytest.fixture
def message():

    output = {
        'download': 'All downloads are complete.',
        'folder_empty': 'Output folder must be empty.',
        'gdf_write': 'GeoDataFrame saved to the output file.',
        'geoprocess': 'All geoprocessing has been completed.',
        'error_area': 'The index map does not intersect with the given area.',
        'error_folder': 'The folder path does not exist.',
        'error_driver': 'Could not retrieve driver from the file path.',
        'error_gdf': 'Input area must be either file or GeoDataFrame format.',
        'error_label': 'The label ABCDE does not exist in the index map.',
        'error_level': 'Input level must be one of 1, 2, 3, 4, or 5.',
        'error_excel': 'Input file extension ".xl" does not match the required ".xlsx".'
    }

    return output


def test_save_indexmap(
    paituli,
    message
):

    with tempfile.TemporaryDirectory() as tmp_dir:
        # pass test for saving DEM index map
        dem_file = os.path.join(tmp_dir, 'indexmap_dem.shp')
        save_dem = paituli.save_indexmap_dem(dem_file)
        assert save_dem == message['gdf_write']
        dem_gdf = geopandas.read_file(dem_file)
        assert isinstance(dem_gdf, geopandas.GeoDataFrame) is True
        assert dem_gdf.shape[0] == 10320
        # pass test for saving topographical database index map
        tdb_file = os.path.join(tmp_dir, 'indexmap_tdb.shp')
        save_tdb = paituli.save_indexmap_tdb(tdb_file)
        assert save_tdb == message['gdf_write']
        tdb_gdf = geopandas.read_file(tdb_file)
        assert isinstance(tdb_gdf, geopandas.GeoDataFrame) is True
        assert tdb_gdf.shape[0] == 3132

    # error test for undetected OGR driver while saving DEM index map
    with pytest.raises(Exception) as exc_info:
        paituli.save_indexmap_dem('invalid_file_extension.sh')
    assert exc_info.value.args[0] == message['error_driver']

    # error test for undetected OGR driver while saving topographical database index map
    with pytest.raises(Exception) as exc_info:
        paituli.save_indexmap_tdb('invalid_file_extension.sh')
    assert exc_info.value.args[0] == message['error_driver']


def test_is_valid_label(
    paituli
):

    # pass test for valid label of DEM index map
    assert paituli.is_valid_label_dem('K3244G') is True
    assert paituli.is_valid_label_dem('invalid_label') is False

    # pass test for valid label of topographical database index map
    assert paituli.is_valid_label_tdb('K2344R') is True
    assert paituli.is_valid_label_tdb('invalid_label') is False


def test_dem_download_by_labels(
    paituli,
    message
):

    # pass test for downloading DEM labels
    with tempfile.TemporaryDirectory() as tmp_dir:
        assert paituli.dem_download_by_labels(
            ['X4344A'], tmp_dir
        ) == message['download']
        # error test for non empty folder
        with pytest.raises(Exception) as exc_info:
            paituli.dem_download_by_labels(['K3244G'], tmp_dir)
        assert exc_info.value.args[0] == message['folder_empty']

    # error test for invalid label
    with tempfile.TemporaryDirectory() as tmp_dir:
        with pytest.raises(Exception) as exc_info:
            paituli.dem_download_by_labels(['ABCDE'], tmp_dir)
        assert exc_info.value.args[0] == message['error_label']

    # error test for invalid folder path
    with pytest.raises(Exception) as exc_info:
        paituli.dem_download_by_labels(['X4344A'], tmp_dir)
    assert exc_info.value.args[0] == message['error_folder']


def test_tdb_download_by_labels(
    paituli,
    message
):

    # pass test for downloading topographical database labels
    with tempfile.TemporaryDirectory() as tmp_dir:
        assert paituli.tdb_download_by_labels(
            ['J3224R'], tmp_dir
        ) == message['download']
        # error test for non empty folder
        with pytest.raises(Exception) as exc_info:
            paituli.tdb_download_by_labels(['K2344R'], tmp_dir)
        assert exc_info.value.args[0] == message['folder_empty']

    # error test for invalid label
    with tempfile.TemporaryDirectory() as tmp_dir:
        with pytest.raises(Exception) as exc_info:
            paituli.tdb_download_by_labels(['ABCDE'], tmp_dir)
        assert exc_info.value.args[0] == message['error_label']

    # error test for invalid folder path
    with pytest.raises(Exception) as exc_info:
        paituli.tdb_download_by_labels(['J3224R'], tmp_dir)
    assert exc_info.value.args[0] == message['error_folder']


def test_dem_labels_download_by_area(
    paituli,
    message
):

    with tempfile.TemporaryDirectory() as tmp_dir:
        # error test for invalid input
        with pytest.raises(Exception) as exc_info:
            paituli.dem_labels_download_by_area(5, tmp_dir)
        assert exc_info.value.args[0] == message['error_gdf']
        # pass test for downloading when the input is a GeoDataFrame format
        example_gdf = paituli.get_example_area
        assert paituli.dem_labels_download_by_area(
            example_gdf, tmp_dir
        ) == message['download']
        # pass test for downloading when the input is a file format
        example_file = os.path.join(tmp_dir, 'example_file.shp')
        example_gdf.to_file(example_file)
        sub_dir = os.path.join(tmp_dir, 'sub_dir')
        os.makedirs(sub_dir)
        assert paituli.dem_labels_download_by_area(
            example_file, sub_dir
        ) == message['download']

    example_area = shapely.Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
    with tempfile.TemporaryDirectory() as tmp_dir:
        # error test for input GeoDataFrame has no CRS
        nocrs_gdf = geopandas.GeoDataFrame({'geometry': [example_area]})
        with pytest.raises(Exception) as exc_info:
            paituli.dem_labels_download_by_area(nocrs_gdf, tmp_dir)
        assert exc_info.value.args[0] == message['error_area']
        # error test for input GeoDataFrame has CRS other than 'EPSG:3067'
        crs_gdf = geopandas.GeoDataFrame({'geometry': [example_area]}, crs='EPSG:4326')
        with pytest.raises(Exception) as exc_info:
            paituli.dem_labels_download_by_area(crs_gdf, tmp_dir)
        assert exc_info.value.args[0] == message['error_area']


def test_download_corine_land_cover_2018(
    syke,
    message
):

    # pass test for downloading Syke's land cover map
    with tempfile.TemporaryDirectory() as tmp_dir:
        assert len(os.listdir(tmp_dir)) == 0
        assert syke.download_corine_land_cover_2018(tmp_dir) == message['download']
        assert len(os.listdir(tmp_dir)) > 0

    # error test for invalid folder path
    with pytest.raises(Exception) as exc_info:
        syke.download_corine_land_cover_2018(tmp_dir)
    assert exc_info.value.args[0] == message['error_folder']


def test_dem_by_area(
    paituli,
    syke,
    core,
    message
):

    # temporary directory
    with tempfile.TemporaryDirectory() as tmp_dir:
        # pass test for downloading Syke's catchment divisions
        assert syke.download_catchment_divisions_2023(tmp_dir) == message['download']
        catchd5_path = os.path.join(tmp_dir, 'catchment_division_level_5.shp')
        sub_dir = os.path.join(tmp_dir, 'sub_dir')
        os.makedirs(sub_dir)
        # error test for Syke's single subcatchment when the input level is not an integer
        with pytest.raises(Exception) as exc_info:
            paituli.dem_labels_download_by_syke_subcatchment(
                input_file=catchd5_path,
                level='invalid_level',
                single_area=15730216003,
                folder_path=sub_dir
            )
        assert exc_info.value.args[0] == message['error_level']
        # error test for Syke's single subcatchment when the input area does not intersect with the index map
        with pytest.raises(Exception) as exc_info:
            paituli.dem_labels_download_by_syke_subcatchment(
                input_file=catchd5_path,
                level=5,
                single_area=157302,
                folder_path=sub_dir
            )
        assert exc_info.value.args[0] == message['error_area']
        # pass test for downloading DEM labels for single subcatchment from Syke's catchment divisions
        assert paituli.dem_labels_download_by_syke_subcatchment(
            input_file=catchd5_path,
            level=5,
            single_area=15730216003,
            folder_path=sub_dir
        ) == message['download']
        # pass test for selecting single polygons for Syke's single subcatchment
        spg_gdf = syke.select_single_subcatchment(
            input_file=catchd5_path,
            level=5,
            single_area=15730216003,
            output_file=os.path.join(tmp_dir, 'single_subcatchment_spg.shp'),
            merge_polygons=True,
            percentage_cutoff=0
        )
        assert isinstance(spg_gdf, geopandas.GeoDataFrame) is True
        assert spg_gdf.geometry.iloc[0].bounds == (594410.0, 7377690.0, 596350.0, 7379700.0)
        # error test for undetected OGR driver while saving Syke's single subcatchment
        with pytest.raises(Exception) as exc_info:
            syke.select_single_subcatchment(
                input_file=catchd5_path,
                level=5,
                single_area=15730216003,
                output_file=os.path.join(tmp_dir, 'invalid_file_extension.sh')
            )
        assert exc_info.value.args[0] == message['error_driver']
        # pass test for Syke's single subcatchment with merging polygons and percentage cutoff
        mpg_gdf = syke.select_single_subcatchment(
            input_file=catchd5_path,
            level=5,
            single_area=42010117301,
            output_file=os.path.join(tmp_dir, 'single_subcatchment_mpg.shp'),
            merge_polygons=True,
            percentage_cutoff=0
        )
        assert mpg_gdf.geometry.iloc[0].bounds == (689130.0, 6898840.0, 693370.0, 6902730.0)
        # pass test for Syke's single subcatchment without merging polygons or percentage cutoff
        mpg_gdf = syke.select_single_subcatchment(
            input_file=catchd5_path,
            level=5,
            single_area=31670606904,
            merge_polygons=False,
            percentage_cutoff=-1
        )
        assert round(mpg_gdf.geometry.iloc[0].area) == 238699
        # pass test for raster merging
        assert core.raster_merging(
            folder_path=sub_dir,
            output_file=os.path.join(tmp_dir, 'check_merged.tif')
        ) == 'Merging of rasters completed.'
        # error test for raster merging when the input is a invalid folder path
        with pytest.raises(Exception) as exc_info:
            core.raster_merging(
                folder_path=os.path.join(tmp_dir, 'nonexist_dir'),
                output_file=os.path.join(tmp_dir, 'check_merged.tif')
            )
        assert exc_info.value.args[0] == message['error_folder']
        # error test for undetected driver while raster merging
        with pytest.raises(Exception) as exc_info:
            core.raster_merging(
                folder_path=sub_dir,
                output_file=os.path.join(tmp_dir, 'merged.t')
            )
        assert exc_info.value.args[0] == message['error_driver']
        # pass test for raster clipping
        assert core.raster_clipping_by_mask(
            input_file=os.path.join(tmp_dir, 'check_merged.tif'),
            mask_area=geopandas.read_file(os.path.join(tmp_dir, 'single_subcatchment_spg.shp')),
            output_file=os.path.join(tmp_dir, 'check_clipped.tif')
        ) == 'Raster clipping completed.'
        with rasterio.open(os.path.join(tmp_dir, 'check_clipped.tif')) as clip_raster:
            assert clip_raster.bounds.bottom == 7377690.0
            assert clip_raster.bounds.top == 7379700.0
        # error test for invalid mask area while clipping raster file
        with pytest.raises(Exception) as exc_info:
            core.raster_clipping_by_mask(
                input_file=os.path.join(tmp_dir, 'check_merged.tif'),
                mask_area=5,
                output_file=os.path.join(tmp_dir, 'check_clipped.tif')
            )
        assert exc_info.value.args[0] == message['error_gdf']
        # error test for undetected driver while clipping raster file
        with pytest.raises(Exception) as exc_info:
            core.raster_clipping_by_mask(
                input_file=os.path.join(tmp_dir, 'check_merged.tif'),
                mask_area=os.path.join(tmp_dir, 'single_subcatchment_spg.shp'),
                output_file=os.path.join(tmp_dir, 'invalid.t')
            )
        assert exc_info.value.args[0] == message['error_driver']
        # pass test for downoading clipped dem from Syke's catchment divisions
        raster_path = os.path.join(tmp_dir, 'clipped_catchment.tif')
        assert paituli.dem_clipped_download_by_syke_subcatchment(
            input_file=catchd5_path,
            level=5,
            single_area=15730216003,
            output_file=raster_path,
            compress='lzw'
        ) == message['geoprocess']
        with rasterio.open(raster_path) as tmp_raster:
            assert tmp_raster.bounds.left == 594410.0
            assert tmp_raster.bounds.right == 596350.0
        catchd2_path = os.path.join(tmp_dir, 'catchment_division_level_2.shp')
        # error test for Syke's multiple subcatchment without merging or percentage cutoff
        with pytest.raises(Exception) as exc_info:
            syke.merging_multiple_subcatchments(
                input_file=catchd2_path,
                level='invalid_level',
                multiple_area=[1159, 1160, 1161],
            )
        assert exc_info.value.args[0] == message['error_level']
        # error test for Syke's multiple subcatchment when the input area contains single element
        with pytest.raises(Exception) as exc_info:
            syke.merging_multiple_subcatchments(
                input_file=catchd2_path,
                level=2,
                multiple_area=[11],
            )
        assert exc_info.value.args[0] == 'Input multiple area list contains single element.'
        # error test for Syke's multiple subcatchment when the input area does not intersect with the index map
        with pytest.raises(Exception) as exc_info:
            syke.merging_multiple_subcatchments(
                input_file=catchd2_path,
                level=2,
                multiple_area=[11, 12],
            )
        assert exc_info.value.args[0] == message['error_area']
        # error test for undetected OGR driver while saving Syke's multiple subcatchment
        with pytest.raises(Exception) as exc_info:
            syke.merging_multiple_subcatchments(
                input_file=catchd2_path,
                level=2,
                multiple_area=[1159, 1160, 1161],
                output_file=os.path.join(tmp_dir, 'invalid_file_extension.sh'),
            )
        assert exc_info.value.args[0] == message['error_driver']
        # pass test for Syke's multiple subcatchment without percentage cutoff
        msc_gdf = syke.merging_multiple_subcatchments(
            input_file=catchd2_path,
            level=2,
            multiple_area=[1159, 1160, 1161],
            output_file=os.path.join(tmp_dir, 'merging_msc.shp'),
        )
        assert msc_gdf.shape[0] == 20
        # pass test for Syke's multiple subcatchment with percentage cutoff
        msc_gdf = syke.merging_multiple_subcatchments(
            input_file=catchd5_path,
            level=5,
            multiple_area=[15730214505, 15730214514],
            percentage_cutoff=0
        )
        assert msc_gdf.geometry.iloc[0].area == 22858200.0
        # pass test for downoading clipped dem from area
        raster_path = os.path.join(tmp_dir, 'clipped_area.tif')
        assert paituli.dem_clipped_download_by_area(
            input_area=msc_gdf,
            output_file=raster_path,
        ) == message['geoprocess']
        with rasterio.open(raster_path) as tmp_raster:
            assert tmp_raster.bounds.left == 582480.0
            assert tmp_raster.bounds.right == 589690.0

    # error test for downloading Syke's catchment division when the input is a invalid folder path
    with pytest.raises(Exception) as exc_info:
        syke.download_catchment_divisions_2023(tmp_dir)
    assert exc_info.value.args[0] == message['error_folder']


def test_tdb_metadata_to_dataframe(
    paituli,
    message
):

    # pass test for topographic database to multi-index DataFrame
    with tempfile.TemporaryDirectory() as tmp_dir:
        excel_file = os.path.join(tmp_dir, 'tdb_metadata.xlsx')
        df = paituli.tdb_metadata_to_dataframe(
            excel_file=excel_file
        )
        assert len(df.index.names) == 4

    # error test for invalid Excel file input
    with pytest.raises(Exception) as exc_info:
        paituli.tdb_metadata_to_dataframe('tdb_metadata.xl')
    assert exc_info.value.args[0] == message['error_excel']
