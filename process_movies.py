cat > process_movies.py << 'EOF'
import ollama
import time
from tqdm import tqdm

print("🚀 شروع پردازش فیلم‌ها با Phi-3 mini\n")

model_name = "phi3:mini"
input_file = "movies.txt"
output_file = "output_movies.txt"

system_prompt = {
    "role": "system",
    "content": "تو یک دستیار مفید هستی. برای هر فیلم، داستان کامل و صحنه‌های مهم را در دقیقاً ۳ خط بنویس."
}

# خواندن لیست فیلم‌ها
with open(input_file, 'r', encoding='utf-8') as f:
    movies = [line.strip() for line in f.readlines() if line.strip()]

print(f"✅ {len(movies)} فیلم بارگذاری شد.\n")

with open(output_file, 'w', encoding='utf-8') as out:
    for i, movie in enumerate(tqdm(movies, desc="پردازش"), 1):
        try:
            prompt = f"فیلم: {movie}\nدرباره این فیلم توضیح کامل بده (داستان + صحنه‌های کلیدی) دقیقاً در ۳ خط بنویس."

            response = ollama.chat(
                model=model_name,
                messages=[system_prompt, {"role": "user", "content": prompt}]
            )

            result = response['message']['content'].strip()

            out.write(f"{i}. {movie}\n")
            out.write(result + "\n")
            out.write("="*100 + "\n\n")

            print(f"✅ {i}/{len(movies)} - {movie}")

            time.sleep(1)

        except Exception as e:
            out.write(f"{i}. {movie} → خطا: {str(e)}\n\n")
            print(f"❌ خطا در {movie}: {e}")

print(f"\n🎉 تمام شد! خروجی در {output_file} ذخیره شد.")
EOF
