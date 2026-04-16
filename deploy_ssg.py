#!/usr/bin/env python3

import subprocess
import datetime

def main():
    print("🚀 Commencing One-Way Push to the Empire's Showcase...")

    try:
        # Add all files in the current directory (public/) to the staging area
        subprocess.run(['git', 'add', '.'], check=True)
        print(f"✅ Added all files to the staging area.")

        # Commit changes with a message indicating an auto-deploy
        commit_message = f"Auto-deploy: Update SSG ({datetime.datetime.now()})"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        print(f"✅ Committed changes with message: '{commit_comment}'")

        # Push the changes to the remote repository (e.g., GitHub/GitLab)
        subprocess.run(['git', 'push'], check=True)
        print("✅ 2億円のショーウィンドウ、世界へ射出完了（っさ）")
        
    except subprocess.CalledProcessError as e:
        print(f"🚨 Error during Git operation: {e}")
        exit(1)

if __name__ == "__main__":
    main()