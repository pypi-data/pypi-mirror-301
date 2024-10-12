from typing import List, Optional, Dict, Iterable, Any, overload
import io
import collections.abc
from datetime import datetime
from aspose.pyreflection import Type
import aspose.pycore
import aspose.pydrawing
import aspose.cells
import aspose.cells.charts
import aspose.cells.digitalsignatures
import aspose.cells.drawing
import aspose.cells.drawing.activexcontrols
import aspose.cells.drawing.equations
import aspose.cells.drawing.texts
import aspose.cells.externalconnections
import aspose.cells.json
import aspose.cells.markup
import aspose.cells.metadata
import aspose.cells.numbers
import aspose.cells.ods
import aspose.cells.pivot
import aspose.cells.properties
import aspose.cells.querytables
import aspose.cells.rendering
import aspose.cells.rendering.pdfsecurity
import aspose.cells.revisions
import aspose.cells.saving
import aspose.cells.settings
import aspose.cells.slicers
import aspose.cells.slides
import aspose.cells.tables
import aspose.cells.timelines
import aspose.cells.utility
import aspose.cells.vba
import aspose.cells.webextensions

class ConversionUtility:
    
    @overload
    @staticmethod
    def convert(source : str, save_as : str) -> None:
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def convert(source : str, load_options : aspose.cells.LoadOptions, save_as : str, save_options : aspose.cells.SaveOptions) -> None:
        raise NotImplementedError()
    

class ExportRangeToJsonOptions:
    '''Indicates the options that exporting range to json.'''
    
    @property
    def has_header_row(self) -> bool:
        '''Indicates whether the range contains header row.'''
        raise NotImplementedError()
    
    @has_header_row.setter
    def has_header_row(self, value : bool) -> None:
        '''Indicates whether the range contains header row.'''
        raise NotImplementedError()
    
    @property
    def export_as_string(self) -> bool:
        '''Exports the string value of the cells to json.'''
        raise NotImplementedError()
    
    @export_as_string.setter
    def export_as_string(self, value : bool) -> None:
        '''Exports the string value of the cells to json.'''
        raise NotImplementedError()
    
    @property
    def export_empty_cells(self) -> bool:
        '''Indicates whether exporting empty cells as null.'''
        raise NotImplementedError()
    
    @export_empty_cells.setter
    def export_empty_cells(self, value : bool) -> None:
        '''Indicates whether exporting empty cells as null.'''
        raise NotImplementedError()
    
    @property
    def indent(self) -> str:
        '''Indicates the indent.'''
        raise NotImplementedError()
    
    @indent.setter
    def indent(self, value : str) -> None:
        '''Indicates the indent.'''
        raise NotImplementedError()
    

class JsonLayoutOptions:
    '''Represents the options of json layout type.'''
    
    @property
    def array_as_table(self) -> bool:
        '''Processes Array as table.'''
        raise NotImplementedError()
    
    @array_as_table.setter
    def array_as_table(self, value : bool) -> None:
        '''Processes Array as table.'''
        raise NotImplementedError()
    
    @property
    def ignore_null(self) -> bool:
        '''Indicates whether ignoring null value.'''
        raise NotImplementedError()
    
    @ignore_null.setter
    def ignore_null(self, value : bool) -> None:
        '''Indicates whether ignoring null value.'''
        raise NotImplementedError()
    
    @property
    def ignore_array_title(self) -> bool:
        '''Indicates whether ignore title if array is a property of object.'''
        raise NotImplementedError()
    
    @ignore_array_title.setter
    def ignore_array_title(self, value : bool) -> None:
        '''Indicates whether ignore title if array is a property of object.'''
        raise NotImplementedError()
    
    @property
    def ignore_object_title(self) -> bool:
        '''Indicates whether ignore title if object is a property of object.'''
        raise NotImplementedError()
    
    @ignore_object_title.setter
    def ignore_object_title(self, value : bool) -> None:
        '''Indicates whether ignore title if object is a property of object.'''
        raise NotImplementedError()
    
    @property
    def ignore_title(self) -> bool:
        '''Ingores titles of attributes'''
        raise NotImplementedError()
    
    @ignore_title.setter
    def ignore_title(self, value : bool) -> None:
        '''Ingores titles of attributes'''
        raise NotImplementedError()
    
    @property
    def convert_numeric_or_date(self) -> bool:
        '''Indicates whether converting the string in json to numeric or date value.'''
        raise NotImplementedError()
    
    @convert_numeric_or_date.setter
    def convert_numeric_or_date(self, value : bool) -> None:
        '''Indicates whether converting the string in json to numeric or date value.'''
        raise NotImplementedError()
    
    @property
    def number_format(self) -> str:
        '''Gets and sets the format of numeric value.'''
        raise NotImplementedError()
    
    @number_format.setter
    def number_format(self, value : str) -> None:
        '''Gets and sets the format of numeric value.'''
        raise NotImplementedError()
    
    @property
    def date_format(self) -> str:
        '''Gets and sets the format of date value.'''
        raise NotImplementedError()
    
    @date_format.setter
    def date_format(self, value : str) -> None:
        '''Gets and sets the format of date value.'''
        raise NotImplementedError()
    
    @property
    def title_style(self) -> aspose.cells.Style:
        '''Gets and sets the style of the title.'''
        raise NotImplementedError()
    
    @title_style.setter
    def title_style(self, value : aspose.cells.Style) -> None:
        '''Gets and sets the style of the title.'''
        raise NotImplementedError()
    
    @property
    def kept_schema(self) -> bool:
        raise NotImplementedError()
    
    @kept_schema.setter
    def kept_schema(self, value : bool) -> None:
        raise NotImplementedError()
    

class JsonUtility:
    '''Represents the utility class of processing json.'''
    
    @overload
    @staticmethod
    def export_range_to_json(range : aspose.cells.Range, options : aspose.cells.utility.ExportRangeToJsonOptions) -> str:
        '''Exporting the range to json file.
        
        :param range: The range.
        :param options: The options of exporting.
        :returns: The json string value.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def export_range_to_json(range : aspose.cells.Range, options : aspose.cells.JsonSaveOptions) -> str:
        '''Exporting the range to json file.
        
        :param range: The range.
        :param options: The options of exporting.
        :returns: The json string value.'''
        raise NotImplementedError()
    
    @staticmethod
    def import_data(json : str, cells : aspose.cells.Cells, row : int, column : int, option : aspose.cells.utility.JsonLayoutOptions) -> List[int]:
        '''Import the json string.
        
        :param json: The json string.
        :param cells: The Cells.
        :param row: The row index.
        :param column: The column index.
        :param option: The options of import json string.'''
        raise NotImplementedError()
    

