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
      <a-layout>
        <a-layout-sider v-model:collapsed="collapsed" collapsible width="200" style="background: #fff; border-right: 1px solid #f0f0f0">
          <a-menu v-model:selectedKeys="selectedKeys" mode="inline" style="height: 100%; border-inline-end: none" @click="onMenuClick">
            <a-menu-item key="dashboard">
              <DashboardOutlined />
              <span>Dashboard</span>
            </a-menu-item>
            <a-menu-item key="nhap">
              <EditOutlined />
              <span>Nhập dữ liệu</span>
            </a-menu-item>
            <a-menu-item key="xem">
              <TableOutlined />
              <span>Xem dữ liệu</span>
            </a-menu-item>
            <a-menu-item key="goi">
              <InboxOutlined />
              <span>Quản lý gói</span>
            </a-menu-item>
          </a-menu>
        </a-layout-sider>
        <a-layout-content style="padding: 16px 24px">
          <component :is="currentComponent" />
        </a-layout-content>
      </a-layout>
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
import { ref, computed, watch, onMounted } from 'vue'
import { DashboardOutlined, EditOutlined, TableOutlined, InboxOutlined } from '@ant-design/icons-vue'
import { useRouter, useRoute } from 'vue-router'
import viVN from 'ant-design-vue/es/locale/vi_VN'
import dayjs from 'dayjs'
import 'dayjs/locale/vi'
import Dashboard from './components/Dashboard.vue'
import DataEntryForm from './components/DataEntryForm.vue'
import DataTable from './components/DataTable.vue'
import GoiManager from './components/GoiManager.vue'
import { useDataStore } from './stores/dataStore'
import { downloadTemplate, uploadTemplate, previewUpload, confirmUpload } from './services/api'
import { message } from 'ant-design-vue'

dayjs.locale('vi')

const locale = viVN
const router = useRouter()
const route = useRoute()
const store = useDataStore()
const collapsed = ref(false)
const loading = ref(false)
const uploading = ref(false)

const componentMap = { dashboard: Dashboard, nhap: DataEntryForm, xem: DataTable, goi: GoiManager }

function hashToMenuKey() {
  const key = window.location.hash.replace('#/', '').split('/')[0]
  return key || 'dashboard'
}
const selectedKeys = ref([hashToMenuKey()])
const currentComponent = computed(() => componentMap[selectedKeys.value[0]])

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

const routeNameMap = { dashboard: 'Dashboard', nhap: 'Nhap', xem: 'Xem', goi: 'Goi' }

function onMenuClick({ key }) {
  selectedKeys.value = [key]
  router.push({ name: routeNameMap[key] })
  if (key === 'xem') {
    store.loadRecords()
  }
}

watch(() => route.name, (name) => {
  const map = { Dashboard: 'dashboard', Xem: 'xem', Goi: 'goi', Nhap: 'nhap' }
  selectedKeys.value = [map[name] || 'dashboard']
})

onMounted(() => {
  store.loadDropdowns()
  store.loadRecords()
})
</script>
