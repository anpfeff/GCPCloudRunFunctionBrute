import requests
import sys
import time
from threading import Thread, Lock
from queue import Queue
import argparse

def check_function(url, queue, results_file, lock, total_count):
    """
    Worker thread to check if a Cloud Function URL exists.

    Args:
        url (str): The URL of the Cloud Function to check.
        queue (Queue): A queue containing URLs to check.
        results_file (str): The path to the output file.
        lock (Lock): A lock to synchronize access to the output file and console.
        total_count (int): The total number of URLs to check (for progress).
    """
    while not queue.empty():
        func_url = queue.get()
        try:
            response = requests.get(func_url, timeout=10)
            if response.status_code == 200:
                with lock:
                    sys.stdout.write('\n')
                    print(f"[+] Found: {func_url}")
                    with open(results_file, "a") as f:
                        f.write(f"{func_url}\n")
            elif response.status_code != 404:
                with lock:
                    print(f"[*] Unexpected status code {response.status_code} for {func_url}")

        except requests.exceptions.RequestException as e:
            with lock:
                print(f"[-] Error checking {func_url}: {e}")
        finally:
            with lock:
                checked_count = total_count - queue.qsize()
                completed_percent = (checked_count / total_count) * 100
                print(f"Checked: {checked_count}/{total_count} ({completed_percent:.2f}%) | Now checking: {func_url}", end='\r')


def main(project_name, region, wordlist_file, results_file, num_threads):
    """
    Main function to perform the Cloud Function brute force.

    Args:
        project_name (str): The GCP project name.
        region (str): The GCP region.
        wordlist_file (str): The path to the wordlist file.
        results_file (str): The path to the output file.
        num_threads (int): The number of threads to use.
    """
    try:
        with open(wordlist_file, "r") as f:
            function_names = [line.strip() for line in f]
    except FileNotFoundError:
        print(f"Error: Wordlist file not found at {wordlist_file}")
        sys.exit(1)

    queue = Queue()
    for func_name in function_names:
        url = f"https://{region}-{project_name}.cloudfunctions.net/{func_name}"
        queue.put(url)

    total_count = queue.qsize()


    threads = []
    lock = Lock()

    print(f"Starting brute force with {num_threads} threads...")
    print(f"Project: {project_name}, Region: {region}")
    print(f"Checking {total_count} function names...")

    start_time = time.time()

    for _ in range(num_threads):
        thread = Thread(target=check_function, args=(None, queue, results_file, lock, total_count))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    duration = end_time - start_time
    print(f"\nBrute force completed in {duration:.2f} seconds.")
    print(f"Results saved to {results_file}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GCP Cloud Function Brute Forcer")
    parser.add_argument("-p", "--project", required=True, help="GCP Project Name")
    parser.add_argument("-r", "--region", required=True, help="GCP Region")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to the wordlist file")
    parser.add_argument("-o", "--out-file", required=True, help="Path to the output file")
    parser.add_argument("-t", "--threads", type=int, default=20, help="Number of threads (default: 20)")

    args = parser.parse_args()

    project_name = args.project
    region = args.region
    wordlist_file = args.wordlist
    results_file = args.out_file
    num_threads = args.threads

    main(project_name, region, wordlist_file, results_file, num_threads)

