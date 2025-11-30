import time
import requests
import runpod
from realtime_phone_agents.config import settings

runpod.api_key = settings.runpod.api_key

pod = runpod.create_pod(
    name="Faster Whisper Server",
    image_name="theneuralmaze/faster-whisper-server:latest",
    gpu_type_id=settings.runpod.faster_whisper_gpu_type,
    cloud_type="SECURE",
    gpu_count=1,
    volume_in_gb=20,
    volume_mount_path="/workspace",
    ports="8000/http",
    env={
        "DEFAULT_MODEL": settings.runpod.faster_whisper_model,
        "COMPUTE_TYPE": "int8",
        "LOOPBACK_HOST_URL": "http://localhost:8000"
    },
)

print(f"Pod created: {pod.get('id')}")
pod_url = f"https://{pod.get('id')}-8000.proxy.runpod.net"
print(f"Pod URL: {pod_url}")

# Wait for the server to be ready
print("\nWaiting for server to be ready...")
max_attempts = 60
attempt = 0

while attempt < max_attempts:
    try:
        response = requests.get(f"{pod_url}/v1/models", timeout=10)
        if response.status_code == 200:
            print("✓ Server is ready!")
            break
    except requests.exceptions.RequestException as e:
        pass
    
    attempt += 1
    print(f"  Attempt {attempt}/{max_attempts} - Server not ready yet, retrying in 5 seconds...")
    time.sleep(5)

if attempt >= max_attempts:
    print("✗ Server did not become ready in time")
    exit(1)

# Download the model
print(f"\nDownloading model: {settings.runpod.faster_whisper_model}")
try:
    download_response = requests.post(
        f"{pod_url}/v1/models/{settings.runpod.faster_whisper_model}",
        timeout=300  # 5 minutes timeout for model download
    )
    
    if download_response.status_code == 200:
        print(f"✓ Model {settings.runpod.faster_whisper_model} downloaded successfully!")
    else:
        print(f"✗ Failed to download model. Status: {download_response.status_code}")
        print(f"  Response: {download_response.text}")
except requests.exceptions.RequestException as e:
    print(f"✗ Error downloading model: {e}")

# Final instructions
print("\n" + "="*70)
print("🎉 Setup complete!")
print("="*70)
print("\nPlease copy the following URL and paste it in your .env file:")
print(f"\n  RUNPOD__FASTER_WHISPER_POD_URL={pod_url}")
print("\n" + "="*70)




