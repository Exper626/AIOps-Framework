#import json 

# with open("juniper_copy.jsonl", "r") as f:
#     content = f.read()
#     pos = 2398
#     print(f"Character at position {pos}:\n{content[pos]}")
#     print("\nContext (100 chars before and after):")
#     print(content[max(0, pos - 100): pos + 100])


# import json

# with open("juniper.jsonl", "r") as infile:
#     data = json.load(infile)  # loads entire content as one JSON object

# filtered_data = [{"prompt": item["prompt"], "chosen": item["chosen"]} for item in data]

# with open("juniper_output.jsonl", "w") as outfile:
#     json.dump(filtered_data, outfile, indent=4)



# import re
import json

with open("cisco_copy.jsonl", "r") as f:
    content = json.loads(f.read())
    print(content)

print("\n Successful")


# Remove all opening and closing brackets
# content = content.replace('[', '').replace(']', '')

# Split by '}{' and rejoin with '},{'
# parts = content.split('}{')
# fixed = ['{' + p + '}' if i == 0 else '{' + p + '}' for i, p in enumerate(parts)]
# final = '[' + ','.join(fixed) + ']'

# Parse and save
# data = json.loads(final)
# with open("cisco_output.json", "w") as f:
#     json.dump(data, f, indent=2)



# import re
# import json

# with open("juniper_copy.jsonl", "r") as f:
#     content = f.read()

# # Attempt to fix missing quotes around property names
# # Caution: this is a simple regex and may not cover all edge cases
# content = re.sub(r'([{,])\s*([a-zA-Z0-9_]+)\s*:', r'\1 "\2":', content)

# # Fix JSON format (if two arrays stuck together)
# content = '[' + content.replace('][', ',') + ']'

# # Parse and save
# try:
#     data = json.loads(content)
#     with open("juniper_output.json", "w") as f:
#         json.dump(data, f, indent=2)
# except json.JSONDecodeError as e:
#     print(f"Still invalid JSON: {e}")

# with open("juniper_copy.jsonl", "r") as f:
#     content = f.read()

# # Remove leading/trailing square brackets if any
# content = content.strip().replace('\n', '').replace('\r', '')
# content = content.replace('][', '},{')  # close+open array back-to-back

# # Handle missing commas between objects: replace '}{' with '},{'
# content = re.sub(r'}\s*{', '},{', content)

# # Wrap in brackets to form a single valid JSON array
# content = f'[{content}]'

# # Try parsing
# try:
#     data = json.loads(content)
#     with open("juniper_output.json", "w") as f:
#         json.dump(data, f, indent=2)
#     print("Successfully cleaned and saved JSON.")
# except json.JSONDecodeError as e:
#     print("Still invalid JSON:", e)

