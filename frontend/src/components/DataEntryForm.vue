<template>
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
        <a-col :span="3">
          <a-form-item label="Sale">
            <a-select v-model:value="store.form.sale" placeholder="Chọn Sale" allow-clear>
              <a-select-option v-for="s in store.saleOptions" :key="s" :value="s">{{ s }}</a-select-option>
            </a-select>
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="PT chăm sóc">
            <a-select v-model:value="store.form.ptChamSoc" placeholder="Chọn PT" allow-clear>
              <a-select-option v-for="p in store.ptChamSocOptions" :key="p" :value="p">{{ p }}</a-select-option>
            </a-select>
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="CS nhập">
            <a-select v-model:value="store.form.csNhap" placeholder="Chọn CS" allow-clear>
              <a-select-option v-for="c in store.csNhapOptions" :key="c" :value="c">{{ c }}</a-select-option>
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
            <a-input-number :value="store.donGiaNiemYet" disabled style="width: 100%" :formatter="v => `${v}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')" />
          </a-form-item>
        </a-col>
      </a-row>
    </a-card>

    <a-card title="Buổi tập & Thời gian" style="margin-bottom: 16px">
      <a-row :gutter="16">
        <a-col :span="3">
          <a-form-item label="PT GYM">
            <a-input-number v-model:value="store.form.ptGym" :min="0" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="PTTL/PTP">
            <a-input-number v-model:value="store.form.pttl" :min="0" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="2">
          <a-form-item label="Daily">
            <a-input-number v-model:value="store.form.daily" :min="0" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="2">
          <a-form-item label="Bơi">
            <a-input-number v-model:value="store.form.boi" :min="0" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="2">
          <a-form-item label="PT tặng">
            <a-input-number v-model:value="store.form.ptTang" :min="0" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="Buổi PT cố định">
            <a-input-number v-model:value="store.form.buoiPtCoDinh" :min="0" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="Tổng SS">
            <a-input-number :value="store.tongSS" disabled style="width: 100%" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-row :gutter="16">
        <a-col :span="3">
          <a-form-item label="Số tháng">
            <a-input-number v-model:value="store.form.soThang" :min="0" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="Cộng tháng BL">
            <a-input-number v-model:value="store.form.congThangBL" :min="0" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="Cộng tháng tặng">
            <a-input-number v-model:value="store.form.congThangTang" :min="0" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="Cộng ngày tặng">
            <a-input-number v-model:value="store.form.congNgayTang" :min="0" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="Tổng số tháng">
            <a-input-number :value="store.tongSoThang" disabled style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="4">
          <a-form-item label="Gói tập">
            <a-input :value="store.goiTap" disabled />
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
        <a-col :span="4">
          <a-form-item label="Tổng tiền bảo lưu">
            <a-input-number :value="store.tongTienBaoLuu" disabled style="width: 100%" :formatter="v => `${v}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')" />
          </a-form-item>
        </a-col>
        <a-col :span="4">
          <a-form-item label="Tổng tiền buổi dạy">
            <a-input-number :value="store.tongTienBuoiDay" disabled style="width: 100%" :formatter="v => `${v}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')" />
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="Tổng tiền">
            <a-input-number :value="store.tongTien" disabled style="width: 100%" :formatter="v => `${v}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')" />
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="Mức ưu đãi (%)">
            <a-input-number v-model:value="store.form.mucUuDai" :min="0" :max="100" :formatter="v => `${v}%`" :parser="v => v.replace('%', '')" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="4">
          <a-form-item label="Số tiền KH giảm">
            <a-input-number :value="store.soTienKHGiam" disabled style="width: 100%" :formatter="v => `${v}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')" />
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item label="Tổng">
            <a-input-number :value="store.tong" disabled style="width: 100%" :formatter="v => `${v}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-row :gutter="16">
        <a-col :span="4">
          <a-form-item label="% Sale tính DT">
            <a-input-number v-model:value="store.form.phanTramSaleDT" :min="0" :max="100" :formatter="v => `${v}%`" :parser="v => v.replace('%', '')" style="width: 100%" />
          </a-form-item>
        </a-col>
        <a-col :span="4">
          <a-form-item label="Tiền DV phải thu">
            <a-input-number :value="store.soTienDVPhaiThu" disabled style="width: 100%" :formatter="v => `${v}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')" />
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
</template>

<script setup>
import { ref } from 'vue'
import { message } from 'ant-design-vue'
import { useDataStore } from '../stores/dataStore'

const store = useDataStore()
const saving = ref(false)

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
