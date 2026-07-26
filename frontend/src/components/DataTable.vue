<template>
  <div>
    <a-card>
      <a-table
        :data-source="store.savedRecords"
        :columns="columns"
        :scroll="{ x: 3000 }"
        :pagination="pagination"
        @change="onTableChange"
        size="small"
        bordered
      >
        <template #headerCell="{ column }">
          <span style="font-weight: 600; white-space: nowrap">{{ column.title }}</span>
        </template>

        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'stt'">{{ record.stt }}</template>
          <template v-else-if="column.key === 'ngayThangNam'">{{ record.ngayThangNam }}</template>
          <template v-else-if="column.key === 'tongTien'">
            {{ formatMoney(record.tongTien) }}
          </template>
          <template v-else-if="column.key === 'tong'">
            {{ formatMoney(record.tong) }}
          </template>
          <template v-else-if="column.key === 'donGiaNiemYet'">
            {{ formatMoney(record.donGiaNiemYet) }}
          </template>
          <template v-else-if="column.key === 'tinhTrang'">
            <a-tag :color="getStatusColor(record)">{{ record.tinhTrang }}</a-tag>
          </template>
          <template v-else-if="column.key === 'actions'">
            <a-space>
              <a-button type="link" size="small" @click="editRecord(record)">Sửa</a-button>
              <a-button type="link" danger size="small" @click="deleteRecord(record)">Xóa</a-button>
            </a-space>
          </template>
          <template v-else>
            {{ record[column.key] }}
          </template>
        </template>
      </a-table>
    </a-card>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { message, Modal } from 'ant-design-vue'
import { useDataStore } from '../stores/dataStore'
import { useRouter } from 'vue-router'

const store = useDataStore()
const router = useRouter()

const pagination = reactive({
  current: 1,
  pageSize: 20,
  showSizeChanger: true,
  pageSizeOptions: ['10', '20', '50', '100'],
  showTotal: (total) => `Tổng: ${total} dòng`,
})

function onTableChange(pag) {
  pagination.current = pag.current
  pagination.pageSize = pag.pageSize
}

const columns = [
  { title: 'STT', dataIndex: 'stt', key: 'stt', width: 60, fixed: 'left' },
  { title: 'CLB', dataIndex: 'clb', key: 'clb', width: 80 },
  { title: 'Ngày', dataIndex: 'ngay', key: 'ngay', width: 60 },
  { title: 'Tháng', dataIndex: 'thang', key: 'thang', width: 60 },
  { title: 'Năm', dataIndex: 'nam', key: 'nam', width: 60 },
  { title: 'NTN', dataIndex: 'ngayThangNam', key: 'ngayThangNam', width: 100 },
  { title: 'QS', dataIndex: 'quyenSo', key: 'quyenSo', width: 60 },
  { title: 'Số BN', dataIndex: 'soBN', key: 'soBN', width: 80 },
  { title: 'Mã KH', dataIndex: 'maKH', key: 'maKH', width: 100 },
  { title: 'Họ tên KH', dataIndex: 'hoTenKH', key: 'hoTenKH', width: 150 },
  { title: 'Mã gói', dataIndex: 'maGoi', key: 'maGoi', width: 100 },
  { title: 'Sale', dataIndex: 'sale', key: 'sale', width: 80 },
  { title: 'PT GYM', dataIndex: 'ptGym', key: 'ptGym', width: 70 },
  { title: 'PTTL/PTP', dataIndex: 'pttl', key: 'pttl', width: 80 },
  { title: 'Daily', dataIndex: 'daily', key: 'daily', width: 60 },
  { title: 'Bơi', dataIndex: 'boi', key: 'boi', width: 60 },
  { title: 'Số tháng', dataIndex: 'soThang', key: 'soThang', width: 70 },
  { title: 'Tổng tháng', dataIndex: 'tongSoThang', key: 'tongSoThang', width: 80 },
  { title: 'Đơn giá', dataIndex: 'donGiaNiemYet', key: 'donGiaNiemYet', width: 100 },
  { title: 'Tổng tiền', dataIndex: 'tongTien', key: 'tongTien', width: 100 },
  { title: 'Tổng', dataIndex: 'tong', key: 'tong', width: 100 },
  { title: 'Tình trạng', dataIndex: 'tinhTrang', key: 'tinhTrang', width: 150 },
  { title: 'Hành động', key: 'actions', width: 100, fixed: 'right' },
]

function formatMoney(val) {
  if (val === null || val === undefined || val === 0) return '0'
  return Number(val).toLocaleString('vi-VN')
}

function getStatusColor(record) {
  const t = record.tinhTrang || ''
  if (t.includes('Còn')) return 'green'
  if (t.includes('hết hạn')) return 'red'
  return 'default'
}

function editRecord(record) {
  store.setFormFromRecord(record)
  router.push({ name: 'Nhap' })
}

function deleteRecord(record) {
  Modal.confirm({
    title: 'Xác nhận xóa',
    content: `Xóa dòng STT ${record.stt} - ${record.hoTenKH}?`,
    okText: 'Xóa',
    cancelText: 'Hủy',
    okType: 'danger',
    async onOk() {
      try {
        await store.deleteRecord(record.stt)
        message.success('Đã xóa')
        store.loadRecords()
      } catch (e) {
        message.error('Xóa thất bại')
      }
    },
  })
}
</script>
