---
name: dex-ruby-gem-engineering
description: Architect, package, test, and securely distribute Ruby Gems with Bundler dependency constraints, native C extension compilation, and automated publishing. Use when authoring shared Ruby libraries or maintaining gem ecosystems.
---

# dex-ruby-gem-engineering

## 1. Purpose & Scope
Thiết kế, đóng gói, kiểm thử và phân phối an toàn thư viện Ruby Gems; thiết lập ràng buộc phiên bản phụ thuộc chặt chẽ qua Bundler, quản lý quy trình biên dịch phần mở rộng mã C native (C extensions), và tự động hóa quy trình phát hành bảo đảm tính toàn vẹn chữ ký số.

## 2. When to Use
- Khi xây dựng thư viện dùng chung cho các ứng dụng Ruby on Rails hoặc microservices viết bằng Ruby.
- Khi cần đóng gói mã nguồn C/Rust hiệu năng cao thành một Gem nhị phân để tăng tốc độ xử lý trong Ruby.
- Khi cấu hình bảo mật quy trình phát hành Gem lên RubyGems.org với xác thực hai lớp (2FA) và chữ ký số.

## 3. When NOT to Use
- Khi chỉ phát triển ứng dụng web Rails hoàn chỉnh phục vụ người dùng cuối (không phải thư viện dùng chung).
- Khi viết các script shell nhỏ dùng nội bộ không cần đóng gói và quản lý phiên bản Gem.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Tệp đặc tả thư viện `.gemspec`, công cụ quản lý gói Bundler, trình biên dịch C (gcc/clang) nếu có native extension, tài khoản RubyGems.
- **Quyền hạn truy cập:** Quyền đóng gói file `.gem` và quyền phát hành lên kho lưu trữ.

## 5. Core Concepts & Taxonomy
- **Gemspec Specification:** Tệp khai báo metadata của Gem: tên, phiên bản, tác giả, giấy phép bản quyền, các tệp mã nguồn được đính kèm và danh sách dependencies.
- **Pessimistic Version Constraint (`~>`):** Toán tử khóa phiên bản an toàn trong Bundler (ví dụ: `~> 2.1` cho phép `>= 2.1` và `< 3.0`) ngăn ngừa breaking changes ngoài ý muốn.
- **Native C Extension (`extconf.rb`):** Script sinh ra `Makefile` để biên dịch mã nguồn C/C++ thành thư viện chia sẻ `.so`/`.bundle` khi Gem được cài đặt.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo cấu trúc thư mục Gem chuẩn hóa bằng Bundler (`bundle gem my_gem`).
2. Đặc tả chi tiết tệp `my_gem.gemspec`: khai báo giấy phép MIT/Apache-2.0, mô tả kỹ thuật và ràng buộc dependencies tối thiểu.
3. Nếu có native C extension: đặt mã nguồn trong thư mục `ext/my_gem/` và viết script cấu hình `extconf.rb` an toàn.
4. Viết bộ kiểm thử tự động toàn diện bằng RSpec hoặc Minitest kiểm thử cả logic Ruby và native code.
5. Cấu hình RuboCop để kiểm tra chuẩn định dạng mã nguồn và phân tích bảo mật tĩnh.
6. Đóng gói tệp nhị phân `my_gem-x.y.z.gem` và kiểm tra nội dung bên trong trước khi xuất bản bằng chữ ký số.

## 7. Concrete Examples
### Ví dụ tệp đặc tả chuẩn mực `my_gem.gemspec`:
```ruby
# frozen_string_literal: true

require_relative "lib/my_gem/version"

Gem::Specification.new do |spec|
  spec.name = "dex_core_security"
  spec.version = DexCoreSecurity::VERSION
  spec.authors = ["DEX Engineering Team"]
  spec.email = ["engineering@dex.dev"]

  spec.summary = "Enterprise security and cryptographic utilities for Ruby."
  spec.license = "MIT"
  spec.required_ruby_version = ">= 3.2.0"

  spec.files = Dir["lib/**/*.rb", "LICENSE.txt", "README.md"]
  spec.require_paths = ["lib"]

  # Ràng buộc dependencies chặt chẽ chống breaking changes
  spec.add_dependency "concurrent-ruby", "~> 1.2"
  spec.add_development_dependency "bundler", "~> 2.5"
  spec.add_development_dependency "rspec", "~> 3.12"
  spec.add_development_dependency "rubocop", "~> 1.60"
end
```

## 8. Anti-Patterns & Common Traps
- **Open-Ended Dependencies:** Khai báo dependency dạng `spec.add_dependency 'nokogiri'` không có ràng buộc phiên bản, khiến Gem bị sập khi thư viện bên ngoài phát hành bản cập nhật mới.
- **Leaking Test Files into Package:** Không cấu hình `spec.files` cẩn thận làm đóng gói toàn bộ thư mục `spec/` và tài nguyên kiểm thử nặng nề vào tệp Gem phát hành.
- **Unsandboxed Native Extensions:** Viết mã C extension bị tràn bộ nhớ đệm (Buffer Overflow) làm sập toàn bộ tiến trình Ruby VM (Segmentation Fault).

## 9. Quality Gates & Acceptance Criteria
- **QG-02**: Tệp `.gemspec` vượt qua lệnh kiểm tra tính hợp lệ `gem build` không có bất kỳ warning nào.
- **QG-04**: 100% các ca kiểm thử RSpec/Minitest chạy thành công trên các phiên bản Ruby mục tiêu (3.2, 3.3).
- **QG-06**: Chạy công cụ kiểm toán lỗ hổng bảo mật `bundle audit` trả về 0 lỗ hổng đã biết.

## 10. Security & Safety Boundaries
- Bắt buộc kích hoạt xác thực hai yếu tố (2FA) với WebAuthn/YubiKey trên tài khoản quản trị RubyGems.
- Ký số cho Gem bằng khóa mã hóa RSA công khai để người dùng có thể xác minh tính toàn vẹn nguồn gốc.

## 11. Platform Adapters
- **Package Managers**: RubyGems, Bundler.
- **Test Frameworks**: RSpec, Minitest, rake-compiler.

## 12. Deliverables & Output Artifacts
- Tệp đặc tả `*.gemspec` chuẩn mực.
- Gói cài đặt nhị phân `*.gem` hợp lệ.
- Bộ kiểm thử RSpec và cấu hình RuboCop tự động hóa.

## 13. Related & Complementary Skills
dex-dependency-vulnerability-intelligence, dex-open-source-license-scanning, dex-package-publishing-checks

## 14. Realistic Usage Example
```powershell
# Kiểm tra bảo mật và đóng gói Ruby Gem
bundle exec bundle audit check --update
bundle exec rake build
```
