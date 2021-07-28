# club_data_loader

club_data_loader is a Python sript for loading new club data into our DB.

## Installation

run the following commands before running the script

```bash
python -c 'import pandas'
```
```bash
python -m pip install openpyxl 
```

## Usage
Assuming your Excel files are in your working directory.
If that is not the case use the global path to the files.
```python
python main.py <data_base_file_path> <new_club_data_path> <club_id>
```

