import os
import requests

base_url = "https://github.com/danielmiessler/Fabric/tree/main/data/patterns"

response = requests.get(base_url)
        
if response.status_code == 200:
    system_prompt = response.text
    print(system_prompt)

exit()
        
# Define agent folders
agent_folders = [
    'analyze_answers', 'analyze_code', 'analyze_data', 'analyze_paper',
    'create_adventure', 'create_keynote', 'create_website', 'create_workout',
    'diagram_flow', 'diagram_sitemap', 'teach_language', 'teach_math'
]

for folder in agent_folders:
    try:
        url = f"{base_url}{folder}/system.md"
        response = requests.get(url)
        
        if response.status_code == 200:
            system_prompt = response.text
            
            # Extract category from folder name (first word)
            category = folder.split('_')[0].capitalize()
            name = ' '.join(folder.split('_')[1:]).title() if '_' in folder else folder.title()



            
    except Exception as e:
        self.stdout.write(self.style.ERROR(f'Error loading {folder}: {str(e)}'))