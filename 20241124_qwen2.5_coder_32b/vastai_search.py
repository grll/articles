#!/usr/bin/env python3
"""
A utility script for searching, comparing, and deploying Vast.ai GPU instances optimized for running the Qwen2.5-Coder-32B model.

This script automates the process of:
1. Searching for RTX 4090 instances meeting specific requirements (CUDA, storage, bandwidth)
2. Calculating total costs including GPU, storage, and bandwidth
3. Displaying the top 3 most cost-effective options
4. Deploying a llama.cpp server with Qwen2.5-Coder-32B model on the selected instance

The script requires the vast.ai CLI tool to be installed and configured with valid credentials:
https://cloud.vast.ai/cli/?_gl=1*12l9h6z*_gcl_au*MTEyMjk3MjEyMC4xNzMyNDY2NTIz*_ga*MTU4Mjc0NTU2Ni4xNzMyNDY2NTI0*_ga_DG15WC8WXG*MTczMjQ2NjUyMy4xLjEuMTczMjQ2NjU0MS40Mi4wLjA.

Usage:
    python vastai_search.py
    or
    ./vastai_search.py

The script will interactively prompt for instance selection after displaying options.

**Important Note**: by default only EU countries instances are in scope.
"""
import json
import subprocess
import sys
from time import sleep

def run_vastai_search():
    cmd = [
        "vastai", "search", "offers",
        "cuda_vers>=12.6 disk_space>=30 cpu_ram>=20 gpu_name=RTX_4090 num_gpus=1 " +
        "inet_up>=200 inet_down>=200 dlperf>20 verified=true reliability>=0.99 " +
        "geolocation in [AT,BE,BG,CY,CZ,DE,DK,EE,ES,FI,FR,GR,HR,HU,IE,IT,LT,LU,LV,MT,NL,PL,PT,RO,SE,SI,SK]",
        "--raw"
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running vastai search: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON output: {e}")
        sys.exit(1)

def calculate_costs(instance):
    # Calculate monthly costs for 30GB
    storage_monthly = instance['storage_cost'] * 30 # assuming 30GB storage
    bandwidth_cost_down = instance['inet_down_cost'] * 30 # assuming 30GB down
    bandwidth_cost_up = instance['inet_up_cost'] * 10 # assuming 10GB up
    
    # Convert to hourly (30 days = 720 hours)
    storage_hourly = storage_monthly / 720
    
    # Calculate total hourly cost
    total_hourly = instance['dph_total'] + storage_hourly
    
    return {
        'base_hourly': instance['dph_total'],
        'storage_hourly': storage_hourly,
        'bandwidth_fixed': bandwidth_cost_down + bandwidth_cost_up,
        'total_hourly': total_hourly,
        'total_4hours': total_hourly * 4 + bandwidth_cost_down + bandwidth_cost_up
    }

def create_instance(instance):
    cmd = [
        "vastai", "create", "instance",
        str(instance['id']),
        "--image", "ghcr.io/ggerganov/llama.cpp:server-cuda-b4154",
        "--disk", "30",
        "--env", "-p 8081:8081",
        "--onstart-cmd", "cd / && ./llama-server --hf-repo unsloth/Qwen2.5-Coder-32B-Instruct-128K-GGUF --hf-file Qwen2.5-Coder-32B-Instruct-Q4_K_M.gguf --host 0.0.0.0 --port 8081 --gpu-layers 65 -c 15000",
        "--raw"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("Instance created successfully!")
        json_result = json.loads(result.stdout) # {'success': True, 'new_contract': 13839687}
        if not json_result['success']:
            print(f"Error: {json_result}")
            sys.exit(1)
        return json_result
    except subprocess.CalledProcessError as e:
        print(f"Error creating instance: {e}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)


def get_instance_info(instance_id):
    cmd = ["vastai", "show", "instance", str(instance_id), "--raw"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error getting instance info: {e}")
        sys.exit(1)

def wait_for_instance_ready(instance_id):
    print("Waiting for instance to be ready...")
    while True:
        instance_info = get_instance_info(instance_id)
        if not instance_info:
            print("No instance information available")
            sys.exit(1)

        if instance_info.get('actual_status') == 'running':
            port_mapping = instance_info.get('ports', {}).get('8081/tcp')[0]['HostPort']
            if port_mapping:
                print("\nInstance is ready!")
                print(f"Access the server at: http://{instance_info['public_ipaddr']}:{port_mapping}")
                print("Note that it roughly takes 10 minutes to download the model.")
                break
        
        print(".", end="", flush=True)
        sleep(5)

def main():
    # Get instances
    print("Running vastai search...")

    instances = run_vastai_search()

    print(f"Found {len(instances)} potential instances")

    for i in instances:
        costs = calculate_costs(i)
        for k, v in costs.items():
            i[k] = v

    sorted_instances = sorted(instances, key=lambda x: x['total_4hours'])
    
    # Display top 3 options
    print("\nTop 3 most affordable options including storage and bandwidth costs:")
    print("================================")
    
    for idx, instance in enumerate(sorted_instances[:3]):
        
        print(f"OPTION #{idx}")
        print(f"GPU: {instance["num_gpus"]}x {instance['gpu_name']}")
        print(f"CPU: {int(instance["cpu_cores_effective"])}/{instance["cpu_cores"]} cores - {instance["cpu_name"]}")
        print(f"RAM: {int(instance['cpu_ram'] / 1000)} GB")
        print(f"Bandwidth: {instance['inet_down']} Mbps down, {instance['inet_up']} Mbps up")
        print(f"Location: {instance['geolocation']}")

        print()

        print("Costs:")
        print(f"GPU: ${instance['base_hourly']:.3f}/hour")
        print(f"Storage (30GB): ${instance['storage_hourly']:.3f}/hour")
        print(f"Total: ${instance['total_hourly']:.3f}/hour")
    
        print(f"Bandwith (30GB down / 10GB up): ${instance['bandwidth_fixed']:.3f}")
        print(f"Total (4 hours): ${instance['total_4hours']:.3f}")
        print("--------------------------------")
    
    instance_id = input("Enter [0,1,2] to deploy on to corresponding instance (default: 0): ")
    instance_id = int(instance_id) if instance_id else 0
    instance = sorted_instances[instance_id]

    print(f"Deploying OPTION #{instance_id}...")
    response = create_instance(instance)

    # get the link info 
    wait_for_instance_ready(response["new_contract"])


if __name__ == "__main__":
    main()
