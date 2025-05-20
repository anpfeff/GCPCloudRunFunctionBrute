# GCP Cloud Function Brute Forcer

This tool is designed to help security researchers and penetration testers identify publicly accessible GCP Cloud Functions that may lack proper authentication. It works by brute-forcing potential function names based on a provided prefix and a wordlist.

**Disclaimer:** This tool is for educational and ethical security testing purposes only.  It should not be used to access systems without explicit permission.  The author is not responsible for any misuse of this tool.

## Purpose

GCP Cloud Functions are serverless functions that can be exposed via HTTP.  If these functions are not properly secured, they may be vulnerable to unauthorized access. This tool helps identify such vulnerabilities by systematically checking a list of possible function names.

## Features

* Brute-force discovery of publicly accessible GCP Cloud Functions.
* Supports customizable wordlists.
* Multi-threaded for faster enumeration.
* Output is saved to a file.
* Can be used with or without Docker.
* Clear progress indication during enumeration.
* Accepts project and region as input.

## Requirements

* Python 3.6 or later
* `requests` library
* `argparse` library (included in Python 3)
* A wordlist of possible function name suffixes.
* GCP Project ID
* GCP Region

## Installation

### Without Docker

1.  Clone the repository:

```bash
git clone <repository_url>
cd GCPCloudRunFunctionBrute
```

2.  Install the required Python packages:

```bash
pip install -r requirements.txt
```

### With Docker

1.  Clone the repository:

```bash
git clone <repository_url>
cd GCPCloudRunFunctionBrute
```

2.  Build the Docker image:

```bash
docker build -t gcp_function_brute .
```

## Usage

### Without Docker

```bash
python gcp_function_brute.py -p <project_id> -r <region> -w <wordlist_file> -o <output_file> [-t <num_threads>]
```

### With Docker

```bash
docker run --rm -v /path/to/your/wordlist.txt:/wordlist.txt -v /path/to/your/output.txt:/output.txt gcp_function_brute -p <project_id> -r <region> -w /wordlist.txt -o /output.txt [-t <num_threads>]
```

### Arguments

- `-p`, `--project`: GCP Project ID (required).
- `-r`, `--region`: GCP Region (e.g., `us-central1`) (required).
- `-w`, `--wordlist`: Path to the wordlist file containing possible function name suffixes (required).
- `-o`, `--out-file`: Path to the file where results will be saved (required).
- `-t`, `--threads`: Number of threads to use (optional, default: 20). Increasing this can improve performance, but may also increase the risk of being rate-limited.

### Example

To run the tool with a wordlist named `function_names.txt`, project ID `my-gcp-project`, region `us-central1`, output file `found_functions.txt`, and 30 threads, you would use the following command:

**Without Docker:**

```bash
python gcp_function_brute.py -p my-gcp-project -r us-central1 -w function_names.txt -o found_functions.txt -t 30
```

**With Docker:**

```bash
docker run --rm -v ./function_names.txt:/wordlist.txt -v ./found_functions.txt:/output.txt gcp_function_brute -p my-gcp-project -r us-central1 -w /wordlist.txt -o /output.txt -t 30
```

## Wordlist Generation

You can generate a wordlist using a tool like `cewl` or `crunch`, or with a custom script. A simple Python script is provided below as an example. Save it as `generate_wordlist.py`:

```python
import itertools
import argparse
import string

def generate_wordlist(prefix, length=4, mode='hex'):
    if mode == 'hex':
        chars = '0123456789abcdef'
    elif mode == 'lowercase':
        chars = string.ascii_lowercase
    else:
        raise ValueError("Invalid mode. Choose 'hex' or 'lowercase'.")

    wordlist = []
    for suffix in itertools.product(chars, repeat=length):
        wordlist.append(prefix + "".join(suffix))
    return wordlist

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a wordlist with a specified prefix and character set.")
    parser.add_argument("--prefix", help="The prefix for the generated words.")
    parser.add_argument("--length", type=int, default=4, help="The length of the suffix.")
    parser.add_argument("--mode", choices=['hex', 'lowercase'], default='hex', help="The character set for the suffix ('hex' or 'lowercase').")
    args = parser.parse_args()

    try:
        wordlist = generate_wordlist(args.prefix, args.length, args.mode)
        for word in wordlist:
            print(word)
    except ValueError as e:
        print(f"Error: {e}")
```

To generate a wordlist of lowercase 4-character suffixes with the prefix "my-function-", save the script and run:

```bash
python generate_wordlist.py --prefix my-function- --mode lowercase > wordlist.txt
```

This will create a file named `wordlist.txt` containing the generated function names.

## Output

The tool will print the following to the console:

- Progress of the enumeration, showing the number of URLs checked and the current URL being checked.
- Any found Cloud Function URLs.
- Any errors encountered during the process.
- The total time taken for the enumeration.

The found Cloud Function URLs are also saved to the specified output file.

## Disclaimer

This tool is intended for educational and ethical security testing purposes only. Any unauthorized use of this tool is strictly prohibited.


