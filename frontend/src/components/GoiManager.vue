<template>
  <div>
    <a-card>
      <template #extra>
        <a-space>
          <a-upload :before-upload="handleImport" :show-upload-list="false" accept=".xlsx,.xls">
            <a-button :loading="importing">Import Excel</a-button>
          </a-upload>
          <a-button type="primary" @click="openAdd">Thêm gói</a-button>
        </a-space>
      </template>
      <a-table
        :data-source="goiList"
        :columns="columns"
        :pagination="pagination"
        @change="onTableChange"
        size="small"
        bordered
        :loading="loading"
        :row-key="r => r.id"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'actions'">
            <a-space>
              <a-button type="link" size="small" @click="openEdit(record)">Sửa</a-button>
              <a-button type="link" danger size="small" @click="handleDelete(record)">Xóa</a-button>
            </a-space>
          </template>
          <template v-else-if="column.key === 'giaNiemYet'">
            {{ formatMoney(record.giaNiemYet) }}
          </template>
          <template v-else-if="column.key === 'giaNiemYetGD'">
            {{ formatMoney(record.giaNiemYetGD) }}
          </template>
          <template v-else>
            {{ record[column.key] }}
          </template>
        </template>
      </a-table>
    </a-card>

    <a-modal v-model:open="modalVisible" :title="editing ? 'Sửa gói' : 'Thêm gói'" width="700px" @ok="handleSave" :confirm-loading="saving" :destroy-on-close="true">
      <a-form :model="form" layout="vertical">
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="Mã gói">
              <a-input v-model:value="form.maGoi" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="CLB">
              <a-input v-model:value="form.clb" />
            </a-form-item>
          </a-col>
        </a-row>
        <a-row :gutter="16">
          <a-col :span="8">
            <a-form-item label="Loại thẻ">
              <a-input v-model:value="form.loaiThe" />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="Mã gói hoạt động">
              <a-input v-model:value="form.maGoiHoatDong" />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="Phân bổ">
              <a-input v-model:value="form.phanBo" />
            </a-form-item>
          </a-col>
        </a-row>
        <a-row :gutter="16">
          <a-col :span="8">
            <a-form-item label="Mã loại thẻ target">
              <a-input v-model:value="form.maLoaiTheTarget" />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="Mã loại thẻ lọc PT">
              <a-input v-model:value="form.maLoaiTheLocPT" />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="Thời gian">
              <a-input v-model:value="form.thoiGian" />
            </a-form-item>
          </a-col>
        </a-row>
        <a-row :gutter="16">
          <a-col :span="8">
            <a-form-item label="Thời gian 2">
              <a-input v-model:value="form.thoiGian2" />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="Giá niêm yết">
              <a-input-number v-model:value="form.giaNiemYet" style="width:100%" :formatter="v => `${v}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')" :parser="v => v.replace(/,/g, '')" />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="Giá niêm yết GD">
              <a-input-number v-model:value="form.giaNiemYetGD" style="width:100%" :formatter="v => `${v}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')" :parser="v => v.replace(/,/g, '')" />
            </a-form-item>
          </a-col>
        </a-row>
        <a-form-item label="Ghi chú">
          <a-input v-model:value="form.ghiChu" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { message, Modal } from 'ant-design-vue'
import { fetchGoiList, createGoi, updateGoi, deleteGoi } from '../services/api'
import api from '../services/api'

const pagination = reactive({
  current: 1,
  pageSize: 20,
  showSizeChanger: true,
  pageSizeOptions: ['10', '20', '50', '100'],
  showTotal: (total) => `Tổng: ${total} gói`,
})

function onTableChange(pag) {
  pagination.current = pag.current
  pagination.pageSize = pag.pageSize
}

const goiList = ref([])
const loading = ref(false)
const modalVisible = ref(false)
const saving = ref(false)
const editing = ref(false)
const importing = ref(false)
const emptyForm = {
  maGoi: '', clb: '', loaiThe: '', maGoiHoatDong: '', phanBo: '',
  maLoaiTheTarget: '', maLoaiTheLocPT: '', thoiGian: '', thoiGian2: '',
  giaNiemYet: 0, giaNiemYetGD: 0, ghiChu: '',
}
const form = ref({ ...emptyForm })

const columns = [
  { title: 'Mã gói', dataIndex: 'maGoi', key: 'maGoi', width: 120 },
  { title: 'CLB', dataIndex: 'clb', key: 'clb', width: 100 },
  { title: 'Loại thẻ', dataIndex: 'loaiThe', key: 'loaiThe', width: 100 },
  { title: 'Mã gói HĐ', dataIndex: 'maGoiHoatDong', key: 'maGoiHoatDong', width: 100 },
  { title: 'Phân bổ', dataIndex: 'phanBo', key: 'phanBo', width: 80 },
  { title: 'Target', dataIndex: 'maLoaiTheTarget', key: 'maLoaiTheTarget', width: 80 },
  { title: 'Lọc PT', dataIndex: 'maLoaiTheLocPT', key: 'maLoaiTheLocPT', width: 80 },
  { title: 'Thời gian', dataIndex: 'thoiGian', key: 'thoiGian', width: 80 },
  { title: 'TG 2', dataIndex: 'thoiGian2', key: 'thoiGian2', width: 80 },
  { title: 'Giá NY', dataIndex: 'giaNiemYet', key: 'giaNiemYet', width: 100 },
  { title: 'Giá NY GD', dataIndex: 'giaNiemYetGD', key: 'giaNiemYetGD', width: 100 },
  { title: 'Ghi chú', dataIndex: 'ghiChu', key: 'ghiChu', width: 150 },
  { title: 'Hành động', key: 'actions', width: 100, fixed: 'right' },
]

function formatMoney(v) {
  if (v === null || v === undefined || v === 0) return '0'
  return Number(v).toLocaleString('vi-VN')
}

async function loadGoi() {
  loading.value = true
  try {
    const res = await fetchGoiList()
    goiList.value = res.data || []
  } catch (e) {
    message.error('Tải danh sách gói thất bại')
  } finally {
    loading.value = false
  }
}

function openAdd() {
  editing.value = false
  form.value = { ...emptyForm }
  modalVisible.value = true
}

function openEdit(record) {
  editing.value = true
  form.value = { ...record }
  modalVisible.value = true
}

async function handleSave() {
  saving.value = true
  try {
    if (editing.value) {
      await updateGoi(form.value.id, form.value)
      message.success('Đã cập nhật gói')
    } else {
      await createGoi(form.value)
      message.success('Đã thêm gói mới')
    }
    modalVisible.value = false
    loadGoi()
  } catch (e) {
    message.error('Lỗi: ' + (e.response?.data?.detail || e.message))
  } finally {
    saving.value = false
  }
}

async function handleImport(file) {
  importing.value = true
  try {
    const form = new FormData()
    form.append('file', file)
    const res = await api.post('/goi/import', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    message.success(`Đã import ${res.data.imported}/${res.data.total} gói`)
    loadGoi()
  } catch (e) {
    message.error('Import thất bại: ' + (e.response?.data?.detail || e.message))
  } finally {
    importing.value = false
  }
  return false
}

function handleDelete(record) {
  Modal.confirm({
    title: 'Xác nhận xóa',
    content: `Xóa gói "${record.maGoi}"?`,
    okText: 'Xóa',
    cancelText: 'Hủy',
    okType: 'danger',
    async onOk() {
      try {
        await deleteGoi(record.id)
        message.success('Đã xóa')
        loadGoi()
      } catch (e) {
        message.error('Xóa thất bại')
      }
    },
  })
}

onMounted(loadGoi)
</script>
