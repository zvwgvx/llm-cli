# PolyCLI

Phần mềm chat CLI chất lượng cao để tương tác với các mô hình AI qua Ollama API.

**Đặc biệt: Không cần cài thêm thư viện nào! Chỉ dùng thư viện built-in của Python.**

## Tính năng

- ✅ Không cần cài đặt dependencies (chỉ dùng thư viện built-in Python)
- ✅ Giao diện CLI đẹp với màu sắc nhẹ nhàng (kiểu Claude/Gemini)
- ✅ Hỗ trợ streaming response real-time mượt mà
- ✅ Lưu lịch sử hội thoại
- ✅ Cấu hình linh hoạt qua file JSON
- ✅ Hỗ trợ reasoning_effort cho các model đặc biệt
- ✅ Các lệnh đặc biệt để quản lý chat
- ✅ Xử lý lỗi và timeout hoàn chỉnh

## Yêu cầu

- Python 3.7+ (không cần cài thêm gì!)
- Ollama đã được cài đặt và đang chạy

## Cài đặt

Không cần cài đặt gì cả! Chỉ cần chạy trực tiếp:

```bash
python main.py
```

hoặc:

```bash
python3 main.py
```

## Cấu hình

Chỉnh sửa file `config.json` để tùy chỉnh:

```json
{
  "api_url": "http://localhost:11434",
  "model": "gpt-oss:120b-cloud",
  "temperature": 0.7,
  "max_tokens": 128000,
  "system_prompt": "Bạn là 1 trợ lí hữu ích",
  "stream": true,
  "timeout": 120,
  "reasoning_effort": "medium"
}
```

### Các tham số cấu hình:

- `api_url`: URL của Ollama API (mặc định: http://localhost:11434)
- `model`: Tên model muốn sử dụng (ví dụ: llama2, mistral, codellama, qwen, gpt-oss:120b-cloud, v.v.)
- `temperature`: Độ sáng tạo của AI (0.0 - 1.0)
- `max_tokens`: Số token tối đa cho mỗi response
- `system_prompt`: System prompt cho AI
- `stream`: Bật/tắt streaming response (true/false)
- `timeout`: Thời gian timeout cho API request (giây)
- `reasoning_effort`: Mức độ suy luận của model (low/medium/high) - tùy chọn, dùng cho các model hỗ trợ reasoning như gpt-oss

## Sử dụng

Chạy chương trình:

```bash
python main.py
```

Hoặc làm cho file có thể thực thi (trên Linux/Mac):

```bash
chmod +x main.py
./main.py
```

## Lệnh đặc biệt

Trong khi chat, bạn có thể sử dụng các lệnh sau:

- `/clear` - Xóa lịch sử hội thoại
- `/history` - Hiển thị lịch sử hội thoại
- `/config` - Hiển thị cấu hình hiện tại
- `/exit` hoặc `/quit` - Thoát chương trình
- `Ctrl+C` - Thoát chương trình

## Ví dụ sử dụng

```
┌──────────────────────── PolyCLI ─────────────────────────┐
│ PolyCLI - Chat với AI models qua Ollama                 │
│                                                          │
│ Model: gpt-oss:120b-cloud                               │
│ API: http://0.0.0.0:11434                               │
│                                                          │
│ Gõ tin nhắn để chat. Lệnh đặc biệt:                    │
│   /clear   - Xóa lịch sử hội thoại                      │
│   /history - Xem lịch sử hội thoại                      │
│   /config  - Xem cấu hình                               │
│   /exit    - Thoát chương trình                         │
│   Ctrl+C   - Thoát chương trình                         │
└──────────────────────────────────────────────────────────┘

You: Xin chào!