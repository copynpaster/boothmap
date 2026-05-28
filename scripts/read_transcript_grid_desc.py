import json

transcript_path = "/Users/uchun1ee/.gemini/antigravity/brain/9c55d14c-dd38-45b4-8ae3-ec1af5913b15/.system_generated/logs/transcript.jsonl"

with open(transcript_path, "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        content = data.get("content", "")
        source = data.get("source")
        step = data.get("step_index")
        
        # Search for user messages describing grid, cells, sizes, corridors, or layout structure
        if source == "USER_EXPLICIT" and any(keyword in content for keyword in ["그리드", "grid", "통로", "복도", "크기", "좌표", "셀"]):
            print(f"=== Step {step} ===")
            print(content.strip())
            print("=" * 60)
