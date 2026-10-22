---
name: dex-tool-calling-contracts
description: Define and validate JSON Schema tool-calling contracts for LLMs, handle multi-tool orchestration, validate parameter schemas, and safely parse tool execution results. Use when equipping AI agents with function calling, database tools, or API execution capabilities.
---

# dex-tool-calling-contracts

## 1. Purpose & Scope
Thiết kế, chuẩn hóa và kiểm soát an toàn các hợp đồng gọi công cụ (Tool / Function Calling Contracts) cho AI Agent; định nghĩa tham số bằng JSON Schema chặt chẽ, xử lý điều phối gọi nhiều công cụ đồng thời hoặc tuần tự (Multi-tool Execution), xác thực kiểu dữ liệu đầu vào trước khi thực thi và định dạng kết quả trả về an toàn cho ngữ cảnh của LLM.

## 2. When to Use
- Khi xây dựng AI Agent có khả năng tự động thực hiện hành động: Truy vấn cơ sở dữ liệu, gửi email, gọi API bên thứ ba, chạy lệnh shell.
- Khi LLM tự ý bịa đặt tham số (Hallucinated parameters) không có trong định nghĩa công cụ gây lỗi crash mã nguồn.
- Khi cần giới hạn và kiểm soát chặt chẽ các tham số mà AI được phép truyền vào các hàm nhạy cảm.

## 3. When NOT to Use
- Xây dựng chatbot trò chuyện thuần túy không có nhu cầu tương tác với hệ thống bên ngoài.
- Viết các API endpoint nội bộ thông thường do lập trình viên gọi trực tiếp.

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Danh sách các công cụ cần cấp cho Agent (Tool Name, Description, Handler Function).
- Định nghĩa tham số bằng JSON Schema hoặc Zod Schema.
- Quyền hạn và giới hạn an toàn của từng công cụ.

**Điều kiện tiên quyết:**
- Mô hình LLM mục tiêu có hỗ trợ tính năng Native Tool Calling (OpenAI Function Calling, Anthropic Tools).
- Handler function của từng công cụ đã được viết sẵn và có unit test kiểm chứng độc lập.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Tên Và Mô Tả Là Yếu Tố Quyết Định**: LLM chọn công cụ dựa hoàn toàn vào Tên và Mô tả; mô tả mơ hồ sẽ dẫn đến việc LLM gọi sai công cụ hoặc không biết khi nào cần gọi.
- **Validate Trước Khi Chạy Handler**: Tuyệt đối không bao giờ tin tưởng mù quáng các tham số do LLM sinh ra; luôn kiểm tra qua schema validator trước khi truyền vào database query hay HTTP request.
- **Kết Quả Trả Về Phải Ngắn Gọn**: Kết quả trả về cho LLM chỉ nên chứa thông tin cần thiết; không nhét toàn bộ mớ JSON thô 5MB vào context làm tràn cửa sổ ngữ cảnh.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **LLM truyền tham số sai kiểu dữ liệu (truyền chuỗi thay vì số)**: Do schema không ghi rõ kiểu -> Khắc phục: Schema validator từ chối và tự động gửi phản hồi lỗi cấu trúc để LLM tự sửa lại tham số.
- **Agent gọi đi gọi lại 1 công cụ trong vòng lặp vô tận**: Do kết quả trả về không giúp Agent giải quyết được bài toán -> Khắc phục: Bộ đếm số lần gọi (Step Counter) đạt ngưỡng tối đa 5 lần sẽ tự động ngắt và yêu cầu hỗ trợ từ con người.

## 6. Step-by-Step Execution Workflow
1. Khai báo danh mục công cụ với tên gọi rõ ràng, mang tính động từ (ví dụ: `search_customer_by_phone`, `create_support_ticket`).
2. Viết phần mô tả (Tool Description) cực kỳ chi tiết, giải thích rõ CÔNG CỤ LÀM GÌ và KHI NÀO NÊN GỌI.
3. Định nghĩa schema tham số bằng Zod hoặc JSON Schema: Ghi rõ kiểu dữ liệu, các trường bắt buộc (`required`), giá trị mẫu và mô tả cho từng tham số.
4. Khi LLM quyết định gọi công cụ (Tool Call): BẮT BUỘC phải validate tham số nhận được qua Zod Schema trước khi đưa vào hàm thực thi thật.
5. Xử lý lỗi an toàn: Nếu hàm thực thi bị lỗi ngoại lệ (ví dụ: không tìm thấy khách hàng), đóng gói lỗi thành một thông điệp thân thiện và trả ngược lại cho LLM để LLM tự hiểu và thử phương án khác thay vì làm crash hệ thống.
6. Kiểm soát vòng lặp thực thi: Giới hạn tối đa số bước gọi công cụ liên tiếp (ví dụ: tối đa 5 bước) để tránh Agent rơi vào vòng lặp vô tận.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```typescript
// src/ai/tools/weatherTool.ts
import { z } from 'zod';

export const GetWeatherTool = {
  name: 'get_current_weather',
  description: 'Lấy thông tin thời tiết hiện tại cho một thành phố cụ thể.',
  parameters: z.object({
    city: z.string().describe('Tên thành phố, ví dụ: Hanoi, Ho Chi Minh City'),
    unit: z.enum(['celsius', 'fahrenheit']).default('celsius').describe('Đơn vị nhiệt độ')
  }),
  execute: async ({ city, unit }: { city: string; unit: string }) => {
    const data = await weatherApi.fetch(city, unit);
    return { temperature: data.temp, condition: data.desc };
  }
};
```

### Lệnh xác minh & thực thi:
- Chạy unit test kiểm tra validate schema của công cụ: `npm test -- tests/ai/toolValidation.spec.ts`
- Chạy kịch bản giả lập Agent gọi công cụ: `npm run test:agent-tools`
- Kiểm tra JSON Schema sinh ra từ Zod: `node -e 'console.log(zodToJsonSchema(myToolSchema))'`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các công cụ đều có phần mô tả rõ ràng và tham số được định nghĩa bằng Schema chặt chẽ.
- QG-05: Kịch bản kiểm thử tham số không hợp lệ được hệ thống xử lý an toàn mà không làm sập ứng dụng.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Cấm cấp các công cụ có khả năng thực thi lệnh tùy ý (như `eval()` hoặc raw SQL execution không ràng buộc) cho Agent.
- Các thao tác có tính chất phá hủy hoặc thay đổi tiền tệ bắt buộc phải có bước xác nhận phê duyệt từ con người (Human-in-the-loop Approval).
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- File định nghĩa danh mục công cụ (`src/ai/tools/customerTools.ts`).
- Bộ điều phối thực thi công cụ an toàn (`src/ai/toolDispatcher.ts`).
- File unit test kiểm chứng quá trình gọi và validate công cụ.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-tool-calling-contracts**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
