<template>
  <a-config-provider :locale="locale">
    <a-layout style="min-height: 100vh">
      <a-layout-header style="background: #fff; padding: 0 24px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #f0f0f0">
        <h2 style="margin: 0; color: #1677ff">Hệ thống nhập dữ liệu</h2>
        <div></div>
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

dayjs.locale('vi')

const locale = viVN
const router = useRouter()
const route = useRoute()
const store = useDataStore()
const collapsed = ref(false)

const componentMap = { dashboard: Dashboard, nhap: DataEntryForm, xem: DataTable, goi: GoiManager }

function hashToMenuKey() {
  const key = window.location.hash.replace('#/', '').split('/')[0]
  return key || 'dashboard'
}
const selectedKeys = ref([hashToMenuKey()])
const currentComponent = computed(() => componentMap[selectedKeys.value[0]])

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
