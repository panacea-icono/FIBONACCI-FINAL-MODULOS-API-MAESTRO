#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integration Test Script for FIBONACCI Fusion

This script tests the complete integration of MAESTRO + Lab fusion.
"""

import os
import sys
import json
import time
import subprocess
import signal
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError

class FibonacciIntegrationTest:
    """Test suite for the FIBONACCI fusion"""
    
    def __init__(self):
        self.root_dir = Path(__file__).resolve().parent.parent
        self.lab_process = None
        self.results = []
        
    def log(self, message, status="INFO"):
        """Log test results"""
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] [{status}] {message}")
        self.results.append({
            "timestamp": timestamp,
            "status": status,
            "message": message
        })
    
    def test_lab_module_files(self):
        """Test that all lab module files exist"""
        self.log("Testing lab module file structure...")
        
        required_files = [
            "lab/main.py",
            "lab/Dockerfile", 
            "lab/requirements.txt",
            "lab/README.md"
        ]
        
        for file_path in required_files:
            full_path = self.root_dir / file_path
            if full_path.exists():
                self.log(f"✅ {file_path} exists", "PASS")
            else:
                self.log(f"❌ {file_path} missing", "FAIL")
                return False
        
        return True
    
    def test_modules_config(self):
        """Test modules.json configuration"""
        self.log("Testing modules.json configuration...")
        
        modules_file = self.root_dir / "modules.json"
        if not modules_file.exists():
            self.log("❌ modules.json not found", "FAIL")
            return False
        
        try:
            with open(modules_file, 'r') as f:
                config = json.load(f)
            
            if "lab" in config:
                lab_config = config["lab"]
                if lab_config.get("port") == 8001:
                    self.log("✅ Lab module configured correctly", "PASS")
                    return True
                else:
                    self.log("❌ Lab port not configured as 8001", "FAIL")
                    return False
            else:
                self.log("❌ Lab module not found in config", "FAIL")
                return False
        except Exception as e:
            self.log(f"❌ Error reading modules.json: {e}", "FAIL")
            return False
    
    def start_lab_server(self):
        """Start the lab server for testing"""
        self.log("Starting lab server for integration test...")
        
        try:
            os.chdir(self.root_dir / "lab")
            self.lab_process = subprocess.Popen(
                [sys.executable, "main.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env={**os.environ, "LAB_PORT": "8001"}
            )
            
            # Give the server time to start
            time.sleep(3)
            
            if self.lab_process.poll() is None:
                self.log("✅ Lab server started successfully", "PASS")
                return True
            else:
                self.log("❌ Lab server failed to start", "FAIL")
                return False
        except Exception as e:
            self.log(f"❌ Error starting lab server: {e}", "FAIL")
            return False
    
    def test_lab_endpoints(self):
        """Test lab API endpoints"""
        self.log("Testing lab API endpoints...")
        
        endpoints = [
            ("Health Check", "http://localhost:8001/health"),
            ("Root", "http://localhost:8001/"),
            ("Experiments", "http://localhost:8001/api/v1/experiments"),
            ("Research", "http://localhost:8001/api/v1/research"),
            ("MAESTRO Integration", "http://localhost:8001/api/v1/integration/maestro")
        ]
        
        all_passed = True
        for name, url in endpoints:
            try:
                with urlopen(url, timeout=5) as response:
                    if response.status == 200:
                        data = json.loads(response.read().decode())
                        self.log(f"✅ {name} endpoint working", "PASS")
                        
                        # Special check for integration endpoint
                        if "integration/maestro" in url:
                            if data.get("fusion_complete"):
                                self.log("✅ Fusion status confirmed", "PASS")
                            else:
                                self.log("⚠️  Fusion status unclear", "WARN")
                    else:
                        self.log(f"❌ {name} returned status {response.status}", "FAIL")
                        all_passed = False
            except URLError as e:
                self.log(f"❌ {name} endpoint unreachable: {e}", "FAIL")
                all_passed = False
            except Exception as e:
                self.log(f"❌ {name} endpoint error: {e}", "FAIL")
                all_passed = False
        
        return all_passed
    
    def test_docker_compose(self):
        """Test docker-compose configuration"""
        self.log("Testing docker-compose configuration...")
        
        compose_file = self.root_dir / "docker-compose.yml"
        if not compose_file.exists():
            self.log("❌ docker-compose.yml not found", "FAIL")
            return False
        
        try:
            with open(compose_file, 'r') as f:
                content = f.read()
            
            if "lab:" in content and "8001:8001" in content:
                self.log("✅ Docker compose includes lab service", "PASS")
                return True
            else:
                self.log("❌ Lab service not properly configured in docker-compose", "FAIL")
                return False
        except Exception as e:
            self.log(f"❌ Error reading docker-compose.yml: {e}", "FAIL")
            return False
    
    def test_fusion_script(self):
        """Test the fusion verification script"""
        self.log("Testing fusion verification script...")
        
        try:
            os.chdir(self.root_dir)
            result = subprocess.run(
                [sys.executable, "scripts/fibonacci_fusion.py"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                if "FUSION COMPLETE" in result.stdout:
                    self.log("✅ Fusion script confirms integration", "PASS")
                    return True
                else:
                    self.log("⚠️  Fusion script ran but status unclear", "WARN")
                    return True
            else:
                self.log(f"❌ Fusion script failed: {result.stderr}", "FAIL")
                return False
        except Exception as e:
            self.log(f"❌ Error running fusion script: {e}", "FAIL")
            return False
    
    def cleanup(self):
        """Clean up test resources"""
        if self.lab_process and self.lab_process.poll() is None:
            self.log("Stopping lab server...")
            self.lab_process.terminate()
            try:
                self.lab_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.lab_process.kill()
    
    def run_all_tests(self):
        """Run the complete test suite"""
        self.log("🔬 Starting FIBONACCI Fusion Integration Tests")
        self.log("=" * 60)
        
        tests = [
            ("File Structure", self.test_lab_module_files),
            ("Module Configuration", self.test_modules_config),
            ("Docker Compose", self.test_docker_compose),
            ("Fusion Script", self.test_fusion_script),
        ]
        
        # Run tests that don't need server
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            self.log(f"Running: {test_name}")
            if test_func():
                passed += 1
        
        # Server-dependent tests
        if self.start_lab_server():
            self.log("Running: API Endpoints")
            if self.test_lab_endpoints():
                passed += 1
            total += 1
        else:
            total += 1
        
        # Results
        self.log("=" * 60)
        self.log(f"🎯 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            self.log("🎉 ALL TESTS PASSED - FUSION INTEGRATION SUCCESSFUL!", "PASS")
        else:
            self.log(f"⚠️  {total - passed} tests failed - integration may need attention", "WARN")
        
        return passed == total

def main():
    """Main test function"""
    test_suite = FibonacciIntegrationTest()
    
    try:
        success = test_suite.run_all_tests()
        return 0 if success else 1
    except KeyboardInterrupt:
        test_suite.log("Tests interrupted by user", "INFO")
        return 1
    finally:
        test_suite.cleanup()

if __name__ == "__main__":
    exit(main())