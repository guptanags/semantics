from pathlib import Path
import yaml

class FederationRegistry:
    """Application-level bridge. It contains no graph edges and is outside all three graphs."""
    def __init__(self, path):
        self.path=Path(path)
        self.data=yaml.safe_load(self.path.read_text()) if self.path.exists() else {}
        self.data=self.data or {}
        self.dataset_assets=self.data.get('dataset_to_asset', {})
        self.element_columns=self.data.get('element_to_columns', {})

    def asset_for_dataset(self, dataset_id):
        return self.dataset_assets.get(dataset_id)

    def columns_for_element(self, element_id):
        value=self.element_columns.get(element_id, [])
        return value if isinstance(value, list) else [value]
