import os
import re
import sqlite3
import json
import yaml
import configparser
import pickle
from threading import Thread
import queue

# Worker queue for multi-threaded processing
file_queue = queue.Queue()

# Default file extensions to search (can be overridden by command-line args)
EXTENSIONS = [
    # Configuration Files
    '.conf', '.config', '.ini', '.env', '.cfg', '.yaml', '.yml', 
    '.json', '.xml', '.plist', '.toml',

    # Credentials & Authentication
    '.htpasswd', '.passwd', '.pgpass', '.aws', 'docker/config.json',

    # Source Code
    '.py', '.js', '.ts', '.java', '.php', '.rb', '.go', '.c', 
    '.cpp', '.h', '.cs', '.swift', '.sh', '.bat', '.pl', '.sql',

    # Database Files
    '.db', '.sqlite', '.sqlite3', '.mdb', '.accdb', '.bak', 
    '.sql', '.ldif',

    # Logs & Debugging
    '.log', '.trace', '.dmp', '.dump', '.out', '.err',

    # Certificates & Keys
    '.pem', '.key', '.csr', '.crt', '.pfx', '.p12', '.der', 
    '.cer', '.jks', '.gpg',

    # Backup & Archive Files
    '.zip', '.tar', '.tar.gz', '.tgz', '.rar', '.7z', 
    '.bak', '.old', '.sav',

    # Virtualization & Containerization Files
    '.vmdk', '.vdi', '.qcow2', '.iso', '.ova', '.ovf', 
    '.img', '.dockerfile', '.yml',

    # Sensitive Application Files
    '.htaccess', '.gitignore', '.gitconfig', '.git', '.npmrc', 
    '.bashrc', '.bash_profile', '.bash_history', '.zshrc', '.zprofile', 
    '.zsh_history', '.vimrc', '.viminfo', '.tmux.conf',

    # Containerization & CI/CD Configuration
    '.dockerignore', 'Dockerfile', '.travis.yml', '.circleci/config.yml', 
    '.gitlab-ci.yml', 'Jenkinsfile',

    # Cloud & API Key Files
    '.aws/credentials', '.gcloud', '.kube/config', '.azure/credentials', 
    '.azure/config', '.env',

    # Miscellaneous
    '.rsa', '.dsa', '.p12', '.pfx', '.bak', '.old', '.swp', 
    '.swo', '.id_rsa', '.id_rsa.pub', '.ovpn'
]


# Default keywords to search (can be overridden by command-line args)
KEYWORDS = [
    # Credentials & Authentication
    'pass', 'password', 'passwd', 'user', 'username', 'userid', 'uid',
    'admin', 'root', 'superuser', 'su', 'credential', 'auth', 'authentication',
    'secret', 'key', 'token', 'api_key', 'access_token', 'jwt', 'login', 
    'signin', 'login_token', 'oauth', 'sso', 'auth_token', 'privilege', 
    'privileged', 'session_token',

    # Configuration Files
    'config', 'configuration', 'conf', 'settings', 'setup', 'default', 'host', 
    'hostname', 'url', 'uri', 'endpoint', 'ip', 'ip_address', 'dns', 'port',

    # Database-related
    'db', 'database', 'dbname', 'sql', 'mysql', 'postgres', 'oracle', 'sqlite', 
    'schema', 'table', 'tbl', 'db_user', 'db_pass', 'db_host', 'mongodb', 'redis',
    'couchdb', 'nosql', 'db_password', 'db_key',

    # Encryption & Security
    'rsa', 'dsa', 'ecdsa', 'key', 'ssh_key', 'private_key', 'public_key', 'cert', 
    'certificate', 'aes', 'md5', 'sha', 'sha256', 'hmac', 'pbkdf2', 'bcrypt', 
    'pfx', 'crt', 'pem', 'tls', 'ssl', 'https', 'secure', 'token', 'encryption_key',
    'decrypt', 'decrypt_key', 'cipher', 'nonce', 'sensitive', 'secret_key',

    # System Information & Logs
    'log', 'logging', 'debug', 'trace', 'error', 'warn', 'info', 'verbose', 
    'stacktrace', 'system', 'sys', 'uname', 'kernel', 'os', 'windows', 'linux', 
    'mac', 'version', 'release',

    # Cloud & Service Credentials
    'aws_access_key_id', 'aws_secret_access_key', 'aws_session_token', 'gcp', 
    'google_cloud', 'gcp_key', 'gcp_secret', 'azure', 'azure_key', 'azure_secret', 
    'azure_token', 's3_bucket', 'bucket', 'api_key', 'access_key', 'secret_key', 
    'client_id', 'client_secret',

    # Tokens & API Keys
    'api_key', 'apikey', 'api_secret', 'api_token', 'token', 'access_token', 
    'refresh_token', 'bearer_token', 'jwt', 'jws', 'oauth_token', 'oauth2', 
    'gcp_key', 'gcp_token', 'firebase_key', 'aws_key', 'aws_secret',

    # Network & Communication
    'ip', 'ip_address', 'subnet', 'gateway', 'dns', 'domain', 'dns_name', 
    'network', 'netmask', 'network_config', 'proxy', 'proxy_user', 'proxy_pass', 
    'vpn', 'tunnel', 'ftp', 'smtp', 'imap', 'pop3', 'ssh', 'telnet', 'http', 'https',

    # Environment Variables
    'env', 'environment', 'environment_variables', 'ENV', 'export', 'path', 
    'HOME', 'TMPDIR', 'LOGNAME', 'PWD', 'DB_PASS', 'DB_USER', 'DB_HOST', 
    'DB_PORT', 'SECRET_KEY', 'API_KEY', 'TOKEN',

    # File Paths & Directory Information
    'path', 'dir', 'directory', 'filepath', 'filename', 'absolute_path', 
    'relative_path', 'working_directory', 'temp', 'tmp', 'log', 'var', 'bin', 
    'home', 'etc', 'usr', 'backup', 'bkup', 'snapshot'
]

output_file = None

results_found = None

TOOL_VERSION = "1.0.7"
TOOL_AUTHOR = "Griffin Skaff @TraxionRPh"

def print_banner():
    """ Print the banner for Juicy Dir """
    banner = r"""

       __     __  __     __     ______     __  __        _____     __     ______    
      /\ \   /\ \/\ \   /\ \   /\  ___\   /\ \_\ \      /\  __-.  /\ \   /\  == \   
     _\_\ \  \ \ \_\ \  \ \ \  \ \ \____  \ \____ \     \ \ \/\ \ \ \ \  \ \  __<   
    /\_____\  \ \_____\  \ \_\  \ \_____\  \/\_____\     \ \____-  \ \_\  \ \_\ \_\ 
    \/_____/   \/_____/   \/_/   \/_____/   \/_____/      \/____/   \/_/   \/_/ /_/ 
                                                                                   
    JuicyDir - Recursive File & Content Scanner
    Version: {} - {}
        """.format(TOOL_VERSION, TOOL_AUTHOR)
    
    print(banner)

def search_files(directory, extensions, max_depth=None):
    """ Recursively search for files with specific extensions. """
    for root, dirs, files in os.walk(directory):
        current_depth = root[len(directory):].count(os.sep)
        if max_depth is not None and current_depth >= max_depth:
            dirs[:] = []
            continue

        dir_name = os.path.basename(root)
        for keyword in KEYWORDS:
            if re.search(rf'\b{keyword}\b', dir_name, re.IGNORECASE):
                log_result(f"Found keyword '{keyword}' in directory name: {root}")
        
        for file in files:
            file_path = os.path.join(root, file)
            file_name = os.path.basename(file_path)
            for keyword in KEYWORDS:
                if re.search(rf'\b{keyword}\b', file_name, re.IGNORECASE):
                    log_result(f"Found keyword '{keyword}' in file name: {file_path}")
            
            if any(file.endswith(ext) for ext in EXTENSIONS):
                file_queue.put(file_path)

def search_content(file_path, keywords):
    """ Detect file type and call appropriate handler. """
    try:
        if file_path.endswith(".db"):
            search_db(file_path, keywords)
        elif file_path.endswith(".json"):
            search_json(file_path, keywords)
        elif file_path.endswith(".yaml") or file_path.endswith(".yml"):
            search_yaml(file_path, keywords)
        elif file_path.endswith(".ini"):
            search_ini(file_path, keywords)
        elif file_path.endswith(".pkl"):
            search_pickle(file_path, keywords)
        else:
            # Fallback to plain text search for other files
            search_text_file(file_path, keywords)
    except Exception as e:
        log_result(f"Error reading {file_path}: {e}")

def search_text_file(file_path, keywords):
    """ Search for keywords in a text file. """
    global results_found
    with open(file_path, 'r', errors='ignore') as f:
        content = f.read()
        for keyword in keywords:
            if re.search(rf'\b{keyword}\b', content, re.IGNORECASE):
                log_result(f"Found keyword '{keyword}' in {file_path}")
                results_found = True
                break

def search_db(file_path, keywords):
    """ Search for sensitive data in an SQLite database. """
    global results_found
    try:
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        for table in tables:
            cursor.execute(f"SELECT * FROM {table[0]} LIMIT 5")
            rows = cursor.fetchall()
            for row in rows:
                for field in row:
                    if isinstance(field, str) and any(kw in field.lower() for kw in keywords):
                        log_result(f"Found potential sensitive data in {file_path}: {field}")
                        results_found = True
        conn.close()
    except Exception as e:
        log_result(f"Error querying database {file_path}: {e}")

def search_json(file_path, keywords):
    """ Search for sensitive data in a JSON file. """
    global results_found
    with open(file_path, 'r', errors='ignore') as f:
        try:
            data = json.load(f)
            if recursive_search(data, keywords, file_path):
                results_found = True
        except json.JSONDecodeError as e:
            log_result(f"Error parsing JSON {file_path}: {e}")

def search_yaml(file_path, keywords):
    """ Search for sensitive data in a YAML file. """
    global results_found
    with open(file_path, 'r', errors='ignore') as f:
        try:
            data = yaml.safe_load(f)
            if recursive_search(data, keywords, file_path):
                results_found = True
        except yaml.YAMLError as e:
            log_result(f"Error parsing YAML {file_path}: {e}")

def search_ini(file_path, keywords):
    """ Search for sensitive data in an INI file. """
    global results_found
    config = configparser.ConfigParser()
    try:
        config.read(file_path)
        for section in config.sections():
            for key, value in config.items(section):
                if any(kw in key.lower() or kw in value.lower() for kw in keywords):
                    log_result(f"Found potential sensitive data in {file_path}: {key} = {value}")
                    results_found = True
    except Exception as e:
        log_result(f"Error reading INI file {file_path}: as {e}")

def search_pickle(file_path, keywords):
    """ Attempt to deserialize and search a pickle file (with caution). """
    global results_found
    try:
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
            if recursive_search(data, keywords, file_path):
                results_found = True
    except Exception as e:
        log_result(f"Error reading pickle file {file_path}: {e}")

def recursive_search(data, keywords, file_path):
    """ Recursively search for sensitive data in nested structures like JSON or YAML. """
    found = False
    if isinstance(data, dict):
        for key, value in data.items():
            if any(kw in str(key).lower() or kw in str(value).lower() for kw in keywords):
                log_result(f"Found potential sensitive data in {file_path}: {key} = {value}")
                found = True
            if isinstance(value, (dict, list)) and recursive_search(value, keywords, file_path):
                found = True
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)) and recursive_search(item, keywords, file_path):
                found = True
    return found

def log_result(message):
    """ Log results to both the console and a file if requested. """
    print(message)
    if output_file:
        with open(output_file, 'a') as log_file:
            log_file.write(message + "\n")

def worker(keywords):
    """ Worker function for multithreading. """
    while not file_queue.empty():
        file_path = file_queue.get()
        search_content(file_path, keywords)
        file_queue.task_done()

def main():
    global output_file
    import argparse

    print_banner()

    parser = argparse.ArgumentParser(description="JuicyDir")

    parser.add_argument("-d", "--directory", required=True, help="The directory to search")
    parser.add_argument("-e", "--extensions", nargs='+', default=EXTENSIONS, help="File extensions to search for")
    parser.add_argument("-k", "--keywords", nargs='+', default=KEYWORDS, help="Keywords to search for within files")
    parser.add_argument("-t", "--threads", type=int, default=4, help="Number of threads to use")
    parser.add_argument("-p", "--depth", type=int, help="Limit the depth of recursion")
    parser.add_argument("-o", "--outfile", nargs="?", const="juicydir.txt", help="Specify output file (default: juicydir_log.txt)")

    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {TOOL_VERSION}", help="Show the version of this tool")

    args = parser.parse_args()

    if args.outfile:
        output_file = args.outfile
        print(f"Results will be saved to {output_file}")

    print(f"Searching for files in {args.directory}...")
    search_files(args.directory, args.extensions, args.depth)

    for i in range(args.threads):
        t = Thread(target=worker, args=(args.keywords,))
        t.start()
    
    file_queue.join()

    if results_found:
        print(f"Search complete. Results saved to {output_file}" if output_file else "Search complete.")
    else:
        print("Search complete. No results found.")

if __name__ == "__main__":
    main()