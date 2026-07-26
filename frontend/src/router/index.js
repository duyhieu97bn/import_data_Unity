import { createRouter, createWebHashHistory } from 'vue-router'
import DataEntryForm from '../components/DataEntryForm.vue'
import DataTable from '../components/DataTable.vue'
import GoiManager from '../components/GoiManager.vue'

const routes = [
  { path: '/', redirect: '/nhap' },
  { path: '/nhap', name: 'Nhap', component: DataEntryForm },
  { path: '/xem', name: 'Xem', component: DataTable },
  { path: '/goi', name: 'Goi', component: GoiManager },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

export default router
