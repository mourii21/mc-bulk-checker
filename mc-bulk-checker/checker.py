import requests
import time
import os
import codecs

BANNER = r"""                                                 
                              █      █    ▒████   ███    
                                           █▒  ▓█   █    
 ██▓█▓   ███   █   █   █▒██▒ ███    ███         █   █    
 █▒█▒█  █▓ ▓█  █   █   ██  █   █      █        ▒█   █    
 █ █ █  █   █  █   █   █       █      █       ░█▒   █    
 █ █ █  █   █  █   █   █       █      █      ░█▒    █    
 █ █ █  █   █  █   █   █       █      █     ▒█▒     █    
 █ █ █  █▓ ▓█  █▒ ▓█   █       █      █    ▒█░      █    
 █ █ █   ███   ▒██▒█   █     █████  █████  ██████ █████  
"""

def check_bulk_usernames(username_list):
    encoded_url = "uggcf://ncv.zbwnat.pbz/cebsvyrf/zvarpensg"
    url = codecs.decode(encoded_url, "rot13")
    
    results = {}
    for name in username_list:
        results[name.lower()] = "Available"
        
    try:
        response = requests.post(url, json=username_list, timeout=10)
        
        if response.status_code == 200:
            existing_profiles = response.json()
            for profile in existing_profiles:
                taken_name = profile['name'].lower()
                uuid = profile['id']
                results[taken_name] = f"Unavailable (UUID: {uuid})"
            return results
            
        # 429 means your IP is sending requests too fast
        elif response.status_code == 429:
            print("rate limit")
            return "RATE_LIMIT"
            
        else:
            print(f"Error: {response.status_code}")
            return "ERROR"
            
    except Exception as e:
        print(f"Bad Conection: {e}")
        return "ERROR"

if __name__ == "__main__":
    # Prints your stylized text art directly at start runtime
    print(BANNER)
    print("https://github.com/mourii21/mc-bulk-checker.git")
    
    input_file = "names.txt"
    output_file = "available.txt"
    
    if not os.path.exists(input_file):
        print(f"Error: Could not find '{input_file}' on your system.")
        print("Please create a text file named 'names.txt' in the same folder as this script.")
    else:
        with open(input_file, "r", encoding="utf-8") as file:
            all_usernames = [line.strip() for line in file if line.strip() and (3 <= len(line.strip()) <= 16)]
            
        total_names = len(all_usernames)
        print(f"Loaded {total_names} valid usernames to process.\n")
        
        available_found = []
        chunk_size = 10  # Mojang limits bulk profile calls to 10 max per array
        i = 0
        
        while i < total_names:
            chunk = all_usernames[i:i + chunk_size]
            current_batch_num = (i // chunk_size) + 1
            total_batches = (total_names + chunk_size - 1) // chunk_size
            
            print(f"Checking batch {current_batch_num}/{total_batches}: {chunk}...")
            
            batch_results = check_bulk_usernames(chunk)
            
            if batch_results == "RATE_LIMIT":
                print("required sleep")
                time.sleep(15)
                continue  # Retry the exact same batch without advancing index
                
            elif batch_results == "ERROR":
                print("required sleep")
                time.sleep(5)
                continue  # Retry the exact same batch
                
            # Process and display the output results of this verified batch
            for name in chunk:
                status = batch_results.get(name.lower(), "Available")
                print(f"  {name}: {status}")
                if "Available" in status:
                    available_found.append(name)
            
            print("")
            i += chunk_size
            # 3-second standard delay window between clean requests to stay safely under thresholds
            time.sleep(3)
            
        # Automatically save discovered unclaimed names straight to a text document
        print("Complete")
        if available_found:
            with open(output_file, "w", encoding="utf-8") as out:
                for name in available_found:
                    out.write(f"{name}\n")
            print(f"Found {len(available_found)} available names.")
            print(f"Saved results out to: '{output_file}'")
        else:
            print("No available usernames were detected in this list.")
