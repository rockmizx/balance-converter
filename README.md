# Grand Chase Balance Converter

This repository contains a set of Python scripts designed to transfer and format values between character script files. The main purpose of these scripts is to extract specific values (such as damage values and attack properties) from one set of character scripts and apply them to another set. Additionally, the `format.py` script ensures that the source files are properly formatted before the transfer process.

## Requirements

- Python 3.x
- Decrypted character script files (using tools like `unluac`)

## Scripts Overview

### `balance_converter.py`

This script is responsible for extracting and transferring values between character script files. It handles the following:

- **Damage Values (`DAMAGETO_MONSTER`)**: Extracts and updates damage values from the source files to the destination files.
- **Attack Properties (`SetAttackProperty`)**: Extracts and updates attack properties.
- **Start Attack Properties (`StartAttack`)**: Extracts and updates start attack properties.

### `format.py`

This script ensures that the source files are properly formatted before the transfer process. It specifically reformats the `Damage` blocks to ensure consistency.

## Usage Instructions

1. **Prepare Your Files**:
   - Ensure that all character script files are decrypted (using `unluac` or similar tools).
   - Place the source character script files in one directory and the destination files in another.

2. **Run `balance_converter.py`**:
   - This script will prompt you to enter the paths to the source and destination directories.
   - It will extract the necessary values from the source files and apply them to the destination files.

   ```bash
   python balance_converter.py
   ```

3. **Run `format.py` (if needed)**:
   - If the source files have inconsistent formatting, run this script to reformat them.
   - This script will prompt you to enter the path to the source directory.

   ```bash
   python format.py
   ```

4. **Run `balance_converter.py` Again**:
   - After formatting the source files, run `balance_converter.py` again to ensure the values are correctly transferred.

   ```bash
   python balance_converter.py
   ```

## Example Workflow

1. **Initial Transfer**:
   ```bash
   python balance_converter.py
   ```
   - Enter the source and destination directories when prompted.

2. **Format Source Files**:
   ```bash
   python format.py
   ```
   - Enter the source directory when prompted.

3. **Final Transfer**:
   ```bash
   python balance_converter.py
   ```
   - Enter the source and destination directories again.

## Important Notes

- **File Types**: Only character script files should be present in the source and destination directories.
- **Decryption**: Ensure that all files are decrypted before running the scripts.
- **Backup**: Always make a backup of your files before running the scripts to avoid data loss.

## Script Details

### `balance_converter.py`

- **Extracts**:
  - Damage values (`DAMAGETO_MONSTER`).
  - Attack properties (`SetAttackProperty`).
  - Start attack properties (`StartAttack`).

- **Updates**:
  - The destination files with the extracted values from the source files.

- **Logs**:
  - All changes made during the transfer process are logged and displayed in the console.

### `format.py`

- **Reformats**:
  - The `Damage` blocks in the source files to ensure consistent formatting.

- **Usage**:
  - Run this script if the source files have inconsistent formatting that could cause issues during the transfer process.

## Contributing

If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

---

This README provides a comprehensive guide to using the scripts in this repository. Follow the instructions carefully to ensure a smooth transfer of values between your character script files.
