import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

export function fetchGoiList() {
  return api.get('/goi')
}

export function fetchSaleList() {
  return api.get('/sale')
}

export function fetchPtChamSocList() {
  return api.get('/pt-cham-soc')
}

export function fetchCsNhapList() {
  return api.get('/cs-nhap')
}

export function fetchAllRecords() {
  return api.get('/records')
}

export function createRecord(data) {
  return api.post('/records', data)
}

export function updateRecord(stt, data) {
  return api.put(`/records/${stt}`, data)
}

export function deleteRecord(stt) {
  return api.delete(`/records/${stt}`)
}

export function fetchGoiDetail(maGoi) {
  return api.get(`/goi/${encodeURIComponent(maGoi)}`)
}

export function createGoi(data) {
  return api.post('/goi', data)
}

export function updateGoi(id, data) {
  return api.put(`/goi/${id}`, data)
}

export function deleteGoi(id) {
  return api.delete(`/goi/${id}`)
}

export function downloadTemplate() {
  window.open('/api/template/download', '_blank')
}

export function uploadTemplate(file) {
  const form = new FormData()
  form.append('file', file)
  return api.post('/template/upload', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export function previewUpload(file) {
  const form = new FormData()
  form.append('file', file)
  return api.post('/upload/preview', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export function confirmUpload(records) {
  return api.post('/upload/confirm', { records })
}

export default api
