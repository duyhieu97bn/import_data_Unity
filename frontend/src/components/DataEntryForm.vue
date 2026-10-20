<template>
  <div style="margin-bottom: 12px; text-align: right">
    <a-space>
      <a-button @click="handleDownload" :loading="downloading">Tải template</a-button>
      <a-upload :before-upload="handleUpload" :show-upload-list="false" accept=".xlsx,.xls">
        <a-button :loading="uploading">Tải lên Excel</a-button>
      </a-upload>
    </a-space>
  </div>
  <a-form layout="vertical" :model="store.form" style="max-width: 1400px; margin: 0 auto">
    <a-card title="Thông tin cơ bản" style="margin-bottom: 16px">
      <a-row :gutter="16">
        <a-col :span="3">
          <a-form-item label="CLB">
            <a-select v-model:value="store.form.clb" placeholder="Chọn CLB" allow-clear>
              <a-select-option value="Unity">Unity</a-select-option>
            </a-select>
          </a-form-item>
        </a-col>
        <a-col :span="2">
          <a-form-item label="Ngày">
            <a-input-number v-model:value="store.form.ngay" :min="1" :max="31" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="2">
          <a-form-item label="Tháng">
            <a-input-number v-model:value="store.form.thang" :min="1" :max="12" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="2">
          <a-form-item label="Năm">
            <a-input-number v-model:value="store.form.nam" :min="2000" :max="2100" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="4">
          <a-form-item label="Ngày tháng năm">
            <a-input :value="store.ngayThangNam" disabled />
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="Quyển số">
            <a-input :value="store.quyenSo" disabled />
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="Số BN">
            <a-input v-model:value="store.form.soBN" />
          </a-form-item>
        </a-col>
        <a-col :span="5">
          <a-form-item label="Mã KH">
            <a-input v-model:value="store.form.maKH" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-row :gutter="16">
        <a-col :span="6">
          <a-form-item label="Họ và tên KH">
            <a-input v-model:value="store.form.hoTenKH" />
          </a-form-item>
        </a-col>
        <a-col :span="4">
          <a-form-item label="Ngày sinh">
            <a-date-picker v-model:value="store.form.ngaySinh" value-format="DD/MM/YYYY" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="4">
          <a-form-item label="SĐT">
            <a-input v-model:value="store.form.sdt" />
          </a-form-item>
        </a-col>
      </a-row>
    </a-card>

    <a-card title="Gói dịch vụ" style="margin-bottom: 16px">
      <a-row :gutter="16">
        <a-col :span="4">
          <a-form-item label="Mã gói">
            <a-select
              v-model:value="store.form.maGoi"
              show-search
              placeholder="Chọn mã gói"
              :filter-option="filterGoi"
              @click="store.loadGoiOptions"
              @change="store.setSelectedGoi"
              allow-clear
            >
              <a-select-option v-for="g in store.goiOptions" :key="g.maGoi" :value="g.maGoi">
                {{ g.maGoi }}
              </a-select-option>
            </a-select>
          </a-form-item>
        </a-col>
        <a-col v-for="d in dropdownFields" :key="d.key" :span="3">
          <a-form-item :label="d.label">
            <a-select v-model:value="store.form[d.key]" :placeholder="'Chọn ' + d.label" allow-clear>
              <a-select-option v-for="opt in d.options" :key="opt" :value="opt">{{ opt }}</a-select-option>
            </a-select>
          </a-form-item>
        </a-col>
      </a-row>
      <a-row :gutter="16">
        <a-col :span="3">
          <a-form-item label="Loại thẻ 1">
            <a-input :value="store.loaiThe1" disabled />
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="Loại thẻ 2">
            <a-input :value="store.loaiThe2" disabled />
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="Phân bổ 1">
            <a-input :value="store.phanBo1" disabled />
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="Phân bổ 2">
            <a-input v-model:value="store.form.phanBo2" />
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="Số tháng, buổi">
            <a-input :value="store.soThangBuoi" disabled />
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="Đơn giá niêm yết">
            <a-input-number :value="store.donGiaNiemYet" disabled :formatter="formatMoney" style="width: 100%" />
          </a-form-item>
        </a-col>
      </a-row>
    </a-card>

    <a-card title="Buổi tập & Thời gian" style="margin-bottom: 16px">
      <a-row :gutter="16">
        <a-col v-for="f in sessionFields" :key="f.key" :span="f.span">
          <a-form-item :label="f.label">
            <a-input-number
              v-if="f.editable"
              v-model:value="store.form[f.key]"
              :min="0"
              style="width: 100%"
            />
            <a-input-number
              v-else
              :value="store[f.key]"
              disabled
              style="width: 100%"
            />
          </a-form-item>
        </a-col>
      </a-row>
      <a-row :gutter="16">
        <a-col v-for="f in monthFields" :key="f.key" :span="f.span">
          <a-form-item :label="f.label">
            <a-input-number
              v-if="f.editable"
              v-model:value="store.form[f.key]"
              :min="0"
              style="width: 100%"
            />
            <a-input :value="store[f.key]" disabled v-else-if="f.type === 'text'" />
            <a-input-number
              v-else
              :value="store[f.key]"
              disabled
              style="width: 100%"
            />
          </a-form-item>
        </a-col>
      </a-row>
      <a-row :gutter="16">
        <a-col :span="4">
          <a-form-item label="Khung giờ tập">
            <a-input v-model:value="store.form.khungGioTap" />
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="Chuyển nhượng">
            <a-input v-model:value="store.form.chuyenNhuong" />
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="Số HĐ">
            <a-input v-model:value="store.form.soHD" />
          </a-form-item>
        </a-col>
      </a-row>
    </a-card>

    <a-card title="Thời hạn" style="margin-bottom: 16px">
      <a-row :gutter="16">
        <a-col :span="4">
          <a-form-item label="Ngày bắt đầu">
            <a-date-picker v-model:value="store.form.ngayBatDau" value-format="YYYY-MM-DD" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="4">
          <a-form-item label="Ngày kết thúc">
            <a-date-picker :value="store.ngayKetThuc" disabled style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="4">
          <a-form-item label="Tình trạng">
            <a-input :value="store.tinhTrangText" disabled />
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="Tổng số ngày">
            <a-input-number :value="store.tongSoNgay" disabled style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="Số ngày đã đi">
            <a-input-number v-model:value="store.form.tongNgayDaDi" :min="0" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="Số ngày còn lại">
            <a-input-number :value="store.tongSoNgayConLai" disabled style="width: 100%" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-row :gutter="16">
        <a-col :span="6">
          <a-form-item label="Quà tặng">
            <a-input v-model:value="store.form.quaTang" />
          </a-form-item>
        </a-col>
      </a-row>
    </a-card>

    <a-card title="Tài chính" style="margin-bottom: 16px">
      <a-row :gutter="16">
        <a-col v-for="f in moneyFields" :key="f.key" :span="f.span">
          <a-form-item :label="f.label">
            <a-input-number :value="store[f.key]" disabled :formatter="formatMoney" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="Mức ưu đãi (%)">
            <a-input-number v-model:value="store.form.mucUuDai" :min="0" :max="100" :formatter="formatPercent" :parser="parsePercent" style="width: 100%" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-row :gutter="16">
        <a-col :span="4">
          <a-form-item label="% Sale tính DT">
            <a-input-number v-model:value="store.form.phanTramSaleDT" :min="0" :max="100" :formatter="formatPercent" :parser="parsePercent" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="4">
          <a-form-item label="Tiền DV phải thu">
            <a-input-number :value="store.soTienDVPhaiThu" disabled :formatter="formatMoney" style="width: 100%" />
          </a-form-item>
        </a-col>
      </a-row>
    </a-card>

    <a-card title="Thanh toán" style="margin-bottom: 16px">
      <a-row :gutter="16">
        <a-col :span="4">
          <a-form-item label="BN đặt cọc & TT thiếu">
            <a-input v-model:value="store.form.bnDatCoc" />
          </a-form-item>
        </a-col>
        <a-col :span="4">
          <a-form-item label="Nâng cấp">
            <a-input v-model:value="store.form.tenGoiNangCap" />
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="Tiền KH nâng cấp">
            <a-input v-model:value="store.form.soTienKHNangCap" />
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="KH đã đặt cọc">
            <a-input v-model:value="store.form.khDaDatCoc" />
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="Tổng ĐC, NC">
            <a-input v-model:value="store.form.tongDatCocNangCap" />
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="Còn phải thu KH">
            <a-input v-model:value="store.form.conPhaiThuKH" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-row :gutter="16">
        <a-col :span="3">
          <a-form-item label="Đặt cọc">
            <a-input v-model:value="store.form.datCoc" />
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="TT phần thiếu">
            <a-input v-model:value="store.form.ttPhanThieu" />
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="Đóng Full">
            <a-input v-model:value="store.form.dongFull" />
          </a-form-item>
        </a-col>
        <a-col :span="2">
          <a-form-item label="Phí Pos">
            <a-input v-model:value="store.form.phiPos" />
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="Doanh thu">
            <a-input v-model:value="store.form.doanhThu" />
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="Hình thức TT">
            <a-input v-model:value="store.form.hinhThucTT" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-row :gutter="16">
        <a-col :span="3">
          <a-form-item label="Đã nhận TM">
            <a-input v-model:value="store.form.daNhanTM" />
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="CK chung">
            <a-input v-model:value="store.form.ckChung" />
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="Tổng tiền CK chung">
            <a-input v-model:value="store.form.tongTienCKChung" />
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="Trạng thái">
            <a-input v-model:value="store.form.trangThai" />
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="Tổng gói tập">
            <a-input v-model:value="store.form.tongGoiTap" />
          </a-form-item>
        </a-col>
      </a-row>
    </a-card>

    <a-card title="Bổ sung" style="margin-bottom: 16px">
      <a-row :gutter="16">
        <a-col :span="2">
          <a-form-item label="Loại">
            <a-input v-model:value="store.form.loai" />
          </a-form-item>
        </a-col>
        <a-col :span="2">
          <a-form-item label="Lượt">
            <a-input v-model:value="store.form.luot" />
          </a-form-item>
        </a-col>
        <a-col :span="2">
          <a-form-item label="Nguồn">
            <a-input v-model:value="store.form.nguon" />
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="Tình trạng">
            <a-input v-model:value="store.form.tinhTrang" />
          </a-form-item>
        </a-col>
        <a-col :span="4">
          <a-form-item label="Đã nhập time soft bởi">
            <a-input v-model:value="store.form.daNhapTimeSoft" />
          </a-form-item>
        </a-col>
        <a-col :span="2">
          <a-form-item label="Kích hoạt">
            <a-checkbox v-model:checked="store.form.daKichHoat" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-row :gutter="16">
        <a-col :span="6">
          <a-form-item label="Tổng hợp dạy show GX">
            <a-input v-model:value="store.form.tongHopDayShowGX" />
          </a-form-item>
        </a-col>
        <a-col :span="4">
          <a-form-item label="Tháng hoàn thiện HĐ">
            <a-input v-model:value="store.form.thangHoanThienHD" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="Ghi chú">
            <a-textarea v-model:value="store.form.ghiChu" :rows="2" />
          </a-form-item>
        </a-col>
      </a-row>
    </a-card>

    <div style="text-align: center; margin-bottom: 24px">
      <a-space>
        <a-button type="primary" size="large" :loading="saving" @click="handleSave">
          Lưu dữ liệu
        </a-button>
        <a-button size="large" @click="handleReset">
          Làm mới
        </a-button>
      </a-space>
    </div>
  </a-form>

  <a-modal v-model:open="previewVisible" title="Xem trước dữ liệu tải lên" width="90%" :footer="null" :destroy-on-close="true">
    <template v-if="previewRecords.length">
      <a-alert :message="`Tìm thấy ${previewRecords.length} bản ghi trong file.`" type="info" show-icon style="margin-bottom: 12px" />
      <a-table :data-source="previewRecords" :columns="previewColumns" :pagination="{ pageSize: 20 }" size="small" bordered :scroll="{ x: 'max-content' }" :row-key="(r, i) => i" />
      <div style="margin-top: 16px; text-align: right">
        <a-space>
          <a-button @click="previewVisible = false">Huỷ</a-button>
          <a-button type="primary" :loading="confirming" @click="handleConfirmUpload">Xác nhận thêm</a-button>
        </a-space>
      </div>
    </template>
    <a-empty v-else description="Không có dữ liệu" />
  </a-modal>
</template>

<script setup>
import { ref } from 'vue'
import { message } from 'ant-design-vue'
import { useDataStore } from '../stores/dataStore'
import { downloadTemplate, previewUpload, confirmUpload } from '../services/api'

const store = useDataStore()
const saving = ref(false)
const downloading = ref(false)
const uploading = ref(false)
const previewVisible = ref(false)
const previewRecords = ref([])
const confirming = ref(false)

const previewColumns = [
  { title: 'STT', dataIndex: 'stt', width: 60 },
  { title: 'CLB', dataIndex: 'clb', width: 80 },
  { title: 'Ngày', dataIndex: 'ngay', width: 60 },
  { title: 'Tháng', dataIndex: 'thang', width: 60 },
  { title: 'Năm', dataIndex: 'nam', width: 60 },
  { title: 'Họ tên KH', dataIndex: 'hoTenKH', width: 180 },
  { title: 'Ngày sinh', dataIndex: 'ngaySinh', width: 100 },
  { title: 'SĐT', dataIndex: 'sdt', width: 110 },
  { title: 'Mã gói', dataIndex: 'maGoi', width: 100 },
  { title: 'Sale', dataIndex: 'sale', width: 80 },
  { title: 'PT chăm sóc', dataIndex: 'ptChamSoc', width: 100 },
  { title: 'Ngày bắt đầu', dataIndex: 'ngayBatDau', width: 100 },
  { title: 'Ngày kết thúc', dataIndex: 'ngayKetThuc', width: 100 },
  { title: 'Tổng tiền', dataIndex: 'tongTien', width: 100 },
  { title: 'Tình trạng', dataIndex: 'tinhTrang', width: 100 },
  { title: 'Trạng thái', dataIndex: 'trangThai', width: 100 },
  { title: 'Ghi chú', dataIndex: 'ghiChu', width: 150 },
]

function handleDownload() {
  downloading.value = true
  downloadTemplate()
  setTimeout(() => { downloading.value = false }, 1000)
}

async function handleUpload(file) {
  uploading.value = true
  try {
    const res = await previewUpload(file)
    previewRecords.value = res.data.records || []
    previewVisible.value = true
  } catch (e) {
    message.error('Đọc file thất bại: ' + (e.response?.data?.detail || e.message))
  } finally {
    uploading.value = false
  }
  return false
}

async function handleConfirmUpload() {
  confirming.value = true
  try {
    const res = await confirmUpload(previewRecords.value)
    message.success(`Đã thêm ${res.data.added} bản ghi thành công!`)
    previewVisible.value = false
    previewRecords.value = []
    store.loadDropdowns()
    store.loadRecords()
  } catch (e) {
    message.error('Thêm dữ liệu thất bại: ' + (e.response?.data?.detail || e.message))
  } finally {
    confirming.value = false
  }
}

const formatMoney = (v) => v != null ? String(v).replace(/\B(?=(\d{3})+(?!\d))/g, ',') : '0'

const dropdownFields = [
  { key: 'sale', label: 'Sale', options: store.saleOptions },
  { key: 'ptChamSoc', label: 'PT chăm sóc', options: store.ptChamSocOptions },
  { key: 'csNhap', label: 'CS nhập', options: store.csNhapOptions },
]

const moneyFields = [
  { key: 'tongTienBaoLuu', label: 'Tổng tiền bảo lưu', span: 4 },
  { key: 'tongTienBuoiDay', label: 'Tổng tiền buổi dạy', span: 4 },
  { key: 'tongTien', label: 'Tổng tiền', span: 3 },
  { key: 'soTienKHGiam', label: 'Số tiền KH giảm', span: 4 },
  { key: 'tong', label: 'Tổng', span: 3 },
]

const formatPercent = (v) => v != null ? v + '%' : '0%'
const parsePercent = (v) => v ? v.replace('%', '') : '0'

const sessionFields = [
  { key: 'ptGym', label: 'PT GYM', span: 3, editable: true },
  { key: 'pttl', label: 'PTTL/PTP', span: 3, editable: true },
  { key: 'daily', label: 'Daily', span: 2, editable: true },
  { key: 'boi', label: 'Bơi', span: 2, editable: true },
  { key: 'ptTang', label: 'PT tặng', span: 2, editable: true },
  { key: 'buoiPtCoDinh', label: 'Buổi PT cố định', span: 3, editable: true },
  { key: 'tongSS', label: 'Tổng SS', span: 3, editable: false },
]

const monthFields = [
  { key: 'soThang', label: 'Số tháng', span: 3, editable: true },
  { key: 'congThangBL', label: 'Cộng tháng BL', span: 3, editable: true },
  { key: 'congThangTang', label: 'Cộng tháng tặng', span: 3, editable: true },
  { key: 'congNgayTang', label: 'Cộng ngày tặng', span: 3, editable: true },
  { key: 'tongSoThang', label: 'Tổng số tháng', span: 3, editable: false },
  { key: 'goiTap', label: 'Gói tập', span: 4, editable: false, type: 'text' },
]

function filterGoi(input, option) {
  return option.value?.toLowerCase()?.includes(input?.toLowerCase()) ||
    option.children?.toString()?.toLowerCase()?.includes(input?.toLowerCase())
}

async function handleSave() {
  if (!store.form.maGoi) {
    message.warning('Vui lòng chọn Mã gói')
    return
  }
  saving.value = true
  try {
    await store.saveRecord(store.form)
    message.success('Lưu dữ liệu thành công!')
    store.loadRecords()
    handleReset()
  } catch (e) {
    message.error('Lưu thất bại: ' + (e.response?.data?.detail || e.message))
  } finally {
    saving.value = false
  }
}

function handleReset() {
  store.resetForm()
}
</script>
