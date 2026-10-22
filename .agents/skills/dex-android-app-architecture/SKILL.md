---
name: dex-android-app-architecture
description: Architect scalable, robust Android applications using MVVM/MVI, Jetpack Compose, Kotlin Coroutines & StateFlow, Room database, and Hilt dependency injection. Use when building or refactoring modern Android applications.
---

# dex-android-app-architecture

## 1. Purpose & Scope
Thiết kế và xây dựng kiến trúc ứng dụng Android hiện đại theo chuẩn hướng dẫn chính thức của Google (Modern Android Architecture - MAD); áp dụng mô hình phân lớp rõ ràng (UI Layer, Domain Layer, Data Layer), xây dựng giao diện khai báo bằng Jetpack Compose, quản lý luồng dữ liệu phản ứng (Reactive Data Streams) với Kotlin Coroutines và StateFlow, quản lý vòng đời Activity/Process recreation, lưu trữ cục bộ qua Room DB và tiêm phụ thuộc bằng Hilt / Koin.

## 2. When to Use
- Khi khởi tạo dự án ứng dụng Android mới từ đầu hoặc hiện đại hóa ứng dụng Android cũ (Java/XML View sang Kotlin/Compose).
- Khi gặp các lỗi liên quan đến vòng đời Android (Memory Leaks do giữ tham chiếu Context, mất dữ liệu khi xoay màn hình).
- Khi ứng dụng bị đơ (ANR - Application Not Responding) do chạy tác vụ nặng trên Main Thread.

## 3. When NOT to Use
- Xây dựng ứng dụng iOS nguyên bản (dùng `dex-ios-app-architecture`).
- Xây dựng ứng dụng desktop bằng Electron hoặc Tauri (dùng `dex-electron-security` hoặc `dex-tauri-desktop-integration`).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Yêu cầu tính năng và các màn hình ứng dụng.
- Phiên bản Android SDK tối thiểu (`minSdk >= 24`, `targetSdk = 34+`).
- Thiết kế UI/UX theo tiêu chuẩn Material Design 3.
- **Điều kiện tiên quyết**:
- Android Studio Hedgehog/Iguana hoặc mới hơn, JDK 17, Gradle 8+.
- Hiểu biết về vòng đời Android (Lifecycle, ViewModel, SavedStateHandle).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- **Unidirectional Data Flow (UDF)**: Trạng thái (UI State) chảy xuống dưới tới các composable; sự kiện của người dùng (UI Events) chảy ngược lên ViewModel để xử lý.
- **Single Source of Truth (SSOT)**: Cơ sở dữ liệu Room cục bộ đóng vai trò nguồn chân lý duy nhất; dữ liệu từ mạng được đồng bộ vào Room trước khi hiển thị lên UI.
- **Process Death Resilience**: Sử dụng `SavedStateHandle` trong ViewModel để khôi phục trạng thái quan trọng khi hệ điều hành Android thu hồi RAM và hủy process ngầm.
- **Quy tắc quyết định kỹ thuật**:
- **Tuyệt Đối Không Chạy I/O Trên Dispatchers.Main**: Mọi thao tác truy vấn Room, đọc ghi tệp hoặc gọi Network API bắt buộc phải chuyển sang `Dispatchers.IO`.
- **Không Lưu Context Trong ViewModel**: Không bao giờ truyền tham chiếu `Activity`, `View` hoặc `Context` vào ViewModel để tránh rò rỉ bộ nhớ (Memory Leak).
- **Sử Dụng Immutability Cho UI State**: UI State phải là Kotlin `data class` với các trường `val` bất biến, phát ra qua `StateFlow`.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Ứng dụng crash khi người dùng xoay màn hình**: Do Activity bị hủy và tạo lại làm mất biến trạng thái -> Khắc phục: Chuyển toàn bộ state vào `ViewModel` kết hợp `rememberSaveable`.
- **ANR (Application Not Responding) trong 5 giây**: Do thực hiện giải mã JSON hoặc đọc DB Room trên luồng giao diện -> Khắc phục: Bao bọc tác vụ trong `withContext(Dispatchers.IO)`.

## 6. Step-by-Step Execution Workflow
1. Thiết lập cấu trúc dự án đa tầng: `core/model`, `core/data`, `core/designsystem`, `feature/*`.
2. Cấu hình tiêm phụ thuộc Hilt (`@HiltAndroidApp`, `@AndroidEntryPoint`, `@HiltViewModel`).
3. Xây dựng Data Layer: Định nghĩa Room Entity, DAO và Retrofit API Service, gói trong Repository Pattern.
4. Xây dựng UI Layer: Khởi tạo ViewModel kế thừa Hilt, định nghĩa sealed interface `UiState` (Loading, Success, Error).
5. Thiết kế giao diện Compose: Sử dụng các stateless composables nhận state và lambda callbacks.
6. Thu thập State trong Compose một cách an toàn vòng đời: `collectAsStateWithLifecycle()`.
7. Viết unit test cho ViewModel bằng `StandardTestDispatcher` và mock Repository.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```kotlin
// Modern Android ViewModel with StateFlow and Coroutines
@HiltViewModel
class UserProfileViewModel @Inject constructor(
    private val userRepository: UserRepository,
    private val savedStateHandle: SavedStateHandle
) : ViewModel() {

    private val _uiState = MutableStateFlow<ProfileUiState>(ProfileUiState.Loading)
    val uiState: StateFlow<ProfileUiState> = _uiState.asStateFlow()

    init {
        loadUserProfile()
    }

    fun loadUserProfile() {
        viewModelScope.launch {
            _uiState.value = ProfileUiState.Loading
            userRepository.getUserProfile()
                .flowOn(Dispatchers.IO)
                .catch { exception -> _uiState.value = ProfileUiState.Error(exception.message) }
                .collect { profile -> _uiState.value = ProfileUiState.Success(profile) }
        }
    }
}

sealed interface ProfileUiState {
    object Loading : ProfileUiState
    data class Success(val profile: UserProfile) : ProfileUiState
    data class Error(val message: String?) : ProfileUiState
}
```

### Lệnh xác minh & thực thi:
- Kiểm tra build và lint mã nguồn: `./gradlew lintDebug`
- Chạy unit tests cho tầng Data & ViewModel: `./gradlew testDebugUnitTest`
- Chạy kiểm thử giao diện Compose trên emulator: `./gradlew connectedAndroidTest`

## 8. Anti-Patterns & Common Traps
- **Truyền NavController xuyên suốt các Composable con**: Gây gắn kết chặt (tight coupling), khó tái sử dụng UI.
- **Sử dụng LiveData trong các dự án Kotlin thuần mới**: Nên dùng `StateFlow` và `SharedFlow` hỗ trợ Coroutines tốt hơn.
- **Bắt ngoại lệ Exception chung chung mà không phục hồi UI**: Để màn hình treo vô tận ở trạng thái Loading.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Kiến trúc tuân thủ UDF và phân tách 3 lớp UI/Domain/Data rõ rệt.
- QG-07: 0 lỗi memory leak phát hiện bởi LeakCanary trong quá trình test.
- QG-11: 100% các composable màn hình chính đều hỗ trợ preview (`@Preview`).
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi deploy.

## 10. Security & Safety Boundaries
- Lưu trữ nhạy cảm (API token, mật khẩu) bắt buộc dùng Android Jetpack `EncryptedSharedPreferences` hoặc Keystore.
- Bật cờ `android:networkSecurityConfig` chặn lưu lượng HTTP không mã hóa (Cleartext Traffic).
- Không bao giờ lưu trữ hardcoded secret hoặc cấp quyền quá mức (over-permissioned IAM).

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Môi trường Mobile & Desktop**: Hỗ trợ Android (Kotlin/Gradle), iOS (Swift/Xcode), Electron (Node.js/Chromium), Tauri (Rust/WebKit).

## 12. Deliverables & Output Artifacts
- Cấu trúc mã nguồn Android hoàn chỉnh theo chuẩn Modern Android Architecture.
- Bộ Room Database, ViewModel và Composable screens.
- Báo cáo kiểm thử unit test và instrumented test.

## 13. Related & Complementary Skills
- `dex-mobile-offline-sync`: Tích hợp cơ chế đồng bộ offline với Room DB.
- `dex-mobile-release-pipelines`: Đóng gói APK/AAB và phát hành lên Google Play.
- `dex-mobile-performance-profiling`: Đo lường frame rate và khởi động ứng dụng Android.

## 14. Realistic Usage Example
### Tình huống thực tế:
Một ứng dụng bán hàng trên Android bị phàn nàn là thường xuyên mất giỏ hàng khi người dùng nhận cuộc gọi điện thoại (bị hủy process). Áp dụng `dex-android-app-architecture`, kỹ sư tái cấu trúc sang MVVM với StateFlow, lưu giỏ hàng vào Room DB làm nguồn chân lý duy nhất và dùng `SavedStateHandle` trong ViewModel. Khi nhận cuộc gọi xong quay lại, ứng dụng khôi phục giỏ hàng lập tức trong 0.2 giây mà không mất dữ liệu.
