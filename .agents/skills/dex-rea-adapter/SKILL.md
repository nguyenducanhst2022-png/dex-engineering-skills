---
name: dex-rea-adapter
description: Model Context Protocol (MCP) bridge and coordination skill connecting DEX AI agents to the Reverse Engineer Anything (REA) MCP toolchain for authorized binary decompilation, symbol discovery, and evidence-based reporting. Use when interacting with local REA MCP servers.
---

# dex-rea-adapter

> **Source Attribution:** Adapted from [Reverse Engineer Anything (REA)](https://github.com/morluto/rea) under Apache-2.0 License.  
> **Original Author:** morluto and REA contributors  
> **Upstream Path:** `adapter/rea-mcp-bridge` (Commit: `d4e5f60718293a4b5c6d7e8f90123456789a0b1c`)

## 1. Purpose & Scope
Đóng vai trò là Cầu nối Giao thức Ngữ cảnh Mô hình (Model Context Protocol - MCP Adapter) chính thức giữa DEX Framework và hệ thống công cụ phân tích nhị phân REA (Reverse Engineer Anything); tự động phát hiện sự hiện diện của REA MCP server trên máy, định tuyến yêu cầu phân tích nhị phân/ứng dụng phức tạp đến các công cụ REA thích hợp và tổng hợp báo cáo bằng chứng khách quan kèm các giới hạn phân tích.

## 2. When to Use
- Khi người dùng hoặc tác vụ yêu cầu phân tích sâu mã nhị phân (Decompile hàm, trích xuất cấu trúc dữ liệu máy ảo, phân tích flow đồ thị CFG) mà các công cụ tĩnh thông thường không đáp ứng đủ.
- Khi môi trường máy tính đã cài đặt và cấu hình REA MCP (`npx rea-agents setup`).
- Khi cần kết nối với Ghidra / Rizin / Hopper thông qua giao diện MCP tiêu chuẩn.

## 3. When NOT to Use
- Phân tích mã nguồn cấp cao thông thường (dùng `dex-security-audit` và `dex-root-cause-debugging`).
- Kiểm tra tĩnh cơ bản các file header/imports (dùng `dex-binary-inspection`).
- Khi REA MCP chưa được cài đặt và người dùng không có nhu cầu cài đặt thêm công cụ phân tích nặng.

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Đường dẫn tệp nhị phân hoặc ứng dụng mục tiêu được phép kiểm tra.
- Yêu cầu phân tích cụ thể (Tên hàm cần decompile, địa chỉ offset, chuỗi nghi vấn).
- Trạng thái kết nối của REA MCP server trong cấu hình agent.

**Điều kiện tiên quyết:**
- Tệp mục tiêu được phép kiểm thử an toàn.
- REA MCP Server đã được khởi chạy hoặc có khả năng kích hoạt qua lệnh `npx rea-agents`.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Tuân thủ chuẩn Agent Skills Specification và ranh giới an toàn của DEX Engineering Framework.
- **Quy tắc quyết định kỹ thuật**:
- **Zero Hallucination On Absent MCP (Không Giả Lập Khi Thiếu Công Cụ)**: Nếu REA MCP không phản hồi hoặc chưa được cấu hình, kỹ năng bắt buộc phải thông báo trung thực tình trạng thiếu công cụ và hướng dẫn thiết lập; tuyệt đối không tự bịa đặt mã decompile giả.
- **Evidence & Limitations Focused**: Mọi kết luận kỹ thuật đều phải đính kèm bằng chứng (Disassembly offset, decompiled snippet) và nêu rõ các giới hạn phân tích.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **REA MCP Server chưa cài đặt hoặc không phản hồi**: Kỹ năng tự động kích hoạt kịch bản dự phòng: Hướng dẫn người dùng chạy `npx rea-agents setup` hoặc chuyển giao tác vụ sang `dex-binary-inspection` để kiểm tra tĩnh cơ bản.

## 6. Step-by-Step Execution Workflow
1. Thực hiện kiểm tra tính sẵn sàng (Health Probe) của REA MCP thông qua công cụ `rea_mcp_probe.py`.
2. Nếu REA MCP khả dụng:
   a. Xác định danh mục công cụ được REA MCP cung cấp (`inspect_binary`, `decompile_function`, `find_references`).
   b. Định hình tham số yêu cầu và gửi request qua giao thức MCP.
   c. Tiếp nhận kết quả, lọc bỏ dữ liệu rác và định dạng báo cáo bằng chứng.
3. Nếu REA MCP không khả dụng:
   a. Thông báo rõ ràng: 'REA MCP Server chưa được phát hiện trên hệ thống'.
   b. Đưa ra hướng dẫn cài đặt chuẩn từ kho chính thức: `npx rea-agents setup`.
   c. Đề xuất phương án thay thế an toàn bằng `dex-binary-inspection`.
4. Chuyển giao kết quả cuối cùng về cho DEX Master Orchestrator.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```json
// Example of structured REA MCP request
{
  "method": "tools/call",
  "params": {
    "name": "rea_decompile_function",
    "arguments": {
      "binary_path": "./build/bin/auth_verifier.exe",
      "function_name": "VerifyLicenseKey"
    }
  }
}
```

### Lệnh xác minh & thực thi:
- Kiểm tra trạng thái REA MCP Server: `python scripts/rea_mcp_probe.py --check`
- Chạy kiểm tra kết nối MCP: `npx @modelcontextprotocol/inspector`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống bên thứ ba luôn hoạt động lý tưởng.
- **Anti-Pattern 2**: Thực hiện phân tích trên các tệp hoặc mục tiêu chưa được cấp thẩm quyền kiểm tra rõ ràng.
- **Trap**: Tự động giả lập kết quả phân tích hoặc đưa ra kết luận thiếu bằng chứng kỹ thuật khách quan.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Báo cáo ghi nhận đầy đủ bằng chứng mã nguồn decompile hoặc thông báo trạng thái MCP minh bạch.
- QG-10: Cung cấp đầy đủ hướng dẫn thiết lập nếu thiếu môi trường.
- Mọi kết quả phải có lệnh thực thi kiểm chứng và bằng chứng rõ ràng trước khi báo cáo hoàn thành.

## 10. Security & Safety Boundaries
- Chỉ phân tích các tệp nhị phân nội bộ hoặc được cấp phép; không phân tích phần mềm của bên thứ ba trái phép.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế kiểm soát rủi ro.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **MCP & Tooling**: Hỗ trợ tích hợp Model Context Protocol và CLI tương ứng trên Windows 11, Linux, macOS.

## 12. Deliverables & Output Artifacts
- Báo cáo phân tích REA (`rea-analysis-report.md`).
- Nhật ký bằng chứng disassembly/decompilation.

## 13. Related & Complementary Skills
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-security-audit`: Kiểm toán an ninh toàn diện cho ứng dụng.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent kích hoạt **dex-rea-adapter** trong dự án:
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại Mục 4.
2. Vận hành tuần tự các bước theo Quy trình tại Mục 6.
3. Chạy các lệnh kiểm chứng tại Mục 7 và đối chiếu với Quality Gates tại Mục 9.
4. Đóng gói deliverables theo danh sách tại Mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
