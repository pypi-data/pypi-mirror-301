import os
import io
import zipfile
import typing
import geopandas
import shapely
import requests
from .core import Core


class Syke:

    '''
    Executes downloading and extracting data from Syke
    (https://www.syke.fi/en-US/Open_information/Spatial_datasets/Downloadable_spatial_dataset).
    '''

    def download_corine_land_cover_2018(
        self,
        folder_path: str,
        http_headers: typing.Optional[dict[str, str]] = None
    ) -> str:

        '''
        Downloads raster files of Finland's CORINE land cover for the year 2018 and
        returns a confirmation message.

        Parameters
        ----------
        folder_path : str
            Folder path to save the downloaded files.

        http_headers : dict, optional
            HTTP headers to be used for the web request. Defaults to
            :attr:`SuomiGeoData.core.Core.default_http_headers` attribute if not provided.

        Returns
        -------
        str
            A confirmation message indicating that download is complete.
        '''

        # check the existence of the given folder path
        if os.path.isdir(folder_path):
            pass
        else:
            raise Exception(
                'The folder path does not exist.'
            )

        # web request headers
        headers = Core().default_http_headers if http_headers is None else http_headers

        # download land cover
        url = 'https://wwwd3.ymparisto.fi/d3/Static_rs/spesific/clc2018_fi20m.zip'
        response = requests.get(
            url=url,
            headers=headers
        )
        downloaded_data = io.BytesIO(response.content)
        with zipfile.ZipFile(downloaded_data, 'r') as downloaded_zip:
            downloaded_zip.extractall(
                folder_path
            )

        return 'All downloads are complete.'

    def download_catchment_divisions_2023(
        self,
        folder_path: str,
        http_headers: typing.Optional[dict[str, str]] = None
    ) -> str:

        '''
        Downloads shapefiles of Finland's catchment area divisions for the year 2023 and
        returns a confirmation message.

        Parameters
        ----------
        folder_path : str
            Path of empty folder to save the downloaded shapefiles.

        http_headers : dict, optional
            HTTP headers to be used for the web request. Defaults to
            :attr:`SuomiGeoData.core.Core.default_http_headers` attribute if not provided.

        Returns
        -------
        str
            A confirmation message indicating that download is complete.
        '''

        # check the existence of the given folder path
        if os.path.isdir(folder_path):
            pass
        else:
            raise Exception(
                'The folder path does not exist.'
            )

        # web request headers
        headers = Core().default_http_headers if http_headers is None else http_headers

        # download land cover
        url = 'https://wwwd3.ymparisto.fi/d3/gis_data/spesific/valumaalueet.zip'
        response = requests.get(
            url=url,
            headers=headers
        )
        downloaded_data = io.BytesIO(response.content)
        with zipfile.ZipFile(downloaded_data, 'r') as downloaded_zip:
            downloaded_zip.extractall(
                folder_path
            )
            for file in os.listdir(folder_path):
                if file.startswith('Valumaaluejako_taso'):
                    renamed_file = file.replace(
                        'Valumaaluejako_taso', 'catchment_division_level_'
                    )
                else:
                    renamed_file = file.replace(
                        'Valumaaluejako_purkupiste', 'catchment_discharge_point'
                    )
                os.rename(
                    os.path.join(folder_path, file),
                    os.path.join(folder_path, renamed_file)
                )

        return 'All downloads are complete.'

    def select_single_subcatchment(
        self,
        input_file: str,
        level: int,
        single_area: int,
        output_file: typing.Optional[str] = None,
        merge_polygons: bool = True,
        percentage_cutoff: float = 0,
        **kwargs: typing.Any
    ) -> geopandas.GeoDataFrame:

        '''
        Selects a single subcatchment from the shapefile of
        Syke's catachment divisions and returns a GeoDataFrame.

        Parameters
        ----------
        input_file : str
            Path to the shapefile of catchment area divisions, obtained from the
            :meth: `SuomiGeoData.Syke.download_catchment_divisions_2023` method.

        level : int
            Catchment division level, must be one of 1, 2, 3, 4, or 5.

        single_area : int
            Selected value from the 'taso<level>_osai' column in the shapefile.

        output_file : str, optional
            File path to save the ouput GeoDataFrame.

        merge_polygons : bool, optional
            Merges the polygons using the :meth:`geopandas.GeoDataFrame.dissolve` method
            and explodes them with the :meth:`geopandas.GeoDataFrame.explode` method. If False,
            no operation is performed.

        percentage_cutoff : float, optional
            Excludes polygon below the specified area percentage, ranging from 0 to 100,
            relative to the total area of all polygons. Default is 0, excluding negligible polygons.
            Provide -1 for no exclusion.

        **kwargs : optional
            Additional keyword arguments for the
            :meth:`geopandas.GeoDataFrame.to_file` method.

        Returns
        -------
        GeoDataFrame
            GeoDataFrame containing the selected subcatchment.
        '''

        # check level
        if level in [1, 2, 3, 4, 5]:
            pass
        else:
            raise Exception('Input level must be one of 1, 2, 3, 4, or 5.')

        # input GeoDataFrame
        gdf = geopandas.read_file(input_file)

        # processing of the selected suncatchment
        area_col = f'taso{level}_osai'
        area_gdf = gdf[gdf[area_col].isin([single_area])].reset_index(drop=True)
        if area_gdf.shape[0] == 0:
            raise Exception('The index map does not intersect with the given area.')
        else:
            area_gdf = area_gdf.drop(
                columns=['muutospvm', 'Shape_STAr', 'Shape_STLe']
            )
            area_gdf[area_col] = area_gdf[area_col].astype('int')
            id_col = area_col.replace('_osai', '_id')
            area_gdf[id_col] = area_gdf[id_col].astype('int')

        # merging polygons
        if area_gdf.geometry.iloc[0].geom_type == 'Polygon':
            pass
        else:
            if merge_polygons is True:
                area_gdf = area_gdf.dissolve()
                area_gdf = area_gdf[['geometry']]
                area_gdf = area_gdf.explode(ignore_index=True)
                area_gdf['PID'] = list(range(1, area_gdf.shape[0] + 1))
            else:
                pass
            # removing negligible polygons
            if percentage_cutoff < 0:
                pass
            else:
                total_area = area_gdf.geometry.area.sum()
                area_gdf['area_%'] = round(100 * area_gdf.geometry.area / total_area).astype('int')
                area_gdf = area_gdf[area_gdf['area_%'] > percentage_cutoff].reset_index(drop=True)
                area_gdf = area_gdf.drop(columns=['area_%'])
                area_gdf['PID'] = list(range(1, area_gdf.shape[0] + 1))

        # saving the geodataframe
        if output_file is None:
            pass
        else:
            check_file = Core().is_valid_ogr_driver(output_file)
            # invalid file
            if check_file is False:
                raise Exception(
                    'Could not retrieve driver from the file path.'
                )
            else:
                # saving the output GeoDataFrame
                area_gdf.to_file(
                    output_file,
                    **kwargs
                )

        return area_gdf

    def merging_multiple_subcatchments(
        self,
        input_file: str,
        level: int,
        multiple_area: list[int],
        output_file: typing.Optional[str] = None,
        percentage_cutoff: float = -1,
        **kwargs: typing.Any
    ) -> geopandas.GeoDataFrame:

        '''
        Selects multiple subcatchments from the shapefile of
        Syke's catachment divisions and returns a GeoDataFrame.

        Parameters
        ----------
        input_file : str
            Path to the shapefile of catchment area divisions, obtained from the
            :meth: `SuomiGeoData.Syke.download_catchment_divisions_2023` method.

        level : int
            Catchment division level, must be one of 1, 2, 3, 4, or 5.

        multiple_area : list of int
            List of selected integer values from the 'taso<level>_osai' column in the shapefile.

        output_file : str, optional
            File path to save the output GeoDataFrame.

        percentage_cutoff : float, optional
            Excludes polygon below the specified area percentage, ranging between 0 to 100,
            relative to the total area of all polygons. Default is -1 for no exclusion.

        **kwargs : optional
            Additional keyword arguments for the
            :meth:`geopandas.GeoDataFrame.to_file` method.

        Returns
        -------
        GeoDataFrame
            GeoDataFrame containing the selected subcatchments.
        '''

        # check level
        if level in [1, 2, 3, 4, 5]:
            pass
        else:
            raise Exception('Input level must be one of 1, 2, 3, 4, or 5.')

        # check multiple subcatchments
        if len(multiple_area) > 1:
            pass
        else:
            raise Exception('Input multiple area list contains single element.')

        # input GeoDataFrame
        gdf = geopandas.read_file(input_file)

        # processing of selected subcatchments
        area_col = f'taso{level}_osai'
        area_gdf = gdf[gdf[area_col].isin(multiple_area)].reset_index(drop=True)
        if area_gdf.shape[0] == 0:
            raise Exception('The index map does not intersect with the given area.')
        else:
            area_gdf = area_gdf.drop(
                columns=['muutospvm', 'Shape_STAr', 'Shape_STLe']
            )
            area_gdf['geometry'] = area_gdf['geometry'].apply(lambda x: shapely.union_all(x))
            area_gdf[area_col] = area_gdf[area_col].astype('int')
            id_col = area_col.replace('_osai', '_id')
            area_gdf[id_col] = area_gdf[id_col].astype('int')
            area_gdf = area_gdf.dissolve()
            area_gdf = area_gdf[['geometry']]
            area_gdf = area_gdf.explode(ignore_index=True)
            area_gdf['PID'] = list(range(1, area_gdf.shape[0] + 1))
            # removing negligible polygons
            if percentage_cutoff < 0:
                pass
            else:
                total_area = area_gdf.geometry.area.sum()
                area_gdf['area_%'] = round(100 * area_gdf.geometry.area / total_area).astype('int')
                area_gdf = area_gdf[area_gdf['area_%'] > percentage_cutoff].reset_index(drop=True)
                area_gdf = area_gdf.drop(columns=['area_%'])
                area_gdf['PID'] = list(range(1, area_gdf.shape[0] + 1))

        # saving the geodataframe
        if output_file is None:
            pass
        else:
            check_file = Core().is_valid_ogr_driver(output_file)
            # invalid file
            if check_file is False:
                raise Exception(
                    'Could not retrieve driver from the file path.'
                )
            else:
                area_gdf.to_file(
                    output_file,
                    **kwargs
                )

        return area_gdf
