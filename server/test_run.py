from model.matcher import IssueMatcher
import asyncio
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Sample test data
issue_data = {
    "owner": "Udayraj123",
    "repo": "OMRChecker",
    "title": "[Environment] OpenCV NULL guiReceiver error during pre-commit testing.",
    "description": "*Describe the bug\nWhile running pre-commit hooks and pytest for my application, I'm encountering an OpenCV error related to GUI functions.\n\nTo Reproduce\nSteps to reproduce the behavior:\n1. Make any changes in code.\n2. Run commands git add and pre-commit run -a (make sure pre-commit is installed).\n3. Commit changes by running git commit -m \"commit message\"\n\nScreenshots\n![Screenshot from 2024-10-03 20-23-30](https://github.com/user-attachments/assets/f0ed906b-26f1-436c-ac39-93201f049153)\n\n**Desktop (please complete the following information):**\n - OS: Ubuntu 24.04.1 LTS\n - Python version - 3.12.3\n - OpenCV version - 4.10.0",
    "labels": [
        "bug",
        "good first issue",
        "hacktoberfest",
        "up-for-grabs",
        "Easy"
    ]
}

filtered_files = [
    {
        "name": "FUNDING.yml",
        "path": ".github/FUNDING.yml",
        "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/.github/FUNDING.yml"
    },
    {
        "name": "pre-commit.yml",
        "path": ".github/pre-commit.yml",
        "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/.github/pre-commit.yml"
    },
    {
        "name": ".pre-commit-config.yaml",
        "path": ".pre-commit-config.yaml",
        "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/.pre-commit-config.yaml"
    },
    {
        "name": "main.py",
        "path": "main.py",
        "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/main.py"
    }
]

def print_match_results(matches):
    if not matches:
        print("\nNo matching files found.")
        return

    print("\nMatching Files (sorted by relevance):")
    print("-" * 50)
    
    for match in matches:
        print(f"File Name: {match['file_name']}")
        print(f"Match Score: {match['match_score']} / 5")
        print(f"Download URL: {match['download_url']}")
        print("-" * 50)

async def main():
    try:
        # Initialize the matcher
        logger.info("Initializing IssueMatcher...")
        matcher = IssueMatcher()
        
        # Run the matching
        logger.info("Starting file matching process...")
        result = await matcher.match_files(issue_data, filtered_files)
        
        # Extract matches
        matches = result.get("filename_matches", [])
        
        # Print results
        print("\nMatching Results Summary:")
        print(f"Total files processed: {len(filtered_files)}")
        print(f"Matches found: {len(matches)}")
        
        # Print detailed results
        print_match_results(matches)
        
    except Exception as e:
        logger.error(f"An error occurred during execution: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
        logger.info("Process terminated by user interruption")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")