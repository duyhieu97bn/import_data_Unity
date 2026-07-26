import { createRouter, createWebHashHistory } from 'vue-router'
import Dashboard from '../components/Dashboard.vue'
import DataEntryForm from '../components/DataEntryForm.vue'
import DataTable from '../components/DataTable.vue'
import GoiManager from '../components/GoiManager.vue'

const routes = [
  { path: '/', name: 'Dashboard', component: Dashboard },
  { path: '/nhap', name: 'Nhap', component: DataEntryForm },
  { path: '/xem', name: 'Xem', component: DataTable },
  { path: '/goi', name: 'Goi', component: GoiManager },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

export default router
