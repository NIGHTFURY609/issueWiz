# test_run.py
from model.matcher import IssueMatcher
import asyncio
import json

# Sample test data
"""issue_data = {
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
    },
    {
      "name": "evaluation.json",
      "path": "samples/answer-key/using-csv/evaluation.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/answer-key/using-csv/evaluation.json"
    },
    {
      "name": "template.json",
      "path": "samples/answer-key/using-csv/template.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/answer-key/using-csv/template.json"
    },
    {
      "name": "evaluation.json",
      "path": "samples/answer-key/weighted-answers/evaluation.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/answer-key/weighted-answers/evaluation.json"
    },
    {
      "name": "template.json",
      "path": "samples/answer-key/weighted-answers/template.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/answer-key/weighted-answers/template.json"
    },
    {
      "name": "template.json",
      "path": "samples/community/Antibodyy/template.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/community/Antibodyy/template.json"
    },
    {
      "name": "template.json",
      "path": "samples/community/Sandeep-1507/template.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/community/Sandeep-1507/template.json"
    },
    {
      "name": "template.json",
      "path": "samples/community/Shamanth/template.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/community/Shamanth/template.json"
    },
    {
      "name": "config.json",
      "path": "samples/community/UPSC-mock/config.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/community/UPSC-mock/config.json"
    },
    {
      "name": "evaluation.json",
      "path": "samples/community/UPSC-mock/evaluation.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/community/UPSC-mock/evaluation.json"
    },
    {
      "name": "template.json",
      "path": "samples/community/UPSC-mock/template.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/community/UPSC-mock/template.json"
    },
    {
      "name": "config.json",
      "path": "samples/community/UmarFarootAPS/config.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/community/UmarFarootAPS/config.json"
    },
    {
      "name": "evaluation.json",
      "path": "samples/community/UmarFarootAPS/evaluation.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/community/UmarFarootAPS/evaluation.json"
    },
    {
      "name": "template.json",
      "path": "samples/community/UmarFarootAPS/template.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/community/UmarFarootAPS/template.json"
    },
    {
      "name": "template.json",
      "path": "samples/community/dxuian/template.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/community/dxuian/template.json"
    },
    {
      "name": "template.json",
      "path": "samples/community/ibrahimkilic/template.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/community/ibrahimkilic/template.json"
    },
    {
      "name": "template.json",
      "path": "samples/community/samuelIkoli/template.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/community/samuelIkoli/template.json"
    },
    {
      "name": "config.json",
      "path": "samples/sample1/config.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/sample1/config.json"
    },
    {
      "name": "template.json",
      "path": "samples/sample1/template.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/sample1/template.json"
    },
    {
      "name": "config.json",
      "path": "samples/sample2/config.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/sample2/config.json"
    },
    {
      "name": "template.json",
      "path": "samples/sample2/template.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/sample2/template.json"
    },
    {
      "name": "template.json",
      "path": "samples/sample3/colored-thick-sheet/template.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/sample3/colored-thick-sheet/template.json"
    },
    {
      "name": "config.json",
      "path": "samples/sample3/config.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/sample3/config.json"
    },
    {
      "name": "template.json",
      "path": "samples/sample3/xeroxed-thin-sheet/template.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/sample3/xeroxed-thin-sheet/template.json"
    },
    {
      "name": "config.json",
      "path": "samples/sample4/config.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/sample4/config.json"
    },
    {
      "name": "evaluation.json",
      "path": "samples/sample4/evaluation.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/sample4/evaluation.json"
    },
    {
      "name": "template.json",
      "path": "samples/sample4/template.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/sample4/template.json"
    },
    {
      "name": "config.json",
      "path": "samples/sample5/config.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/sample5/config.json"
    },
    {
      "name": "evaluation.json",
      "path": "samples/sample5/evaluation.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/sample5/evaluation.json"
    },
    {
      "name": "template.json",
      "path": "samples/sample5/template.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/sample5/template.json"
    },
    {
      "name": "config.json",
      "path": "samples/sample6/config.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/sample6/config.json"
    },
    {
      "name": "template.json",
      "path": "samples/sample6/template.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/sample6/template.json"
    },
    {
      "name": "template_fb_align.json",
      "path": "samples/sample6/template_fb_align.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/sample6/template_fb_align.json"
    },
    {
      "name": "template_no_fb_align.json",
      "path": "samples/sample6/template_no_fb_align.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/sample6/template_no_fb_align.json"
    }
  ]"""

sampleinput={
  "owner": "Udayraj123",
  "repo": "OMRChecker",
  "filteredFiles": [
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
    },
    {
      "name": "evaluation.json",
      "path": "samples/answer-key/using-csv/evaluation.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/answer-key/using-csv/evaluation.json"
    },
    {
      "name": "template.json",
      "path": "samples/answer-key/using-csv/template.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/answer-key/using-csv/template.json"
    },
    {
      "name": "evaluation.json",
      "path": "samples/answer-key/weighted-answers/evaluation.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/answer-key/weighted-answers/evaluation.json"
    },
    {
      "name": "template.json",
      "path": "samples/answer-key/weighted-answers/template.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/answer-key/weighted-answers/template.json"
    },
    {
      "name": "template.json",
      "path": "samples/community/Antibodyy/template.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/community/Antibodyy/template.json"
    },
    {
      "name": "template.json",
      "path": "samples/community/Sandeep-1507/template.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/community/Sandeep-1507/template.json"
    },
    {
      "name": "template.json",
      "path": "samples/community/Shamanth/template.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/community/Shamanth/template.json"
    },
    {
      "name": "config.json",
      "path": "samples/community/UPSC-mock/config.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/community/UPSC-mock/config.json"
    },
    {
      "name": "evaluation.json",
      "path": "samples/community/UPSC-mock/evaluation.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/community/UPSC-mock/evaluation.json"
    },
    {
      "name": "template.json",
      "path": "samples/community/UPSC-mock/template.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/community/UPSC-mock/template.json"
    },
    {
      "name": "config.json",
      "path": "samples/community/UmarFarootAPS/config.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/community/UmarFarootAPS/config.json"
    },
    {
      "name": "evaluation.json",
      "path": "samples/community/UmarFarootAPS/evaluation.json",
      "download_url": "https://raw.githubusercontent.com/Udayraj123/OMRChecker/master/samples/community/UmarFarootAPS/evaluation.json"
    }
  ],
  "issueDetails": {
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
}
issue_data=sampleinput['issueDetails']
filtered_files=sampleinput['filteredFiles']
async def main():
    # Initialize the matcher
    matcher = IssueMatcher()
    
    # Run the matching
    result = await matcher.match_files(issue_data, filtered_files)
   
    print(json.dumps(result,indent=4))
    # Print results
    """ print("\nMatching Results:")
    print("-----------------")
    print(f"Status: {result['status']}")
    if result['status'] == 'success':
        print("\nMatched Files:")
        for match in result['matches']:
            print(f"File: {match['file']}")
            print(f"Similarity Score: {match['similarity_score']}")
            print("---")"""

# Run the async function

if __name__ == "__main__":
    asyncio.run(main())