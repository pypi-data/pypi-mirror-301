# Juicy Dir - Recursive File & Content Scanner

**Juicy Dir** is a pentesting tool designed to recursively scan directories for files with potentially useful extensions and search for sensitive keywords within the file contents. It efficiently handles various file types, including databases, configuration files, and even binary files such as pickled Python objects.

## Features
- Recursively scans directories and subdirectories for files with specified extensions.
- Searches the contents of files for sensitive keywords (e.g., "pass", "user", "config").
- Supports a wide variety of file formats:
  - **Text files** (`.txt`)
  - **JSON** (`.json`)
  - **YAML** (`.yaml`, `.yml`)
  - **INI/Config files** (`.ini`, `.config`)
  - **SQLite databases** (`.db`)
  - **Pickled Python objects** (`.pkl`)
- Multi-threaded for fast performance.
- Outputs results to a specified file or directly to the console.

## Installation

### Using PyPI
You can install Juicy Dir from PyPI using `pip`:

```bash
pip install juicydir
```

### From Source
To install Juicy Dir from source, clone this repository and install it using `setup.py`:

```bash
git clone https://github.com/TraxionRPh/juicydir
cd juicydir
python setup.py install
```

## Usage
Once installed, you can use `juicydir` from the command line:

```bash
juicydir -d /path/to/directory [options]
```

### Command-Line Options
- `-d, --directory`: The directory to scan (required).
- `-e, --extensions`: File extensions to search for (default: `.db`, `.txt`, `.config`, `.json`, `.yaml`, `.yml`, `.ini`, `.pkl`).
- `-k, --keywords`: Keywords to search for within files (default: `pass`, `user`, `root`, `config`, `database`).
- `-t, --threads`: Number of threads to use (default: 4).
- `-p, --depth`: Limit the depth of directory recursion.
- `-o, --outfile`: Specify the output file to save results (default: `juicydir.txt`).
- `-v, --version`: Show the version of Juicy Dir.

## Examples

### Basic usage:
```bash
juicydir -d /path/to/directory
```

### Specify file extensions to search for:
```bash
juicydir -d /path/to/directory -e .txt .json
```

### Search with custom keywords:
```bash
juicydir -d /path/to/directory -k password secret token
```

### Save results to a custom output file:
```bash
juicydir -d /path/to/directory -o results.txt
```

## Example Output
When running Juicy Dir, you'll see something like this in the terminal:
```bash
     __     __  __     __     ______     __  __        _____     __     ______    
    /\ \   /\ \/\ \   /\ \   /\  ___\   /\ \_\ \      /\  __-.  /\ \   /\  == \   
   _\_\ \  \ \ \_\ \  \ \ \  \ \ \____  \ \____ \     \ \ \/\ \ \ \ \  \ \  __<   
  /\_____\  \ \_____\  \ \_\  \ \_____\  \/\_____\     \ \____-  \ \_\  \ \_\ \_\ 
  \/_____/   \/_____/   \/_/   \/_____/   \/_____/      \/____/   \/_/   \/_/ /_/ 
                                                                                   
  Juicy Dir - Recursive File & Content Scanner
  Version: 1.0.5 - Griffin Skaff (@TraxionRPh)

Searching for files in /path/to/directory...
Found keyword 'password' in /path/to/directory/config.yaml
Found keyword 'user' in /path/to/directory/data.json

Search complete. Results saved to juicydir.txt
```

## Contributing
Contributions are welcome! If you'd like to contribute, please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a Pull Request.
Please ensure that your code follows the project's coding standards and includes appropriate tests.

## License
Juicy Dir is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.