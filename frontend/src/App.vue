<template>
  <a-config-provider :locale="locale">
    <a-layout style="min-height: 100vh">
      <a-layout-header style="background: #fff; padding: 0 24px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #f0f0f0">
        <h2 style="margin: 0; color: #1677ff">Hệ thống nhập dữ liệu</h2>
        <a-space>
          <a-button @click="handleDownload" :loading="loading">Tải template</a-button>
          <a-upload :before-upload="handleUpload" :show-upload-list="false" accept=".xlsx,.xls">
            <a-button :loading="uploading">Tải lên Excel</a-button>
          </a-upload>
        </a-space>
      </a-layout-header>
      <a-layout-content style="padding: 16px 24px">
        <a-tabs v-model:activeKey="activeTab" @change="onTabChange">
          <a-tab-pane key="nhap" tab="📝 Nhập dữ liệu">
            <DataEntryForm />
          </a-tab-pane>
          <a-tab-pane key="xem" tab="📋 Xem dữ liệu">
            <DataTable />
          </a-tab-pane>
          <a-tab-pane key="goi" tab="📦 Quản lý gói">
            <GoiManager />
          </a-tab-pane>
        </a-tabs>
      </a-layout-content>
    </a-layout>

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
  </a-config-provider>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import viVN from 'ant-design-vue/es/locale/vi_VN'
import dayjs from 'dayjs'
import 'dayjs/locale/vi'
import DataEntryForm from './components/DataEntryForm.vue'
import DataTable from './components/DataTable.vue'
import GoiManager from './components/GoiManager.vue'
import { useDataStore } from './stores/dataStore'
import { downloadTemplate, uploadTemplate, previewUpload, confirmUpload } from './services/api'
import { message } from 'ant-design-vue'

dayjs.locale('vi')

const locale = viVN
const router = useRouter()
const activeTab = ref(window.location.hash.includes('/xem') ? 'xem' : window.location.hash.includes('/goi') ? 'goi' : 'nhap')
const store = useDataStore()
const loading = ref(false)
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
  loading.value = true
  downloadTemplate()
  setTimeout(() => { loading.value = false }, 1000)
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

const tabRouteMap = { nhap: 'Nhap', xem: 'Xem', goi: 'Goi' }

function onTabChange(key) {
  router.push({ name: tabRouteMap[key] })
  if (key === 'xem') {
    store.loadRecords()
  }
}

const route = useRoute()
watch(() => route.name, (name) => {
  if (name === 'Xem') activeTab.value = 'xem'
  else if (name === 'Goi') activeTab.value = 'goi'
  else activeTab.value = 'nhap'
})

onMounted(() => {
  store.loadDropdowns()
  store.loadRecords()
})
</script>
