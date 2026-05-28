import json

transcript_path = "/Users/uchun1ee/.gemini/antigravity/brain/9c55d14c-dd38-45b4-8ae3-ec1af5913b15/.system_generated/logs/transcript.jsonl"

print("Reading conversation history...")
user_messages = []
model_messages = []

with open(transcript_path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            data = json.loads(line)
            source = data.get("source")
            content = data.get("content", "")
            
            if not content:
                continue
                
            if source == "USER_EXPLICIT":
                user_messages.append(content)
            elif source == "MODEL":
                model_messages.append(content)
        except Exception as e:
            pass

print(f"Loaded {len(user_messages)} user messages and {len(model_messages)} model messages.")

print("\n--- Recent User Requests ---")
for idx, msg in enumerate(user_messages[-10:]):
    print(f"User {idx+1}: {msg.strip()}")

print("\n--- Searches in history for 'grid' or '그리드' or '크기' ---")
with open(transcript_path, "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        content = data.get("content", "")
        if "그리드" in content or "grid" in content or "크기" in content or "통로" in content:
            source = data.get("source")
            step = data.get("step_index")
            print(f"Step {step} ({source}): {content[:300].strip()}...")
            print("-" * 50)
