import os
import typing
import pyogrio
import rasterio
import rasterio.merge
import rasterio.drivers
import rasterio.mask
import geopandas


class Core:

    '''
    Core functionality of :mod:`SuomiGeoData` module.
    '''

    def is_valid_ogr_driver(
        self,
        file_path: str
    ) -> bool:

        '''
        Returns whether the given file path is valid to write a GeoDataFrame.

        Parameters
        ----------
        file_path : str
            File path to save the GeoDataFrame.

        Returns
        -------
        bool
            True if the file path is valid, False otherwise.
        '''

        try:
            pyogrio.detect_write_driver(file_path)
            output = True
        except Exception:
            output = False

        return output

    def is_valid_raster_driver(
        self,
        file_path: str
    ) -> bool:

        '''
        Returns whether the given file path is a valid raster file.

        Parameters
        ----------
        file_path : str
            File path to save the raster.

        Returns
        -------
        bool
            True if the file path is valid, False otherwise.
        '''

        try:
            rasterio.drivers.driver_from_extension(file_path)
            output = True
        except Exception:
            output = False

        return output

    def _excel_file_extension(
        self,
        file_path: str
    ) -> str:

        '''
        Returns the extension of an Excel file.

        Parameters
        ----------
        file_path : str
            Path of the Excel file.

        Returns
        -------
        str
            Extension of the Excel file.
        '''

        output = os.path.splitext(file_path)[-1]

        return output

    @property
    def _url_prefix_paituli_dem_tdb(
        self,
    ) -> str:

        '''
        Returns the prefix url for downloading files
        based on DEM and topographic database labels.
        '''

        output = 'https://www.nic.funet.fi/index/geodata/'

        return output

    @property
    def default_http_headers(
        self,
    ) -> dict[str, str]:

        '''
        Returns the default http headers to be used for the web requests.
        '''

        output = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Connection': 'keep-alive'
        }

        return output

    def raster_merging(
        self,
        folder_path: str,
        output_file: str,
        raster_ext: str = '.tif',
        **kwargs: typing.Any
    ) -> str:

        '''
        Merges raster files and returns a confirmation message.

        Parameters
        ----------
        folder_path : str
            Folder path containing input raster files.

        output_file : str
            File path to save the output raster.

        raster_ext : str, optional
            Extension of input raster files. Defaults to '.tif' if not provided.

        **kwargs : optional
            Additional keyword arguments for updating the dictionary of
            :attr:`rasterio.profile` attribute.

        Returns
        -------
        str
            A confirmation message indicating that the raster merging is complete.
        '''

        # file paths
        if os.path.isdir(folder_path):
            file_paths = filter(
                lambda x: os.path.isfile(os.path.join(folder_path, x)),
                os.listdir(folder_path)
            )
        else:
            raise Exception(
                'The folder path does not exist.'
            )

        # extract raster files
        raster_files = filter(
            lambda x: x.endswith(raster_ext),
            file_paths
        )

        # raster merging
        check_file = self.is_valid_raster_driver(output_file)
        # output file check fail
        if check_file is False:
            raise Exception(
                'Could not retrieve driver from the file path.'
            )
        else:
            # open the split rasters
            split_rasters = [
                rasterio.open(os.path.join(folder_path, file)) for file in raster_files
            ]
            # merge the split rasters
            profile = split_rasters[0].profile
            output_array, output_transform = rasterio.merge.merge(
                sources=split_rasters
            )
            # update merged raster profile
            profile.update(
                {
                    'height': output_array.shape[1],
                    'width': output_array.shape[2],
                    'transform': output_transform
                }
            )
            for key, value in kwargs.items():
                profile[key] = value
            # save the merged raster
            with rasterio.open(output_file, 'w', **profile) as output_raster:
                output_raster.write(output_array)
            # close the split rasters
            for raster in split_rasters:
                raster.close()

        return 'Merging of rasters completed.'

    def raster_clipping_by_mask(
        self,
        input_file: str,
        mask_area: str | geopandas.GeoDataFrame,
        output_file: str,
        **kwargs: typing.Any
    ) -> str:

        '''
        Clips a raster file using a mask and returns a confirmation message.

        Parameters
        ----------
        input_file : str
            File path to the input raster.

        mask_area : str or GeoDataFrame
            Mask area either as a file path or a GeoDataFrame.

        output_file : str
            File path to save the output raster.

        **kwargs : optional
            Additional keyword arguments for updating the dictionary of
            :attr:`rasterio.profile` attribute.

        Returns
        -------
        str
            A confirmation message indicating that the raster clipping is complete.
        '''

        # mask area
        if isinstance(mask_area, str):
            mask_geometry = geopandas.read_file(mask_area).geometry.to_list()
        elif isinstance(mask_area, geopandas.GeoDataFrame):
            mask_geometry = mask_area.geometry.to_list()
        else:
            raise Exception('Input area must be either file or GeoDataFrame format.')

        # raster clipping
        check_file = self.is_valid_raster_driver(output_file)
        # output file check fail
        if check_file is False:
            raise Exception(
                'Could not retrieve driver from the file path.'
            )
        else:
            # raster clipping
            with rasterio.open(input_file) as input_raster:
                profile = input_raster.profile
                output_array, output_transform = rasterio.mask.mask(
                    dataset=input_raster,
                    shapes=mask_geometry,
                    all_touched=True,
                    crop=True
                )
                # update clipped raster profile
                profile.update(
                    {'height': output_array.shape[1],
                     'width': output_array.shape[2],
                     'transform': output_transform}
                )
                for key, value in kwargs.items():
                    profile[key] = value
                # save the clipped raster
                with rasterio.open(output_file, 'w', **profile) as output_raster:
                    output_raster.write(output_array)

        return 'Raster clipping completed.'
