---
name: dex-windows-native-ui-accessibility
description: Implement, test, and audit Windows UI Automation (UIA) and accessibility interfaces. Support screen readers (Narrator, NVDA), keyboard navigation, focus indicators, and High Contrast mode.
---

# dex-windows-native-ui-accessibility

## 1. Purpose & Scope
Thiết kế, tích hợp và kiểm chứng tiêu chuẩn tiếp cận người khuyết tật trên ứng dụng desktop Windows (Windows Accessibility & UI Automation - UIA); cài đặt các nhà cung cấp giao diện UIA (`IRawElementProviderSimple`, `IInvokeProvider`, `IValueProvider`); bảo đảm khả năng hỗ trợ hoàn hảo cho các trình đọc màn hình phổ biến (Windows Narrator, NVDA, JAWS), điều hướng bàn phím toàn diện (Tab Order, Focus Indicators) và khả năng thích ứng với giao diện tương phản cao (Windows High Contrast Themes).

## 2. When to Use
- Khi phát triển các thành phần điều khiển giao diện người dùng tùy biến (Custom UI Controls) trong Win32 hoặc C++ cần hỗ trợ người khiếm thị.
- Khi đáp ứng các tiêu chuẩn pháp lý về khả năng tiếp cận phần mềm của doanh nghiệp hoặc chính phủ (Section 508, WCAG 2.1 AA, EN 301 549).
- Khi tự động hóa kiểm thử giao diện desktop thông qua cây phần tử Windows UI Automation Tree.

## 3. When NOT to Use
- Khi sử dụng các thành phần điều khiển chuẩn của hệ thống (Standard Windows Buttons/Edits) đã được OS tích hợp sẵn UIA mặc định.
- Khi xây dựng ứng dụng dịch vụ chạy ngầm không có thành phần hiển thị giao diện.

## 4. Prerequisites & Input Context
- **Công cụ kiểm tra:** Windows SDK Accessibility Insights for Windows, Inspect.exe, hoặc AccScope.
- **Trình đọc màn hình:** Windows Narrator (phím tắt Win + Ctrl + Enter) hoặc NVDA.

## 5. Core Concepts & Taxonomy
- **UI Automation Tree:** Cấu trúc phân cấp hình cây phản ánh giao diện ứng dụng cho các công nghệ trợ năng, bao gồm các phần tử cha, con và anh em.
- **Control Patterns:** Các giao diện xác định hành vi của phần tử: ví dụ `IInvokeProvider` cho nút bấm, `IToggleProvider` cho checkbox, `IRangeValueProvider` cho slider.
- **Automation Events:** Các thông báo phát ra khi trạng thái giao diện thay đổi (ví dụ `UiaRaiseAutomationEvent` khi nút được click hoặc giá trị text thay đổi).

## 6. Step-by-Step Execution Workflow
1. Khảo sát các thành phần giao diện tùy biến (Custom Controls) chưa có nhà cung cấp trợ năng.
2. Cài đặt giao diện `IRawElementProviderSimple` cho cửa sổ tùy biến trong hàm xử lý thông điệp `WM_GETOBJECT`.
3. Cung cấp các thuộc tính UIA cơ bản: `UIA_NamePropertyId`, `UIA_ControlTypePropertyId`, `UIA_LocalizedControlTypePropertyId`.
4. Cài đặt các Control Patterns phù hợp với hành vi nghiệp vụ của phần tử.
5. Bật Windows Narrator hoặc công cụ Inspect.exe để quét kiểm tra cây UI Automation.
6. Xác nhận việc nhận diện chính xác tên nút, trạng thái kích hoạt và điều hướng phím Tab.

## 7. Concrete Examples
### Cai dat nha cung cap UIA co ban cho Custom Control trong Win32:
```cpp
#include <windows.h>
#include <uiautomation.h>
#include <iostream>

class CustomButtonProvider : public IRawElementProviderSimple, public IInvokeProvider {
private:
    LONG m_refCount = 1;
    HWND m_hwnd;

public:
    CustomButtonProvider(HWND hwnd) : m_hwnd(hwnd) {}

    // IUnknown
    ULONG STDMETHODCALLTYPE AddRef() override { return InterlockedIncrement(&m_refCount); }
    ULONG STDMETHODCALLTYPE Release() override {
        LONG val = InterlockedDecrement(&m_refCount);
        if (val == 0) delete this;
        return val;
    }
    HRESULT STDMETHODCALLTYPE QueryInterface(REFIID riid, void** ppv) override {
        if (riid == IID_IUnknown || riid == IID_IRawElementProviderSimple) {
            *ppv = static_cast<IRawElementProviderSimple*>(this);
        } else if (riid == IID_IInvokeProvider) {
            *ppv = static_cast<IInvokeProvider*>(this);
        } else {
            *ppv = nullptr;
            return E_NOINTERFACE;
        }
        AddRef();
        return S_OK;
    }

    // IRawElementProviderSimple
    HRESULT STDMETHODCALLTYPE get_ProviderOptions(ProviderOptions* pRetVal) override {
        *pRetVal = ProviderOptions_ServerSideProvider;
        return S_OK;
    }
    HRESULT STDMETHODCALLTYPE GetPatternProvider(PATTERNID patternId, IUnknown** pRetVal) override {
        if (patternId == UIA_InvokePatternId) {
            *pRetVal = static_cast<IInvokeProvider*>(this);
            AddRef();
            return S_OK;
        }
        *pRetVal = nullptr;
        return S_OK;
    }
    HRESULT STDMETHODCALLTYPE GetPropertyValue(PROPERTYID propertyId, VARIANT* pRetVal) override {
        if (propertyId == UIA_ControlTypePropertyId) {
            pRetVal->vt = VT_I4;
            pRetVal->lVal = UIA_ButtonControlTypeId;
        } else if (propertyId == UIA_NamePropertyId) {
            pRetVal->vt = VT_BSTR;
            pRetVal->bstrVal = SysAllocString(L"Submit Order");
        } else {
            pRetVal->vt = VT_EMPTY;
        }
        return S_OK;
    }
    HRESULT STDMETHODCALLTYPE get_HostRawElementProvider(IRawElementProviderSimple** pRetVal) override {
        return UiaHostProviderFromHwnd(m_hwnd, pRetVal);
    }

    // IInvokeProvider
    HRESULT STDMETHODCALLTYPE Invoke() override {
        SendMessage(m_hwnd, BM_CLICK, 0, 0);
        return S_OK;
    }
};
```

## 8. Anti-Patterns & Common Traps
- **Missing WM_GETOBJECT Handler:** Tự vẽ nút bấm đồ họa phức tạp nhưng không bắt thông điệp `WM_GETOBJECT` khiến trình đọc màn hình coi cửa sổ là một vùng đen hoàn toàn.
- **Unlabeled Graphic Buttons:** Nút bấm chỉ hiển thị icon mà không cung cấp chuỗi `UIA_NamePropertyId`, khiến Narrator chỉ đọc "Button" không rõ chức năng.
- **Trapping Keyboard Focus:** Thiết kế danh sách phần tử khiến người dùng nhấn phím Tab bị kẹt lại vĩnh viễn không thể chuyển tới phần tử tiếp theo.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% các phần tử tương tác tùy biến đều hiển thị đầy đủ tên, vai trò và trạng thái trong công cụ Inspect.exe.
- **QG-02**: Trình đọc màn hình Windows Narrator đọc chính xác nội dung và hướng dẫn khi con trỏ bàn phím di chuyển tới.
- **QG-03**: Toàn bộ luồng nghiệp vụ của ứng dụng có thể hoàn thành 100% chỉ bằng bàn phím mà không cần chạm vào chuột.

## 10. Security & Safety Boundaries
- Đảm bảo các hàm cung cấp chuỗi UIA không làm lộ các thông tin nhạy cảm (như mật khẩu trong trường Password).

## 11. Platform Adapters
- **Runtimes**: Windows UI Automation API, Accessibility Insights, Windows Narrator, NVDA screen reader.

## 12. Deliverables & Output Artifacts
- Lớp nhà cung cấp trợ năng Windows UIA (`uia_custom_provider.cpp`).
- Báo cáo kiểm định khả năng tiếp cận phần mềm (`accessibility_inspection.json`).

## 13. Related & Complementary Skills
dex-windows-input-api-integration, dex-win32-dpi-multi-monitor-layout, dex-windows-com-interop

## 14. Realistic Usage Example
```powershell
# Kiem tra cay UIA cua ung dung bang Accessibility Insights CLI hoac PowerShell
Add-Type -AssemblyName UIAutomationClient
$root = [System.Windows.Automation.AutomationElement]::RootElement
Write-Host "Root Name: " $root.Current.Name
```
