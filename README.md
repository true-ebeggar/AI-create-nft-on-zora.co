# Zora Automation Script

This Python script automates the process of creating, deploying, minting, and collecting rewards for collections on Zora using third party browser-stash, specifically via an anti-detect browser (ADS) and MetaMask extension.

## 🚀 Workflow

### 1. **Pre-requisites:**
   - Set up profiles in ADS.
   - Obtain API keys for the [astica.ai](https://astica.ai/api-keys/) and [OpenAI](https://platform.openai.com/account/api-keys).
   - Install the [MM Extension version 10.23.2](https://github.com/MetaMask/metamask-extension/releases/tag/v10.23.2) to you ADS and name it 'MetaMask'.
   - Populate the Excel file with profile details, including seed phrases.
   - Have 0.001 ETH in Zora network for each seed.
   - Populate a prompt file with prompts for image generating.

### 2. **Profile Handling:**
   - Fetches profiles from an Excel file and processes them one by one.
   - Marks the profile as done after successful operation to avoid redundancy.

### 3. **MetaMask Interaction:**
   - Logs in or creates a MetaMask wallet using seed phrases.
   - Generates and saves a unique 32 symbols password for future use.
   - Adds Zora network to MetaMask if not already present.

### 4. **Zora Interaction:**
   - Logs in to the Zora page and creates a collection using a generated image and obtained description.
   - Deploys and mints the collection, then collects the reward.

### 5. **Image Generation and Description:**
   - Uses prompts from a user-provided file to create images via OpenAI API.
   - Sends the generated image to another API to get a detailed description.

### 6. **Indefinite Operation:**
   - Runs indefinitely, processing the profiles until all have been processed successfully.

## Installation & Setup
To get started, you will need to clone the repository to your local machine. Open a terminal and run the following command:
```
git clone https://github.com/Reilighost/AI-create-nft-on-zora.co
```
### Install Requirements: 
Navigate to the cloned repository's directory:
```
cd path/to/clone/repo
```
Run the following command to install the required packages:
```
pip install -r requirements.txt
```

Lastly configure settings by open the `config.py` file and add you API-keys, delay and MM identificator

