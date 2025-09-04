#!/usr/bin/env python3
"""
Workflow validation script for GitHub Actions
Validates YAML syntax and workflow structure
"""
import yaml
import os
import sys
from pathlib import Path

def validate_yaml(file_path):
    """Validate YAML syntax"""
    try:
        with open(file_path, 'r') as file:
            yaml.safe_load(file)
        return True, "Valid YAML"
    except yaml.YAMLError as e:
        return False, f"Invalid YAML: {e}"
    except Exception as e:
        return False, f"Error reading file: {e}"

def validate_workflow_structure(workflow_data, file_name):
    """Validate workflow structure"""
    required_keys = ['name', 'jobs']
    issues = []
    
    # Check for 'on' key (it might be parsed as True due to YAML issues)
    has_on_trigger = 'on' in workflow_data or True in workflow_data
    if not has_on_trigger:
        issues.append("Missing required key: 'on'")
    
    for key in required_keys:
        if key not in workflow_data:
            issues.append(f"Missing required key: '{key}'")
    
    # Check for jobs
    if 'jobs' in workflow_data:
        for job_name, job_data in workflow_data['jobs'].items():
            if 'runs-on' not in job_data:
                issues.append(f"Job '{job_name}' missing 'runs-on'")
            
            if 'steps' in job_data:
                for i, step in enumerate(job_data['steps']):
                    if 'name' not in step and 'uses' not in step:
                        issues.append(f"Job '{job_name}' step {i+1} missing 'name' or 'uses'")
    
    return len(issues) == 0, issues

def main():
    """Main validation function"""
    workflows_dir = Path('.github/workflows')
    
    if not workflows_dir.exists():
        print("❌ .github/workflows directory not found")
        return False
    
    workflow_files = list(workflows_dir.glob('*.yml')) + list(workflows_dir.glob('*.yaml'))
    
    if not workflow_files:
        print("❌ No workflow files found")
        return False
    
    print("🔍 Validating GitHub Actions workflows...")
    print("=" * 50)
    
    all_valid = True
    
    for workflow_file in workflow_files:
        print(f"\n📄 Validating {workflow_file.name}...")
        
        # Validate YAML syntax
        is_valid_yaml, yaml_message = validate_yaml(workflow_file)
        if not is_valid_yaml:
            print(f"❌ {yaml_message}")
            all_valid = False
            continue
        else:
            print(f"✅ {yaml_message}")
        
        # Validate workflow structure
        with open(workflow_file, 'r') as file:
            workflow_data = yaml.safe_load(file)
        
        is_valid_structure, structure_issues = validate_workflow_structure(workflow_data, workflow_file.name)
        if not is_valid_structure:
            print(f"❌ Structure issues:")
            for issue in structure_issues:
                print(f"   - {issue}")
            all_valid = False
        else:
            print(f"✅ Valid workflow structure")
    
    print("\n" + "=" * 50)
    if all_valid:
        print("🎉 All workflows are valid!")
        return True
    else:
        print("❌ Some workflows have issues. Please fix them before committing.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
