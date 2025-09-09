#!/usr/bin/env python3
"""
Integration Validation Script
Validates the complete integration of repositories and provides detailed report
"""
import json
import subprocess
import sys
from pathlib import Path
import requests

def check_repo_accessibility(url):
    """Check if a GitHub repository is accessible"""
    try:
        response = requests.head(url, timeout=10)
        return response.status_code, response.reason
    except requests.RequestException as e:
        return None, str(e)

def check_submodule_status():
    """Check Git submodule status"""
    try:
        result = subprocess.run(['git', 'submodule', 'status'], 
                               capture_output=True, text=True, cwd=Path.cwd())
        if result.returncode == 0:
            return result.stdout.strip().split('\n') if result.stdout.strip() else []
        else:
            return None
    except Exception:
        return None

def check_dockerfiles():
    """Find and analyze Dockerfiles in the project"""
    dockerfiles = []
    for dockerfile in Path.cwd().glob('**/Dockerfile'):
        if '.git' not in str(dockerfile):
            dockerfiles.append(dockerfile)
    return dockerfiles

def main():
    print("🔍 INTEGRATION VALIDATION REPORT")
    print("=" * 50)
    
    # 1. Check modules.json files
    original_modules_file = Path("modules.json")
    verified_modules_file = Path("modules_verified.json")
    
    print("\n📄 Configuration Files:")
    if original_modules_file.exists():
        with open(original_modules_file) as f:
            original_modules = json.load(f)
        print(f"✅ modules.json: {len(original_modules)} modules defined")
    else:
        print("❌ modules.json: Not found")
        original_modules = {}
    
    if verified_modules_file.exists():
        with open(verified_modules_file) as f:
            verified_modules = json.load(f)
        print(f"✅ modules_verified.json: {len(verified_modules)} modules verified")
    else:
        print("❌ modules_verified.json: Not found")
        verified_modules = {}
    
    # 2. Repository Accessibility Analysis
    print("\n🌐 Repository Accessibility:")
    accessible_count = 0
    inaccessible_count = 0
    
    for name, config in original_modules.items():
        repo_url = config.get("repo")
        if not repo_url:
            continue
            
        status_code, reason = check_repo_accessibility(repo_url)
        
        if status_code in [200, 301, 302]:
            print(f"  ✅ {name}: Accessible")
            accessible_count += 1
        else:
            print(f"  ❌ {name}: Inaccessible ({status_code} {reason})")
            inaccessible_count += 1
    
    print(f"\n📊 Accessibility Summary: {accessible_count} accessible, {inaccessible_count} inaccessible")
    
    # 3. Submodule Status
    print("\n📦 Submodule Integration Status:")
    submodules = check_submodule_status()
    
    if submodules is None:
        print("❌ Could not check submodule status (not in git repo?)")
    elif not submodules:
        print("⚠️  No submodules currently integrated")
    else:
        print(f"✅ {len(submodules)} submodules integrated:")
        for submodule in submodules:
            if submodule.strip():
                parts = submodule.strip().split()
                status_char = submodule[0]
                path = parts[-1] if parts else "unknown"
                
                status_text = {
                    ' ': "initialized and up-to-date",
                    '-': "not initialized",
                    '+': "different commit checked out",
                    'U': "conflicts during merge"
                }.get(status_char, "unknown status")
                
                print(f"    {status_char} {path} ({status_text})")
    
    # 4. Docker Integration
    print("\n🐳 Docker Integration:")
    dockerfiles = check_dockerfiles()
    
    if not dockerfiles:
        print("⚠️  No Dockerfiles found")
    else:
        print(f"✅ {len(dockerfiles)} Dockerfiles found:")
        for dockerfile in dockerfiles:
            rel_path = dockerfile.relative_to(Path.cwd())
            print(f"    📄 {rel_path}")
    
    # 5. Generated Files
    print("\n🔧 Generated Configuration:")
    docker_compose_file = Path("docker-compose.yml")
    gitmodules_file = Path(".gitmodules")
    
    if docker_compose_file.exists():
        print(f"✅ docker-compose.yml: Generated")
        with open(docker_compose_file) as f:
            content = f.read()
            service_count = content.count('container_name:')
            print(f"    🏃 {service_count} services configured")
    else:
        print("❌ docker-compose.yml: Not generated")
    
    if gitmodules_file.exists():
        print(f"✅ .gitmodules: Present")
    else:
        print("❌ .gitmodules: Not found")
    
    # 6. Integration Scripts
    print("\n🛠️  Integration Scripts:")
    scripts_dir = Path("scripts")
    
    scripts_to_check = [
        "add_submodules.sh",
        "add_submodules_safe.sh", 
        "generate_docker_compose.py",
        "hf_connect.py"
    ]
    
    for script_name in scripts_to_check:
        script_path = scripts_dir / script_name
        if script_path.exists():
            print(f"    ✅ {script_name}: Available")
        else:
            print(f"    ❌ {script_name}: Missing")
    
    # 7. Summary and Recommendations
    print("\n🎯 SUMMARY AND RECOMMENDATIONS:")
    print("-" * 30)
    
    if verified_modules_file.exists() and len(verified_modules) > 0:
        print("✅ Integration successfully validated")
        print("✅ Verified modules configuration created")
        
        if submodules and len(submodules) > 0:
            print("✅ Submodules successfully integrated")
        else:
            print("⚠️  Run integration script to add submodules")
        
        if docker_compose_file.exists():
            print("✅ Docker configuration generated")
        else:
            print("⚠️  Run generate_docker_compose.py")
    else:
        print("❌ Integration not completed")
        print("🔧 Recommended actions:")
        print("   1. Run repository validation script")
        print("   2. Create modules_verified.json with accessible repos")
        print("   3. Run add_submodules_safe.sh")
        print("   4. Generate docker-compose configuration")
    
    print("\n✨ Integration validation complete!")

if __name__ == "__main__":
    main()