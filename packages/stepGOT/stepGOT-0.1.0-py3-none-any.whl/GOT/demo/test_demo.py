from transformers import AutoModel, AutoTokenizer
from GOT.model.GOT_ocr_2_0 import GOTQwenForCausalLM
tokenizer = AutoTokenizer.from_pretrained('ucaslcl/GOT-OCR2_0', trust_remote_code=True)
model = AutoModel.from_pretrained('ucaslcl/GOT-OCR2_0', trust_remote_code=True, low_cpu_mem_usage=True, device_map='cpu', use_safetensors=True, pad_token_id=tokenizer.eos_token_id)
# tokenizer = AutoTokenizer.from_pretrained('/data/model/models--vikp--GOT', trust_remote_code=True)
# model = GOTQwenForCausalLM.from_pretrained('/data/model/models--vikp--GOT', low_cpu_mem_usage=True, device_map='cpu', use_safetensors=True, pad_token_id=151643)
# model = model.eval().cuda()
model = model.eval()


# input your test image
image_file = '/data/tmp_data/0923/table_datas/0006.png'

# plain texts OCR
# res = model.chat(tokenizer, image_file, ocr_type='ocr')

# format texts OCR:
res = model.chat(tokenizer, image_file, ocr_type='format')

# fine-grained OCR:
# res = model.chat(tokenizer, image_file, ocr_type='ocr', ocr_box='')
# res = model.chat(tokenizer, image_file, ocr_type='format', ocr_box='')
# res = model.chat(tokenizer, image_file, ocr_type='ocr', ocr_color='')
# res = model.chat(tokenizer, image_file, ocr_type='format', ocr_color='')

# multi-crop OCR:
# res = model.chat_crop(tokenizer, image_file, ocr_type='ocr')
# res = model.chat_crop(tokenizer, image_file, ocr_type='format')

# render the formatted OCR results:
# res = model.chat(tokenizer, image_file, ocr_type='format', render=True, save_render_file = './demo.html')

print(res)
# 