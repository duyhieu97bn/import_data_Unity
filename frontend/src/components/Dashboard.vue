<template>
  <div>
    <a-row :gutter="[16, 16]">
      <a-col v-for="s in statCards" :key="s.key" :xs="12" :sm="8" :lg="4">
        <a-card size="small">
          <a-statistic :title="s.title" :value="stats[s.valueKey]" :value-style="s.valueStyle" :formatter="s.formatMoney ? v => formatMoney(v) : undefined" />
        </a-card>
      </a-col>
    </a-row>

    <a-row :gutter="[16, 16]" style="margin-top: 16px">
      <a-col :xs="24" :lg="12">
        <a-card title="Doanh thu theo tháng" size="small">
          <Bar v-if="revenueByMonth.labels.length" :data="revenueByMonthChart" :options="commonOptions" />
        </a-card>
      </a-col>
      <a-col :xs="24" :lg="12">
        <a-card title="Hợp đồng mới theo tháng" size="small">
          <Line v-if="newContractsByMonth.labels.length" :data="newContractsByMonthChart" :options="commonOptions" />
        </a-card>
      </a-col>
    </a-row>

    <a-row :gutter="[16, 16]" style="margin-top: 16px">
      <a-col :xs="24" :lg="8">
        <a-card title="Tình trạng hợp đồng" size="small">
          <Doughnut v-if="contractStatus.labels.length" :data="contractStatusChart" :options="doughnutOptions" />
        </a-card>
      </a-col>
      <a-col :xs="24" :lg="8">
        <a-card title="Phân bố gói tập" size="small">
          <Doughnut v-if="packageDist.labels.length" :data="packageDistChart" :options="doughnutOptions" />
        </a-card>
      </a-col>
      <a-col :xs="24" :lg="8">
        <a-card title="Nguồn khách hàng" size="small">
          <Doughnut v-if="customerSource.labels.length" :data="customerSourceChart" :options="doughnutOptions" />
        </a-card>
      </a-col>
    </a-row>

    <a-row :gutter="[16, 16]" style="margin-top: 16px">
      <a-col :xs="24" :lg="12">
        <a-card title="Top Sale" size="small">
          <Bar v-if="topSales.labels.length" :data="topSalesChart" :options="horizontalBarOptions" />
        </a-card>
      </a-col>
      <a-col :xs="24" :lg="12">
        <a-card title="Doanh thu theo CLB" size="small">
          <Bar v-if="revenueByClb.labels.length" :data="revenueByClbChart" :options="commonOptions" />
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script setup>
import { reactive, computed, onMounted } from 'vue'
import { Bar, Doughnut, Line } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement, PointElement, LineElement } from 'chart.js'
import api from '../services/api'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement, PointElement, LineElement)

const formatMoney = (v) => {
  if (v === null || v === undefined) return '0'
  return Number(v).toLocaleString('vi-VN') + 'đ'
}

const stats = reactive({
  totalRevenue: 0, totalContracts: 0, totalCustomers: 0,
  totalPackages: 0, activeContracts: 0, expiredContracts: 0,
})

const statCards = [
  { title: 'Doanh thu', valueKey: 'totalRevenue', formatMoney: true, key: 'revenue' },
  { title: 'Hợp đồng', valueKey: 'totalContracts', key: 'contracts' },
  { title: 'Đang hoạt động', valueKey: 'activeContracts', valueStyle: { color: '#3f8600' }, key: 'active' },
  { title: 'Hết hạn', valueKey: 'expiredContracts', valueStyle: { color: '#cf1322' }, key: 'expired' },
  { title: 'Khách hàng', valueKey: 'totalCustomers', key: 'customers' },
  { title: 'Gói tập', valueKey: 'totalPackages', key: 'packages' },
]

const revenueByMonth = reactive({ labels: [], values: [] })
const topSales = reactive({ labels: [], values: [] })
const packageDist = reactive({ labels: [], values: [] })
const contractStatus = reactive({ labels: [], values: [] })
const revenueByClb = reactive({ labels: [], values: [] })
const customerSource = reactive({ labels: [], values: [] })
const newContractsByMonth = reactive({ labels: [], values: [] })

const commonOptions = {
  responsive: true,
  plugins: { legend: { display: false } },
  scales: { y: { beginAtZero: true } },
}

const horizontalBarOptions = {
  responsive: true,
  indexAxis: 'y',
  plugins: { legend: { display: false } },
  scales: { x: { beginAtZero: true } },
}

const doughnutOptions = {
  responsive: true,
  plugins: { legend: { position: 'bottom' } },
}

const COLORS = ['#1677ff', '#52c41a', '#faad14', '#ff4d4f', '#722ed1', '#13c2c2', '#eb2f96', '#fa8c16', '#2f54eb', '#a0d911']

function chartData(labels, values, label, color) {
  return {
    labels,
    datasets: [{ label, data: values, backgroundColor: color || '#1677ff', borderRadius: 4 }],
  }
}

const revenueByMonthChart = computed(() => chartData(revenueByMonth.labels, revenueByMonth.values, 'Doanh thu'))
const newContractsByMonthChart = computed(() => chartData(newContractsByMonth.labels, newContractsByMonth.values, 'Hợp đồng'))
const topSalesChart = computed(() => chartData(topSales.labels, topSales.values, 'Doanh thu'))
const revenueByClbChart = computed(() => chartData(revenueByClb.labels, revenueByClb.values, 'Doanh thu'))

const contractStatusChart = computed(() => ({
  labels: contractStatus.labels,
  datasets: [{ data: contractStatus.values, backgroundColor: [COLORS[0], COLORS[3], '#d9d9d9'] }],
}))

const packageDistChart = computed(() => ({
  labels: packageDist.labels,
  datasets: [{ data: packageDist.values, backgroundColor: COLORS.slice(0, packageDist.labels.length) }],
}))

const customerSourceChart = computed(() => ({
  labels: customerSource.labels,
  datasets: [{ data: customerSource.values, backgroundColor: COLORS.slice(0, customerSource.labels.length) }],
}))

async function loadDashboard() {
  try {
    const [s, rbm, ts, pd, cs, rbc, csrc, ncm] = await Promise.all([
      api.get('/dashboard/stats'),
      api.get('/dashboard/revenue-by-month'),
      api.get('/dashboard/top-sales'),
      api.get('/dashboard/package-distribution'),
      api.get('/dashboard/contract-status'),
      api.get('/dashboard/revenue-by-clb'),
      api.get('/dashboard/customer-source'),
      api.get('/dashboard/new-contracts-by-month'),
    ])
    Object.assign(stats, s.data)
    Object.assign(revenueByMonth, rbm.data)
    Object.assign(topSales, ts.data)
    Object.assign(packageDist, pd.data)
    Object.assign(contractStatus, cs.data)
    Object.assign(revenueByClb, rbc.data)
    Object.assign(customerSource, csrc.data)
    Object.assign(newContractsByMonth, ncm.data)
  } catch (e) {
    console.error('Dashboard load error', e)
  }
}

onMounted(loadDashboard)
</script>
