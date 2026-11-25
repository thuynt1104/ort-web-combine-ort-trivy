# Open Source License Policy

Rule đánh giá **PASS**, **FAIL** hoặc **REVIEW** cho từng thành phần mã nguồn mở. Agent đọc file này, chọn đúng Type và Target, rồi trả kết quả theo checklist. File này là quy tắc kỹ thuật cho agent, không thay tư vấn pháp lý.

## Kết quả agent được trả

| Kết quả | Nghĩa |
| --- | --- |
| PASS | Đúng target và mọi mục bắt buộc trong checklist đều đạt. |
| FAIL | Đúng target và có ít nhất một mục bắt buộc không đạt. |
| REVIEW | Không đủ dữ liệu, license là `OR`/`AND`/`WITH`, hoặc rule bắt buộc người review. |

Agent nhận các đầu vào sau, nếu thiếu thì kết quả là **REVIEW**:

- SPDX license expression của component, ví dụ `Apache-2.0`, `GPL-2.0-only OR MIT`.
- Sản phẩm là Distributed SW hay SaaS SW.
- Người dùng là Internal User hay External User.
- Component có bị sửa, liên kết tĩnh, hoặc gộp vào phần mềm đóng hay không.
- Bản phân phối có giữ license notice, `NOTICE`, và lời đề nghị mã nguồn khi license yêu cầu hay không.

Thứ tự áp dụng:

1. Nếu expression có `OR`, **PASS** khi có ít nhất một nhánh PASS cho cùng Target.
2. Nếu expression có `AND`, mọi nhánh phải PASS.
3. Nếu expression có `WITH`, áp dụng exception trước license gốc.
4. Không nhận ra license thì dùng Type **Unknown**.

## Định nghĩa

### Distributed SW

Distributed SW là phần mềm mà người nhận được một bản để tự chạy hoặc tự nhúng. Bản đó có thể là source, binary, thư viện, SDK, installer, ứng dụng mobile, image container, firmware, hoặc appliance.

Copy rời khỏi tổ chức phát hành là điều kiện phân biệt. Gửi binary cho khách, đăng package lên registry công khai, hoặc cài phần mềm lên máy của khách đều là Distributed SW.

Chạy phần mềm trên hạ tầng của chính tổ chức và chỉ mở giao diện qua mạng thì không phải Distributed SW.

### SaaS SW

SaaS SW là phần mềm do tổ chức chạy trên hạ tầng của mình. Người dùng chỉ truy cập qua mạng, ví dụ trình duyệt hoặc API, và không nhận bản source hay binary để tự chạy.

Sửa dịch vụ, thêm component vào dịch vụ, hoặc cho khách hàng bên ngoài đăng nhập vẫn là SaaS SW, miễn là bản phần mềm không được giao cho người dùng.

Nếu cùng một sản phẩm vừa chạy dạng dịch vụ vừa giao binary, SDK, hoặc bản on-prem cho khách, phần giao ra ngoài được đánh giá như Distributed SW.

### Internal User

Internal User là nhân viên, nhà thầu, hoặc hệ thống của chính tổ chức, dùng phần mềm cho nội bộ. Bản phần mềm không được giao cho khách hàng, đối tác bên ngoài, hoặc cộng đồng.

Dùng thư viện GPL trong công cụ nội bộ, không ship công cụ đó ra ngoài, là sử dụng bởi Internal User.

### External User

External User là người hoặc tổ chức bên ngoài được nhận phần mềm, hoặc được dùng dịch vụ. Khách hàng, đối tác, người dùng cuối của sản phẩm thương mại, và người tải bản phát hành công khai đều là External User.

Một sản phẩm có cả người dùng nội bộ và khách hàng thì áp dụng Target của External User.

## Type

Agent gán mỗi license vào một Type. Ví dụ SPDX dưới đây là các identifier thường gặp, không phải danh sách đủ.

| Type | License thường gặp | Nghĩa ngắn |
| --- | --- | --- |
| Permissive | `MIT`, `BSD-2-Clause`, `BSD-3-Clause`, `Apache-2.0`, `ISC`, `0BSD`, `Unlicense`, `Zlib` | Cho dùng, sửa, phân phối. Giữ notice. `Apache-2.0` thêm file `NOTICE` và điều khoản bằng sáng chế. |
| Weak Copyleft | `LGPL-2.1-only`, `LGPL-3.0-only`, `MPL-2.0`, `EPL-2.0`, `CDDL-1.0` | Nghĩa vụ mở mã giới hạn ở thư viện hoặc từng file, và chỉ phát sinh khi phân phối bản đó. |
| Strong Copyleft | `GPL-2.0-only`, `GPL-3.0-only`, `OSL-3.0` | Gộp vào một chương trình rồi phân phối thì cả chương trình phải tuân copyleft và có lời đề nghị mã nguồn. |
| Network Copyleft | `AGPL-3.0-only`, `SSPL-1.0`, `RPL-1.5` | Chạy thành dịch vụ cho người ngoài cũng làm phát sinh nghĩa vụ mở mã của dịch vụ tương ứng. |
| Restricted | `CC-BY-NC-4.0`, `BUSL-1.1`, license có `Commons-Clause`, `PolyForm-Noncommercial-1.0.0` | Cấm hoặc giới hạn mục đích thương mại, hoặc chưa cho dùng tự do. |
| Unknown | Không có license, `NOASSERTION`, text không map được sang SPDX | Chưa có quyền sử dụng đã được ghi nhận. |

## Rule

Mỗi rule có **Type**, **Target** và **Checklist**. Mục đánh dấu bắt buộc mà không đạt thì kết quả là **FAIL**.

### PERM-ALL

- **Type:** Permissive
- **Target:** Distributed SW hoặc SaaS SW, Internal User hoặc External User
- **Checklist:**
  - Giữ nguyên copyright notice và nội dung license trong mã nguồn hoặc bản phân phối.
  - Với `Apache-2.0`, đính kèm file `NOTICE` nếu component gốc có file đó.
  - Không xóa hoặc đổi điều khoản bằng sáng chế của `Apache-2.0`.
- **Result:** PASS khi mọi mục đạt. FAIL khi thiếu notice hoặc `NOTICE` bắt buộc.

### WEAK-INTERNAL

- **Type:** Weak Copyleft
- **Target:** Distributed SW hoặc SaaS SW, chỉ Internal User
- **Checklist:**
  - Component chỉ được dùng trong tổ chức.
  - Không giao source, binary, SDK, hoặc image cho External User.
- **Result:** PASS khi cả hai mục đạt.

### WEAK-SAAS-EXTERNAL

- **Type:** Weak Copyleft
- **Target:** SaaS SW, External User
- **Checklist:**
  - Người dùng không nhận bản cài của component.
  - File hoặc thư viện thuộc license này không được ship riêng dưới dạng SDK, plugin, hoặc package.
  - Notice gốc vẫn còn trong kho mã của dịch vụ.
- **Result:** PASS khi không có bản nào được giao ra ngoài. FAIL khi SDK hoặc binary của chính component được giao cho khách.

### WEAK-DIST-EXTERNAL

- **Type:** Weak Copyleft
- **Target:** Distributed SW, External User
- **Checklist:**
  - Người nhận có thể thay bản thư viện LGPL đã liên kết động, hoặc nhận đúng file MPL/EPL/CDDL đã sửa cùng license gốc của file đó.
  - Phần mã đóng không bị đặt dưới copyleft chỉ vì gọi thư viện qua giao diện động hoặc ranh giới file.
  - Copyright notice và license text của component đi cùng bản phân phối.
  - Sửa file thuộc MPL, EPL, hoặc CDDL thì chính file đã sửa được cung cấp.
- **Result:** PASS khi mọi mục đạt. FAIL khi liên kết tĩnh LGPL vào phần mềm đóng mà không cung cấp object file để link lại, hoặc sửa file copyleft yếu mà không mở file đó.

### STRONG-INTERNAL

- **Type:** Strong Copyleft
- **Target:** Distributed SW hoặc SaaS SW, chỉ Internal User
- **Checklist:**
  - Không có External User nào nhận bản phần mềm.
  - Không đăng bản build lên registry hoặc trang tải công khai.
- **Result:** PASS khi phần mềm không rời khỏi tổ chức.

### STRONG-SAAS-EXTERNAL

- **Type:** Strong Copyleft
- **Target:** SaaS SW, External User
- **Checklist:**
  - Dịch vụ chỉ được truy cập qua mạng. Khách không nhận source, binary, container image, hoặc appliance.
  - License không thuộc Type Network Copyleft.
- **Result:** PASS khi đúng hai mục trên. `GPL-2.0` và `GPL-3.0` không tự phát sinh nghĩa vụ mở mã chỉ vì chạy SaaS.

### STRONG-DIST-EXTERNAL

- **Type:** Strong Copyleft
- **Target:** Distributed SW, External User
- **Checklist:**
  - Toàn bộ chương trình kết hợp được phát hành dưới license tương thích với copyleft đó.
  - Kèm lời đề nghị mã nguồn tương ứng, theo đúng thời hạn và hình thức của license.
  - Không có điều khoản riêng làm hạn chế quyền mà GPL đã cấp cho người nhận.
- **Result:** FAIL khi chương trình đóng được phân phối cùng component copyleft mạnh. PASS chỉ khi cả checklist đạt.

### NET-INTERNAL

- **Type:** Network Copyleft
- **Target:** Distributed SW hoặc SaaS SW, chỉ Internal User
- **Checklist:**
  - Dịch vụ và bản cài không dành cho External User.
  - Không dùng component này trong sản phẩm thương mại hướng ra khách hàng.
- **Result:** PASS khi chỉ dùng nội bộ.

### NET-SAAS-EXTERNAL

- **Type:** Network Copyleft
- **Target:** SaaS SW, External User
- **Checklist:**
  - External User của dịch vụ nhận được mã nguồn tương ứng của chương trình, kể cả phần sửa, theo điều kiện của `AGPL-3.0` hoặc license mạng tương đương.
  - Lời đề nghị mã nguồn hiện trên dịch vụ và dùng được trong suốt thời gian dịch vụ vận hành.
  - Với `SSPL-1.0`, mã được mở bao gồm cả phần quản trị dịch vụ mà license đó yêu cầu, nếu tổ chức chấp nhận điều kiện này.
- **Result:** FAIL khi cung cấp SaaS cho External User mà không có lời đề nghị mã nguồn đạt checklist.

### NET-DIST-EXTERNAL

- **Type:** Network Copyleft
- **Target:** Distributed SW, External User
- **Checklist:**
  - Người nhận bản phân phối nhận mã nguồn tương ứng.
  - Nếu người nhận chạy bản đó thành dịch vụ cho người khác, nghĩa vụ mở mã qua mạng vẫn được giữ nguyên trong bản giao.
- **Result:** FAIL khi phân phối mà không kèm mã nguồn hoặc làm mất nghĩa vụ copyleft.

### RESTRICTED-EXTERNAL

- **Type:** Restricted
- **Target:** Distributed SW hoặc SaaS SW, External User
- **Checklist:**
  - License cho phép đúng mục đích thương mại và đúng hình thức phân phối đang dùng.
  - Có bằng chứng chấp thuận riêng nếu license không cho dùng trong sản phẩm thương mại.
- **Result:** FAIL khi không có cả hai mục. `CC-BY-NC`, Commons Clause, và non-commercial không được dùng cho sản phẩm đưa tới External User.

### RESTRICTED-INTERNAL

- **Type:** Restricted
- **Target:** Distributed SW hoặc SaaS SW, chỉ Internal User
- **Checklist:**
  - Việc dùng nội bộ không bị chính license cấm.
  - Không trộn bản này vào sản phẩm sẽ phân phối hoặc cung cấp SaaS cho External User.
- **Result:** REVIEW. Agent không tự PASS.

### UNKNOWN-ANY

- **Type:** Unknown
- **Target:** Mọi kết hợp của Distributed SW, SaaS SW, Internal User, External User
- **Checklist:**
  - Có file license hoặc SPDX expression đã được nhận dạng.
  - Quyền dùng phủ đúng target đang xét.
- **Result:** FAIL với External User khi không có license. REVIEW với chỉ Internal User khi chưa đọc được file license nhưng component chưa rời tổ chức.
