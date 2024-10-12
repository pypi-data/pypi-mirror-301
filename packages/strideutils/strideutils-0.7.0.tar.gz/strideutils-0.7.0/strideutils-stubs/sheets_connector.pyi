from typing import List, Dict, Optional, Tuple
import gspread
import pandas as pd

SCOPES: Tuple[str, ...]

class GoogleSheetsClient:
    _instance: Optional['GoogleSheetsClient']
    client: gspread.Client
    cache_enabled: bool
    _cache: Dict[str, pd.DataFrame]

    def __new__(cls) -> 'GoogleSheetsClient': ...

    def __init__(self, cache_enabled: bool = False) -> None: ...

    @staticmethod
    def _get_auth_client() -> gspread.Client: ...

    def grab_sheet(
            self,
            sheet_id: str,
            sheet_name: str,
            columns_labeled: bool = True,
    ) -> pd.DataFrame: ...

    def write_sheet(
            self,
            df: pd.DataFrame,
            sheet_id: str,
            sheet_name: str,
    ) -> None: ...

    def reorder_sheet(
            self,
            sheet_id: str,
            sheet_name: str,
            new_location: int = 0,
    ) -> None: ...

    def get_sheet_names(self, sheet_id: str) -> List[str]: ...
